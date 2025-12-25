"""Base API class for ESB OMS API endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from esb_oms._http import BearerHTTPClient


class BaseAPI:
    """Base class for all API endpoint groups using Bearer token authentication.

    This class provides common functionality for making API requests.
    Authentication is handled automatically by the BearerHTTPClient.

    Attributes:
        _http: The HTTP client for making requests (with auto Bearer auth).
    """

    def __init__(self, http_client: BearerHTTPClient) -> None:
        """Initialize the API endpoint group.

        Args:
            http_client: The Bearer HTTP client for making requests.
        """
        self._http = http_client

    def _get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any] | list[Any]:
        """Make a GET request with automatic Bearer authentication.

        Args:
            path: API endpoint path.
            params: Query parameters.
            headers: Additional headers.

        Returns:
            Parsed JSON response (dict or list).
        """
        return self._http.get(path, params=params, headers=headers)

    def _post(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any] | list[Any]:
        """Make a POST request with automatic Bearer authentication.

        Args:
            path: API endpoint path.
            params: Query parameters.
            json: JSON body data.
            headers: Additional headers.

        Returns:
            Parsed JSON response (dict or list).
        """
        return self._http.post(path, params=params, json=json, headers=headers)
