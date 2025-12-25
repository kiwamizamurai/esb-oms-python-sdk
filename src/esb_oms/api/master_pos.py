"""Master POS API for ESB OMS.

This API uses Basic authentication (username/password) instead of
Bearer token authentication used by other APIs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import TypeAdapter

from esb_oms.models.master import (
    Branch,
    GetBranchRequest,
    GetMenuRequest,
    GetPaymentMethodRequest,
    GetStockBranchRequest,
    GetVisitPurposeRequest,
    MenuCategory,
    PaymentMethodType,
    StockBranchItem,
    VisitPurpose,
)

if TYPE_CHECKING:
    from esb_oms._http import BasicAuthHTTPClient


class MasterPOSAPI:
    """Master POS API endpoints.

    This API provides access to master data for POS systems including:
    - Menu data (categories, items, packages, extras)
    - Stock data by branch
    - Visit purposes
    - Payment methods
    - Branch/outlet information

    Note:
        This API uses Basic authentication with ESB Core credentials,
        unlike other APIs that use Bearer token authentication.

    Example:
        ```python
        # Get menu data
        menus = client.master.get_menu(
            branch_code="BR001",
            visit_purpose_id="1",
        )
        for category in menus:
            print(f"Category: {category.menu_category_desc}")

        # Get branches
        branches = client.master.get_branch()
        for branch in branches:
            print(f"Branch: {branch.branch_name}")
        ```
    """

    def __init__(self, http_client: BasicAuthHTTPClient) -> None:
        """Initialize the Master POS API.

        Args:
            http_client: Basic Auth HTTP client configured for the Master POS API URL.
        """
        self._http = http_client

    def _post(self, path: str, json: dict[str, Any]) -> Any:
        """Make a POST request with automatic Basic Auth.

        Args:
            path: API endpoint path.
            json: JSON body data.

        Returns:
            Raw response data (usually a list or dict).
        """
        return self._http.post(
            path,
            json=json,
            headers={"Content-Type": "application/json"},
        )

    def get_menu(
        self,
        branch_code: str,
        visit_purpose_id: str,
    ) -> list[MenuCategory]:
        """Get menu data for a branch and visit purpose.

        Retrieve all menu categories with their items, packages, and extras
        for a specific branch and visit purpose combination.

        Args:
            branch_code: Branch code to filter menus.
            visit_purpose_id: Visit purpose ID to filter menus.

        Returns:
            List of menu categories with nested menu items.

        Raises:
            ESBValidationError: If branch_code or visit_purpose_id is empty.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            menus = client.master.get_menu(
                branch_code="BR001",
                visit_purpose_id="1",
            )
            for category in menus:
                print(f"Category: {category.menu_category_desc}")
                for detail in category.menu_category_details:
                    for menu in detail.menus:
                        print(f"  - {menu.menu_name}: {menu.price}")
            ```
        """
        request = GetMenuRequest(
            filter_branch_code=branch_code,
            filter_visit_purpose_id=visit_purpose_id,
        )
        response = self._post(
            "/external/general/get-menu",
            json=request.model_dump(by_alias=True),
        )
        adapter = TypeAdapter(list[MenuCategory])
        return adapter.validate_python(response)

    def get_stock_branch(self, branch_code: str) -> list[StockBranchItem]:
        """Get stock data for a branch.

        Retrieve product stock information for a specific branch.

        Args:
            branch_code: Branch code to get stock for.

        Returns:
            List of stock items with quantities.

        Raises:
            ESBValidationError: If branch_code is empty.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            stocks = client.master.get_stock_branch(branch_code="BR001")
            for stock in stocks:
                print(f"{stock.product_name}: {stock.stock} {stock.uom_name}")
            ```
        """
        request = GetStockBranchRequest(filter_branch_code=branch_code)
        response = self._post(
            "/external/general/stock-branch",
            json=request.model_dump(by_alias=True),
        )
        adapter = TypeAdapter(list[StockBranchItem])
        return adapter.validate_python(response)

    def get_visit_purpose(
        self,
        visit_purpose_id: str | None = None,
    ) -> list[VisitPurpose]:
        """Get visit purposes.

        Retrieve a list of visit purposes, optionally filtered by ID.

        Args:
            visit_purpose_id: Optional visit purpose ID to filter.

        Returns:
            List of visit purposes.

        Raises:
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            # Get all visit purposes
            purposes = client.master.get_visit_purpose()
            for purpose in purposes:
                print(f"{purpose.visit_purpose_name}")

            # Get specific visit purpose
            purposes = client.master.get_visit_purpose(visit_purpose_id="1")
            ```
        """
        request = GetVisitPurposeRequest(visit_purpose_id=visit_purpose_id)
        response = self._post(
            "/external/general/get-visit-purpose",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        adapter = TypeAdapter(list[VisitPurpose])
        return adapter.validate_python(response)

    def get_payment_method(
        self,
        branch_code: str,
    ) -> dict[str, PaymentMethodType]:
        """Get payment methods for a branch.

        Retrieve available payment methods grouped by type for a specific branch.

        Args:
            branch_code: Branch code to get payment methods for.

        Returns:
            Dictionary of payment method types, keyed by type ID.

        Raises:
            ESBValidationError: If branch_code is empty.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            methods = client.master.get_payment_method(branch_code="BR001")
            for type_id, payment_type in methods.items():
                print(f"Type: {payment_type.payment_method_type}")
                for method in payment_type.payment_methods:
                    print(f"  - {method.payment_method_name}")
            ```
        """
        request = GetPaymentMethodRequest(filter_branch_code=branch_code)
        response = self._post(
            "/external/general/get-payment-method",
            json=request.model_dump(by_alias=True),
        )
        # Response is a dict with string keys (e.g., "1", "2")
        result: dict[str, PaymentMethodType] = {}
        if isinstance(response, dict):
            for key, value in response.items():
                if isinstance(value, dict):
                    result[key] = PaymentMethodType.model_validate(value)
        return result

    def get_branch(
        self,
        *,
        branch_name: str | None = None,
        branch_address: str | None = None,
        branch_phone: str | None = None,
        brand_id: str | None = None,
    ) -> list[Branch]:
        """Get branches/outlets.

        Retrieve a list of branches with optional filters.

        Args:
            branch_name: Optional filter by branch name.
            branch_address: Optional filter by branch address.
            branch_phone: Optional filter by branch phone.
            brand_id: Optional filter by brand ID.

        Returns:
            List of branches with business hours and visit purposes.

        Raises:
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            # Get all branches
            branches = client.master.get_branch()
            for branch in branches:
                print(f"{branch.branch_name} ({branch.branch_code})")
                print(f"  Address: {branch.address}")
                print(f"  Phone: {branch.phone}")

            # Filter by name
            branches = client.master.get_branch(branch_name="Main")
            ```
        """
        request = GetBranchRequest(
            filter_branch_name=branch_name,
            filter_branch_address=branch_address,
            filter_branch_phone=branch_phone,
            filter_brand_id=brand_id,
        )
        response = self._post(
            "/external/general/get-branch",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        adapter = TypeAdapter(list[Branch])
        return adapter.validate_python(response)
