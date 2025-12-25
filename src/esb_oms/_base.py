"""Base client implementation for ESB OMS API."""

from __future__ import annotations

import structlog

from esb_oms._http import (
    BasicAuthHTTPClient,
    BearerHTTPClient,
    ManualTokenHTTPClient,
)
from esb_oms.api.auth import AuthAPI
from esb_oms.environments import (
    Environment,
    get_api_url,
    get_core_url,
    get_master_pos_url,
)
from esb_oms.exceptions import ESBAuthenticationError, ESBTokenRefreshError
from esb_oms.models.auth import TokenInfo

logger = structlog.get_logger(__name__)


class BaseClient:
    """Base client with authentication management.

    This class handles:
    - HTTP client setup for different API endpoints and auth methods
    - Token management (storage, retrieval, auto-refresh)
    - Authentication state

    Attributes:
        environment: The target ESB environment.
        auto_refresh: Whether to automatically refresh expired tokens.
    """

    def __init__(
        self,
        *,
        username: str | None = None,
        password: str | None = None,
        static_token: str | None = None,
        environment: Environment = Environment.PRODUCTION,
        auto_refresh: bool = True,
        timeout: float = 30.0,
    ) -> None:
        """Initialize the base client.

        You can authenticate using either:
        1. Username and password (will login automatically)
        2. Static token (API key from ESB Core)

        Args:
            username: ESB Core username for login authentication.
            password: ESB Core password for login authentication.
            static_token: Static API token for API key authentication.
            environment: Target environment (staging or production).
            auto_refresh: Whether to auto-refresh expired tokens.
            timeout: Request timeout in seconds.

        Raises:
            ValueError: If neither credentials nor static token provided.
        """
        self.environment = environment
        self.auto_refresh = auto_refresh
        self._timeout = timeout

        # Validate authentication method
        has_credentials = username is not None and password is not None
        has_static_token = static_token is not None

        if not has_credentials and not has_static_token:
            msg = "Must provide either (username, password) or static_token"
            raise ValueError(msg)

        # Store credentials for auto-login and Basic Auth
        self._username = username
        self._password = password
        self._static_token = static_token

        # Token state
        self._token_info: TokenInfo | None = None

        # Initialize HTTP clients with appropriate auth methods

        # Core HTTP client - for Auth API (login/refresh)
        self._core_http = ManualTokenHTTPClient(
            base_url=get_core_url(environment),
            timeout=timeout,
        )

        # API HTTP client - uses Bearer token (static or access token)
        self._api_http = BearerHTTPClient(
            base_url=get_api_url(environment),
            get_token=self._get_token,
            timeout=timeout,
        )

        # Master POS HTTP client - uses Basic Auth with credentials
        self._master_pos_http = BasicAuthHTTPClient(
            base_url=get_master_pos_url(environment),
            get_credentials=self._get_credentials,
            timeout=timeout,
        )

        # Core Bearer HTTP client - uses Bearer token on Core URL
        # Used for endpoints like sales-payment-summary
        self._core_bearer_http = BearerHTTPClient(
            base_url=get_core_url(environment),
            get_token=self._get_token,
            timeout=timeout,
        )

        # Initialize Auth API (uses core HTTP client)
        self._auth = AuthAPI(self._core_http)

    @property
    def auth(self) -> AuthAPI:
        """Access the Authentication API.

        Returns:
            The AuthAPI instance for login and token operations.
        """
        return self._auth

    @property
    def is_authenticated(self) -> bool:
        """Check if the client has valid authentication.

        Returns:
            True if using static token or has access token.
        """
        if self._static_token:
            return True
        return self._token_info is not None

    def _get_token(self) -> str | None:
        """Get the current Bearer token.

        This is used by BearerHTTPClient to get the token for requests.
        If using static token, returns that. Otherwise returns access token.

        Returns:
            The current token or None if not authenticated.
        """
        if self._static_token:
            return self._static_token
        if self._token_info:
            return self._token_info.access_token
        return None

    def _get_credentials(self) -> tuple[str, str] | None:
        """Get the Basic Auth credentials.

        This is used by BasicAuthHTTPClient for Master POS API.

        Returns:
            Tuple of (username, password) or None if not available.
        """
        if self._username and self._password:
            return (self._username, self._password)
        return None

    def login(self) -> None:
        """Login using stored credentials.

        This is called automatically when needed if auto_refresh is True
        and credentials were provided.

        Raises:
            ESBAuthenticationError: If login fails.
            ValueError: If no credentials were provided.
        """
        if not self._username or not self._password:
            msg = "Cannot login: no credentials provided"
            raise ValueError(msg)

        logger.info("auth_login_start", username=self._username)
        result = self._auth.login(self._username, self._password)
        self._token_info = TokenInfo(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            username=result.username,
            company_code=result.company_code,
        )
        logger.info(
            "auth_login_success",
            username=result.username,
            company_code=result.company_code,
        )

    def refresh_token(self) -> None:
        """Refresh the access token using the refresh token.

        Raises:
            ESBTokenRefreshError: If refresh fails.
            ValueError: If no refresh token available.
        """
        if not self._token_info or not self._token_info.refresh_token:
            msg = "Cannot refresh: no refresh token available"
            raise ValueError(msg)

        logger.info("auth_refresh_start")
        try:
            result = self._auth.refresh(self._token_info.refresh_token)
            self._token_info = TokenInfo(
                access_token=result.access_token,
                refresh_token=result.refresh_token,
                username=result.username,
                company_code=result.company_code,
            )
            logger.info("auth_refresh_success")
        except ESBAuthenticationError as e:
            logger.warning(
                "auth_refresh_failed", code=e.code, status_code=e.status_code
            )
            raise ESBTokenRefreshError(
                "Failed to refresh token",
                code=e.code,
                status_code=e.status_code,
                response_data=e.response_data,
            ) from e

    def ensure_authenticated(self) -> None:
        """Ensure the client is authenticated.

        If using static token, does nothing.
        If using credentials and not logged in, logs in.

        Raises:
            ESBAuthenticationError: If authentication fails.
        """
        if self._static_token:
            return

        if not self._token_info:
            self.login()

    def close(self) -> None:
        """Close the client and release resources."""
        self._core_http.close()
        self._api_http.close()
        self._master_pos_http.close()
        self._core_bearer_http.close()

    def __enter__(self) -> BaseClient:
        """Enter context manager."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Exit context manager."""
        self.close()
