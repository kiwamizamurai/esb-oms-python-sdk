"""Internal HTTP client for ESB OMS API."""

from __future__ import annotations

import json
from types import TracebackType
from typing import TYPE_CHECKING, Any

import httpx
import structlog

from esb_oms.exceptions import (
    ESBAuthenticationError,
    ESBAuthorizationError,
    ESBConnectionError,
    ESBError,
    ESBMethodNotAllowedError,
    ESBNotFoundError,
    ESBRateLimitError,
    ESBServerError,
    ESBTimeoutError,
    ESBValidationError,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping


# Default timeout in seconds
DEFAULT_TIMEOUT = 30.0

# User agent for API requests
USER_AGENT = "esb-oms-python/0.1.0"

logger = structlog.get_logger(__name__)


class HTTPClient:
    """Base HTTP client for making API requests.

    This class wraps httpx.Client and provides error handling
    specific to the ESB OMS API. No authentication is applied.
    """

    def __init__(
        self,
        *,
        base_url: str,
        timeout: float = DEFAULT_TIMEOUT,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize the HTTP client.

        Args:
            base_url: Base URL for API requests.
            timeout: Request timeout in seconds.
            headers: Additional headers to include in all requests.
        """
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._default_headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            **(headers or {}),
        }
        self._client: httpx.Client | None = None

    @property
    def client(self) -> httpx.Client:
        """Get or create the httpx client."""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                timeout=self._timeout,
                headers=self._default_headers,
            )
        return self._client

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> HTTPClient:
        """Enter context manager."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context manager."""
        self.close()

    def _prepare_auth(self) -> tuple[dict[str, str], httpx.Auth | None]:
        """Prepare authentication for request.

        Returns:
            Tuple of (headers_dict, auth_object).
        """
        return {}, None

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any] | list[Any]:
        """Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, etc.).
            path: API endpoint path.
            params: Query parameters.
            json: JSON body data.
            headers: Additional headers for this request.

        Returns:
            Parsed JSON response as a dictionary or list.

        Raises:
            ESBAuthenticationError: When authentication fails.
            ESBAuthorizationError: When permission is denied.
            ESBValidationError: When request validation fails.
            ESBNotFoundError: When resource is not found.
            ESBRateLimitError: When rate limit is exceeded.
            ESBServerError: When server returns 5xx error.
            ESBConnectionError: When connection fails.
            ESBTimeoutError: When request times out.
            ESBError: For other API errors.
        """
        auth_headers, auth = self._prepare_auth()
        request_headers = {**auth_headers, **(headers or {})}

        log = logger.bind(method=method, path=path)
        log.debug("http_request_start", params=params, has_body=json is not None)

        try:
            response = self.client.request(
                method=method,
                url=path,
                params=params,
                json=json,
                headers=request_headers,
                auth=auth,
            )
        except httpx.TimeoutException as e:
            log.warning("http_request_timeout", timeout=self._timeout)
            raise ESBTimeoutError(
                f"Request to {path} timed out after {self._timeout}s"
            ) from e
        except httpx.ConnectError as e:
            log.exception("http_connection_error")
            raise ESBConnectionError(
                f"Failed to connect to {self._base_url}: {e}"
            ) from e
        except httpx.HTTPError as e:
            log.exception("http_error")
            raise ESBConnectionError(f"HTTP error occurred: {e}") from e

        log.debug("http_request_complete", status_code=response.status_code)
        return self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> dict[str, Any] | list[Any]:
        """Handle the API response and raise appropriate exceptions.

        Args:
            response: The HTTP response object.

        Returns:
            Parsed JSON response data (dict or list).

        Raises:
            Various ESB exceptions based on response status and content.
        """
        try:
            json_data: dict[str, Any] | list[Any] = response.json()
        except ValueError as err:
            # Non-JSON response
            if response.status_code >= 500:
                raise ESBServerError(
                    f"Server error: {response.text}",
                    status_code=response.status_code,
                ) from err
            raise ESBError(
                f"Invalid response: {response.text}",
                status_code=response.status_code,
            ) from err

        # If response is a list, return directly (no error metadata)
        if isinstance(json_data, list):
            if response.status_code >= 400:
                # Extract message from first item if available
                msg = "Request failed"
                if json_data and isinstance(json_data[0], dict):
                    msg = json_data[0].get("message", msg)
                # Map HTTP status codes to appropriate exceptions
                if response.status_code == 401:
                    raise ESBAuthenticationError(msg, status_code=response.status_code)
                if response.status_code == 403:
                    raise ESBAuthorizationError(msg, status_code=response.status_code)
                if response.status_code == 404:
                    raise ESBNotFoundError(msg, status_code=response.status_code)
                if response.status_code >= 500:
                    raise ESBServerError(msg, status_code=response.status_code)
                raise ESBError(msg, status_code=response.status_code)
            return json_data

        data = json_data
        # Check for API-level errors
        # Note: status can be "ok", "fail", "failed" or numeric "00", "01"
        status = str(data.get("status", "")).lower()
        code = data.get("code")
        # V1 APIs use "error" field instead of "message"
        message = data.get("message") or data.get("error") or "Unknown error"

        # Successful response
        # Note: V1 APIs return status "00" for success, "01" for error
        if status in ("ok", "00") or (
            status not in ("fail", "failed", "01") and response.status_code < 400
        ):
            return data

        # Handle specific error codes
        error_kwargs: dict[str, Any] = {
            "code": code,
            "status_code": response.status_code,
            "response_data": data,
        }

        # Authentication errors (401)
        if response.status_code == 401:
            raise ESBAuthenticationError(message, **error_kwargs)

        # Authorization errors (403)
        if response.status_code == 403:
            raise ESBAuthorizationError(message, **error_kwargs)

        # Not found errors (404)
        if response.status_code == 404:
            raise ESBNotFoundError(message, **error_kwargs)

        # Method not allowed errors (405)
        if response.status_code == 405:
            raise ESBMethodNotAllowedError(message, **error_kwargs)

        # Rate limit errors (429)
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise ESBRateLimitError(
                message,
                **error_kwargs,
                retry_after=int(retry_after) if retry_after else None,
            )

        # Validation errors (400, 422)
        # The API returns validation errors in different fields:
        # - "data" field (Backend API V2): list of strings or dict
        # - "errors" field (Master POS/V1 APIs): dict mapping fields to error lists
        if response.status_code in (400, 422):
            validation_errors = data.get("data") or data.get("errors")
            raise ESBValidationError(
                message,
                **error_kwargs,
                validation_errors=validation_errors,
            )

        # Server errors (5xx)
        if response.status_code >= 500:
            raise ESBServerError(message, **error_kwargs)

        # Check for fail status in response body
        # - Auth API: "fail" or "failed" with EC* codes
        # - V1 APIs: "01" for error status
        if status in ("fail", "failed", "01"):
            # Try to determine error type from code
            if code and isinstance(code, str):
                # Core API authentication codes (EC031000xx)
                # EC03100001: Invalid Token
                # EC03100003: Validation Error
                # EC03100032: Invalid username or password
                if code in ("EC03100001", "EC03100032"):
                    raise ESBAuthenticationError(message, **error_kwargs)
                if code == "EC03100003":
                    raise ESBValidationError(
                        message,
                        **error_kwargs,
                        validation_errors=data.get("errors"),
                    )
                # Backend API authentication code
                # EC011401: Unauthorized
                if code == "EC011401":
                    raise ESBAuthenticationError(message, **error_kwargs)
                # Backend API error code EC0110
                # Used for both "not found" and validation errors
                # Message may contain JSON-encoded validation errors
                if code == "EC0110":
                    # Try to parse message as JSON validation errors
                    try:
                        parsed_message = json.loads(message)
                        if isinstance(parsed_message, dict):
                            # Message contains validation errors as JSON
                            raise ESBValidationError(
                                "Validation error",
                                **error_kwargs,
                                validation_errors=parsed_message,
                            )
                    except (json.JSONDecodeError, TypeError):
                        pass
                    # Check if message indicates "not found"
                    if "not found" in message.lower():
                        raise ESBNotFoundError(message, **error_kwargs)
                    # Default to generic error
                    raise ESBError(message, **error_kwargs)
                # Backend API error code EC0118
                # Undefined index errors (missing required fields)
                if code == "EC0118":
                    raise ESBValidationError(message, **error_kwargs)
                # Backend API validation error code
                # EC011400: Validation Error (Shift Data API)
                if code == "EC011400":
                    raise ESBValidationError(
                        message,
                        **error_kwargs,
                        validation_errors=data.get("data"),
                    )

            # V1 APIs without EC codes - detect error type from message
            # "Undefined index:" indicates missing required field
            if "undefined index" in message.lower():
                raise ESBValidationError(message, **error_kwargs)

            raise ESBError(message, **error_kwargs)

        # Generic error
        raise ESBError(message, **error_kwargs)

    def get(
        self,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any] | list[Any]:
        """Make a GET request.

        Args:
            path: API endpoint path.
            params: Query parameters.
            headers: Additional headers.

        Returns:
            Parsed JSON response (dict or list).
        """
        return self.request(
            "GET",
            path,
            params=params,
            headers=headers,
        )

    def post(
        self,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any] | list[Any]:
        """Make a POST request.

        Args:
            path: API endpoint path.
            params: Query parameters.
            json: JSON body data.
            headers: Additional headers.

        Returns:
            Parsed JSON response (dict or list).
        """
        return self.request(
            "POST",
            path,
            params=params,
            json=json,
            headers=headers,
        )


class BearerHTTPClient(HTTPClient):
    """HTTP client with Bearer token authentication.

    This client automatically adds Bearer token to all requests.
    The token is retrieved via a callback function, allowing for
    lazy token fetching and automatic refresh.
    """

    def __init__(
        self,
        *,
        base_url: str,
        get_token: Callable[[], str | None],
        timeout: float = DEFAULT_TIMEOUT,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize the Bearer HTTP client.

        Args:
            base_url: Base URL for API requests.
            get_token: Callback function to get the current Bearer token.
            timeout: Request timeout in seconds.
            headers: Additional headers to include in all requests.
        """
        super().__init__(base_url=base_url, timeout=timeout, headers=headers)
        self._get_token = get_token

    def _prepare_auth(self) -> tuple[dict[str, str], httpx.Auth | None]:
        """Prepare Bearer token authentication.

        Returns:
            Tuple of (headers_dict with Authorization, None).
        """
        token = self._get_token()
        if token:
            return {"Authorization": f"Bearer {token}"}, None
        return {}, None


class BasicAuthHTTPClient(HTTPClient):
    """HTTP client with Basic authentication.

    This client automatically adds Basic authentication to all requests.
    Credentials are retrieved via a callback function.
    """

    def __init__(
        self,
        *,
        base_url: str,
        get_credentials: Callable[[], tuple[str, str] | None],
        timeout: float = DEFAULT_TIMEOUT,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize the Basic Auth HTTP client.

        Args:
            base_url: Base URL for API requests.
            get_credentials: Callback function returning (username, password) tuple.
            timeout: Request timeout in seconds.
            headers: Additional headers to include in all requests.
        """
        super().__init__(base_url=base_url, timeout=timeout, headers=headers)
        self._get_credentials = get_credentials

    def _prepare_auth(self) -> tuple[dict[str, str], httpx.Auth | None]:
        """Prepare Basic authentication.

        Returns:
            Tuple of (empty headers, BasicAuth object).
        """
        credentials = self._get_credentials()
        if credentials:
            return {}, httpx.BasicAuth(username=credentials[0], password=credentials[1])
        return {}, None


class ManualTokenHTTPClient(HTTPClient):
    """HTTP client that accepts token per request.

    This client is used for Auth API where token is passed manually
    (e.g., refresh token for the refresh endpoint).
    """

    def get_with_token(
        self,
        path: str,
        *,
        auth_token: str,
        params: Mapping[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any] | list[Any]:
        """Make a GET request with a specific token.

        Args:
            path: API endpoint path.
            auth_token: Bearer token for this request.
            params: Query parameters.
            headers: Additional headers.

        Returns:
            Parsed JSON response (dict or list).
        """
        request_headers = {"Authorization": f"Bearer {auth_token}", **(headers or {})}
        return self.request(
            "GET",
            path,
            params=params,
            headers=request_headers,
        )
