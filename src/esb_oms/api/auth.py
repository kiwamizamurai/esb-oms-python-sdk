"""Authentication API for ESB OMS."""

from __future__ import annotations

from typing import TYPE_CHECKING

from esb_oms.models.auth import LoginResult, RefreshResult

if TYPE_CHECKING:
    from esb_oms._http import ManualTokenHTTPClient


class AuthAPI:
    """Authentication API endpoints.

    This API handles login and token refresh operations.
    Unlike other APIs, it uses the core URL instead of the main API URL.

    Note:
        This API is different from other APIs because:
        1. It uses the core base URL
        2. Login doesn't require authentication
        3. Refresh uses the refresh token, not the access token
    """

    def __init__(self, http_client: ManualTokenHTTPClient) -> None:
        """Initialize the Auth API.

        Args:
            http_client: HTTP client configured for the core URL.
        """
        self._http = http_client

    def login(self, username: str, password: str) -> LoginResult:
        """Login to ESB Core and obtain access tokens.

        This will log you out of any existing ESB Core session
        using the same credentials.

        Args:
            username: ESB Core username.
            password: ESB Core password.

        Returns:
            Login result containing access and refresh tokens.

        Raises:
            ESBAuthenticationError: If username or password is invalid.

        Example:
            ```python
            result = client.auth.login("user", "password")
            print(f"Logged in as {result.full_name}")
            print(f"Company: {result.company_name}")
            ```
        """
        response = self._http.post(
            "/auth/login",
            json={"username": username, "password": password},
            headers={"Content-Type": "application/json"},
        )
        if isinstance(response, dict):
            return LoginResult.model_validate(response["result"])
        msg = "Unexpected response format from login API"
        raise TypeError(msg)

    def refresh(self, refresh_token: str) -> RefreshResult:
        """Refresh an expired access token.

        Use this to get a new access token when the current one expires.
        Access tokens expire after 1 hour, refresh tokens after 24 hours.

        Args:
            refresh_token: The refresh token from login or previous refresh.

        Returns:
            Refresh result containing new access and refresh tokens.

        Raises:
            ESBAuthenticationError: If the refresh token is invalid or expired.

        Example:
            ```python
            result = client.auth.refresh(old_refresh_token)
            # Update tokens
            new_access_token = result.access_token
            new_refresh_token = result.refresh_token
            ```
        """
        response = self._http.get_with_token(
            "/auth/refresh",
            auth_token=refresh_token,
        )
        if isinstance(response, dict):
            return RefreshResult.model_validate(response["result"])
        msg = "Unexpected response format from refresh API"
        raise TypeError(msg)
