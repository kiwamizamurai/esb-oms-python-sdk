"""ESB OMS API Client Library.

A Python client library for interacting with the ESB OMS (Order Management System) API.
Provides a clean, type-safe interface for POS systems to integrate with ESB Core.

Example:
    ```python
    from esb_oms import ESBClient, Environment

    # Using username/password authentication
    client = ESBClient(
        username="your_username",
        password="your_password",
        environment=Environment.PRODUCTION,
    )

    # Or using static token (API key)
    client = ESBClient(
        static_token="your_api_key",
        environment=Environment.PRODUCTION,
    )

    # Access APIs
    menus = client.master.get_menu(branch_code="BR001", visit_purpose_id="1")
    client.sales.push_sales_data(sales_head=data)
    ```
"""

from esb_oms.client import ESBClient
from esb_oms.environments import Environment
from esb_oms.exceptions import (
    ESBAuthenticationError,
    ESBAuthorizationError,
    ESBError,
    ESBMethodNotAllowedError,
    ESBNotFoundError,
    ESBRateLimitError,
    ESBServerError,
    ESBTokenRefreshError,
    ESBValidationError,
)

__version__ = "0.1.0"

__all__ = [
    "ESBAuthenticationError",
    "ESBAuthorizationError",
    "ESBClient",
    "ESBError",
    "ESBMethodNotAllowedError",
    "ESBNotFoundError",
    "ESBRateLimitError",
    "ESBServerError",
    "ESBTokenRefreshError",
    "ESBValidationError",
    "Environment",
]
