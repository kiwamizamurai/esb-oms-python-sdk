"""Custom exceptions for ESB OMS API client.

Error Response Patterns:
    The ESB OMS API uses several distinct error response formats:

    1. Core API (Auth endpoints):
        {"status": "fail", "code": "EC03100032", "message": "Invalid..."}
        {"status": "fail", "code": "EC03100001", "message": "Invalid Token"}
        {"status": "fail", "code": "EC03100003", "message": "...", "errors": [...]}

    2. Backend API V2 (extv1 endpoints):
        {"code": 401, "message": "Your request was made with invalid credentials."}
        {"code": 400, "message": "...", "data": [...] or {...}}
        {"code": 405, "message": "Method Not Allowed..."}
        {"status": "failed", "code": "EC011400", "message": "...", "data": {...}}

    3. Backend API V1 (ext endpoints):
        {"status": "00", "syncDate": "..."} (success)
        {"status": "01", "error": "Branch Not Found"} (error)
        {"status": "01", "error": "SQLSTATE[23000]: ..."} (SQL error)

    4. Yii Framework (V1 endpoints on auth error):
        {"name": "Unauthorized", "message": "...", "code": 0, "status": 401}

Error Codes:
    EC03100001: Invalid Token
    EC03100003: Validation Error
    EC03100032: Invalid username or password
    EC0110: Resource not found or Validation Error (Backend API - context dependent)
    EC0118: Undefined index / Missing required field (Backend API)
    EC011400: Validation Error (Backend API - Shift Data)
    EC011401: Unauthorized (Backend API)
"""

from __future__ import annotations

from typing import Any, Final

# ESB API Error Codes - Core API
ERROR_CODE_SUCCESS: Final[str] = "EC03100000"
ERROR_CODE_INVALID_TOKEN: Final[str] = "EC03100001"
ERROR_CODE_VALIDATION_ERROR: Final[str] = "EC03100003"
ERROR_CODE_REQUIRED_FIELD: Final[str] = "EC03100023"
ERROR_CODE_MAX_LENGTH: Final[str] = "EC03100025"
ERROR_CODE_INVALID_CREDENTIALS: Final[str] = "EC03100032"

# ESB API Error Codes - Backend API
ERROR_CODE_NOT_FOUND: Final[str] = "EC0110"
ERROR_CODE_UNDEFINED_INDEX: Final[str] = "EC0118"
ERROR_CODE_VALIDATION_ERROR_BACKEND: Final[str] = "EC011400"
ERROR_CODE_UNAUTHORIZED: Final[str] = "EC011401"


class ESBError(Exception):
    """Base exception for all ESB OMS API errors.

    Attributes:
        message: Human-readable error message.
        code: ESB API error code (e.g., "EC03100032").
        status_code: HTTP status code if applicable.
        response_data: Raw response data from the API.
    """

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        status_code: int | None = None,
        response_data: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the ESB error.

        Args:
            message: Human-readable error message.
            code: ESB API error code.
            status_code: HTTP status code.
            response_data: Raw response data from the API.
        """
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.response_data = response_data

    def __str__(self) -> str:
        """Return string representation of the error."""
        parts = [self.message]
        if self.code:
            parts.append(f"[{self.code}]")
        if self.status_code:
            parts.append(f"(HTTP {self.status_code})")
        return " ".join(parts)

    def __repr__(self) -> str:
        """Return detailed representation of the error."""
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"code={self.code!r}, "
            f"status_code={self.status_code!r})"
        )


class ESBAuthenticationError(ESBError):
    """Raised when authentication fails.

    This typically occurs when:
    - Invalid username or password (EC03100032)
    - Invalid or expired access token (EC03100001)
    - Invalid or expired refresh token
    - HTTP 401 status code

    Error codes:
        EC03100032: Invalid username or password (login failure)
        EC03100001: Invalid Token (token validation failure)
    """


class ESBAuthorizationError(ESBError):
    """Raised when the user lacks permission for the requested action.

    This typically occurs when:
    - The user doesn't have access to a specific resource
    - The API key lacks required privileges
    """


class ESBValidationError(ESBError):
    """Raised when request validation fails.

    This typically occurs when:
    - Required fields are missing
    - Field values are invalid
    - Data format is incorrect
    - HTTP 400 or 422 status code
    - Core API error code EC03100003

    Error codes:
        EC03100003: Validation Error (Core API format)

    Response formats:
        Core API: {"status": "fail", "code": "EC03100003", "errors": [...]}
        Backend API: {"code": 400, "message": "...", "data": [...]}

    The validation_errors attribute contains detailed error information.
    It can be a list of error strings, or a dict mapping field names to errors.
    """

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        status_code: int | None = None,
        response_data: dict[str, Any] | None = None,
        validation_errors: list[str] | dict[str, list[str]] | None = None,
    ) -> None:
        """Initialize the validation error.

        Args:
            message: Human-readable error message.
            code: ESB API error code.
            status_code: HTTP status code.
            response_data: Raw response data from the API.
            validation_errors: Validation error details (list or dict by field).
        """
        super().__init__(
            message,
            code=code,
            status_code=status_code,
            response_data=response_data,
        )
        self.validation_errors = validation_errors


class ESBNotFoundError(ESBError):
    """Raised when a requested resource is not found.

    HTTP 404 status code or error code EC0110.

    Response format (Backend API):
        {"timeStamp": "...", "status": "failed", "code": "EC0110",
         "message": "Menu Category not found. Invalid menuCategoryID", "result": []}

    Error codes:
        EC0110: Resource not found (Menu Category, Menu Template, etc.)
    """


class ESBMethodNotAllowedError(ESBError):
    """Raised when the HTTP method is not allowed for the endpoint.

    HTTP 405 status code. This typically occurs when using GET
    on POST-only endpoints or vice versa.

    Response format:
        {"code": 405, "message": "Method Not Allowed. This URL can only..."}
    """


class ESBRateLimitError(ESBError):
    """Raised when the API rate limit is exceeded.

    Attributes:
        retry_after: Suggested wait time in seconds before retrying.
    """

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        status_code: int | None = None,
        response_data: dict[str, Any] | None = None,
        retry_after: int | None = None,
    ) -> None:
        """Initialize the rate limit error.

        Args:
            message: Human-readable error message.
            code: ESB API error code.
            status_code: HTTP status code.
            response_data: Raw response data from the API.
            retry_after: Suggested wait time in seconds before retrying.
        """
        super().__init__(
            message,
            code=code,
            status_code=status_code,
            response_data=response_data,
        )
        self.retry_after = retry_after


class ESBServerError(ESBError):
    """Raised when the ESB server returns an error (5xx status codes)."""


class ESBConnectionError(ESBError):
    """Raised when connection to the ESB API fails.

    This typically occurs when:
    - Network is unavailable
    - DNS resolution fails
    - Connection times out
    """


class ESBTimeoutError(ESBError):
    """Raised when an API request times out."""


class ESBTokenExpiredError(ESBAuthenticationError):
    """Raised when the access token has expired.

    This is a specific authentication error that indicates the token
    needs to be refreshed.
    """


class ESBTokenRefreshError(ESBAuthenticationError):
    """Raised when token refresh fails.

    This typically occurs when:
    - The refresh token has expired
    - The refresh token is invalid
    """
