"""Report API for ESB OMS.

This module provides APIs for retrieving sales reports and summaries.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import TypeAdapter

from esb_oms.api._base import BaseAPI
from esb_oms.models.report import (
    SalesHeadItem,
    SalesHeadRequest,
    SalesInformationItem,
    SalesMenuCompletionItem,
    SalesMenuCompletionRequest,
    SalesMenuReportItem,
    SalesMenuRequest,
    SalesMenuSummaryResult,
    SalesPaymentSummaryItem,
)

if TYPE_CHECKING:
    from esb_oms._http import BasicAuthHTTPClient, BearerHTTPClient


class ReportAPI(BaseAPI):
    """Report API endpoints.

    This API provides operations for retrieving sales reports and summaries.
    Different endpoints use different authentication methods and base URLs:

    - Sales Head: Basic Auth (Master POS URL)
    - Sales Information: Bearer Token (API URL)
    - Sales Menu Completion: Basic Auth (Master POS URL)
    - Sales Menu Summary: Bearer Token (API URL)
    - Sales Menu: Basic Auth (Master POS URL)
    - Sales Payment Summary: Bearer Token (Core URL)

    Example:
        ```python
        # Get sales information
        sales = client.report.get_sales_information(
            sales_date_from="2024-01-01",
            sales_date_to="2024-01-31",
            branch_code="BR001",
        )
        for sale in sales:
            print(f"Sales: {sale.sales_num} - {sale.grand_total}")

        # Get sales menu summary
        summary = client.report.get_sales_menu_summary(
            sales_date="2024-01-01",
            branch_code="BR001",
        )
        if summary:
            for menu in summary.menus:
                print(f"{menu.menu_name}: {menu.qty}")
        ```
    """

    def __init__(
        self,
        api_http: BearerHTTPClient,
        master_pos_http: BasicAuthHTTPClient,
        core_bearer_http: BearerHTTPClient,
    ) -> None:
        """Initialize the Report API.

        Args:
            api_http: Bearer HTTP client for API URL endpoints.
            master_pos_http: Basic Auth HTTP client for Master POS URL endpoints.
            core_bearer_http: Bearer HTTP client for Core URL endpoints.
        """
        super().__init__(api_http)
        self._master_pos_http = master_pos_http
        self._core_bearer_http = core_bearer_http

    def get_sales_head(
        self,
        *,
        sales_date_from: str,
        sales_date_to: str,
        branch_code: str | None = None,
        bill_num: str | None = None,
        sales_num: str | None = None,
        page: int = 1,
    ) -> list[SalesHeadItem]:
        """Get sales head transactions.

        Retrieve a paginated list of sales head transactions.
        Uses Basic Auth on Master POS URL.

        Args:
            sales_date_from: Start date filter (YYYY-MM-DD).
            sales_date_to: End date filter (YYYY-MM-DD).
            branch_code: Optional filter by branch code.
            bill_num: Optional filter by bill number.
            sales_num: Optional filter by sales number.
            page: Page number for pagination (default: 1).

        Returns:
            List of sales head items.

        Raises:
            ESBValidationError: If date parameters are missing.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            sales_heads = client.report.get_sales_head(
                sales_date_from="2024-01-01",
                sales_date_to="2024-01-31",
                branch_code="BR001",
            )
            for head in sales_heads:
                print(f"Sales: {head.sales_num}")
                print(f"  Total: {head.grand_total}")
                print(f"  Status: {head.status_name}")
            ```
        """
        request = SalesHeadRequest(
            filter_sales_date_from=sales_date_from,
            filter_sales_date_to=sales_date_to,
            filter_branch_code=branch_code,
            filter_bill_num=bill_num,
            filter_sales_num=sales_num,
        )
        response = self._master_pos_http.post(
            "/external/general/sales-head",
            params={"page": page},
            json=request.model_dump(by_alias=True, exclude_none=True),
            headers={"Content-Type": "application/json"},
        )
        if isinstance(response, list):
            adapter = TypeAdapter(list[SalesHeadItem])
            return adapter.validate_python(response)
        return []

    def get_sales_information(
        self,
        *,
        sales_date_from: str,
        sales_date_to: str,
        branch_code: str | None = None,
        sales_num: str | None = None,
        bill_num: str | None = None,
        self_order_id: str | None = None,
        status_name: str | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        ext_branch_code: str | None = None,
        page: int = 1,
    ) -> list[SalesInformationItem]:
        """Get sales information.

        Retrieve sales data synced from ESB local POS systems.
        Uses Bearer Token on API URL.

        Args:
            sales_date_from: Start date filter (YYYY-MM-DD).
            sales_date_to: End date filter (YYYY-MM-DD).
            branch_code: Optional filter by branch code.
            sales_num: Optional filter by exact sales number.
            bill_num: Optional filter by exact bill number.
            self_order_id: Optional filter by ESB Order ID.
            status_name: Optional filter by status (New, Finished, Cancelled, Void).
            sort_by: Optional sort field (salesDateIn, salesDateOut, memberCode).
            sort_order: Optional sort order (asc, desc).
            ext_branch_code: Optional filter by external branch code.
            page: Page number for pagination (default: 1).

        Returns:
            List of sales information items.

        Raises:
            ESBValidationError: If date parameters are missing.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            sales = client.report.get_sales_information(
                sales_date_from="2024-01-01",
                sales_date_to="2024-01-31",
                branch_code="BR001",
                status_name="Finished",
                sort_by="salesDateIn",
                sort_order="desc",
            )
            for sale in sales:
                print(f"Sales: {sale.sales_num}")
                print(f"  Date: {sale.sales_date}")
                print(f"  Total: {sale.grand_total}")
                print(f"  Payment: {sale.payment_total}")
            ```
        """
        params: dict[str, Any] = {
            "salesDateFrom": sales_date_from,
            "salesDateTo": sales_date_to,
            "page": page,
        }
        if branch_code is not None:
            params["branchCode"] = branch_code
        if sales_num is not None:
            params["salesNum"] = sales_num
        if bill_num is not None:
            params["billNum"] = bill_num
        if self_order_id is not None:
            params["selfOrderID"] = self_order_id
        if status_name is not None:
            params["statusName"] = status_name
        if sort_by is not None:
            params["sortBy"] = sort_by
        if sort_order is not None:
            params["sortOrder"] = sort_order
        if ext_branch_code is not None:
            params["extBranchCode"] = ext_branch_code

        response = self._get("/corev1/sales/sales-information", params=params)
        if isinstance(response, dict):
            result = response.get("result", [])
            if isinstance(result, list):
                adapter = TypeAdapter(list[SalesInformationItem])
                return adapter.validate_python(result)
        return []

    def get_sales_menu_completion(
        self,
        *,
        sales_date_from: str,
        sales_date_to: str,
        branch_code: str | None = None,
        page: int = 1,
    ) -> list[SalesMenuCompletionItem]:
        """Get sales menu completion.

        Retrieve sales menu completion data.
        Uses Basic Auth on Master POS URL.

        Args:
            sales_date_from: Start date filter (YYYY-MM-DD).
            sales_date_to: End date filter (YYYY-MM-DD).
            branch_code: Optional filter by branch code.
            page: Page number for pagination (default: 1).

        Returns:
            List of sales menu completion items.

        Raises:
            ESBValidationError: If date parameters are missing.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            completions = client.report.get_sales_menu_completion(
                sales_date_from="2024-01-01",
                sales_date_to="2024-01-31",
                branch_code="BR001",
            )
            for item in completions:
                print(f"Menu: {item.menu}")
                print(f"  Kitchen: {item.kitchen_qty} / {item.kitchen_process}")
                print(f"  Checker: {item.checker_qty} / {item.checker_process}")
            ```
        """
        request = SalesMenuCompletionRequest(
            filter_sales_date_from=sales_date_from,
            filter_sales_date_to=sales_date_to,
            filter_branch_code=branch_code,
        )
        response = self._master_pos_http.post(
            "/external/general/sales-menu-completion",
            params={"page": page},
            json=request.model_dump(by_alias=True, exclude_none=True),
            headers={"Content-Type": "application/json"},
        )
        if isinstance(response, list):
            adapter = TypeAdapter(list[SalesMenuCompletionItem])
            return adapter.validate_python(response)
        return []

    def get_sales_menu_summary(
        self,
        *,
        sales_date: str,
        branch_code: str | None = None,
    ) -> SalesMenuSummaryResult | None:
        """Get sales menu summary.

        Retrieve a summary of menus sold on a specific date and branch.
        Uses Bearer Token on API URL.

        Args:
            sales_date: Sales date filter (YYYY-MM-DD).
            branch_code: Optional filter by branch code.

        Returns:
            Sales menu summary result or None if no data.

        Raises:
            ESBValidationError: If date parameter is missing.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            summary = client.report.get_sales_menu_summary(
                sales_date="2024-01-01",
                branch_code="BR001",
            )
            if summary:
                print(f"Date: {summary.sales_date}")
                print(f"Branch: {summary.branch_name}")
                for menu in summary.menus:
                    print(f"  {menu.menu_name}: {menu.qty} = {menu.total}")
            ```
        """
        params: dict[str, Any] = {"salesDate": sales_date}
        if branch_code is not None:
            params["branchCode"] = branch_code

        response = self._get("/extv1/sales/sales-menu-summary/", params=params)
        if isinstance(response, dict):
            data = response.get("data")
            if data:
                return SalesMenuSummaryResult.model_validate(data)
        return None

    def get_sales_menu(
        self,
        *,
        sales_date_from: str,
        sales_date_to: str,
        branch_code: str | None = None,
        sales_num: str | None = None,
        page: int = 1,
    ) -> list[SalesMenuReportItem]:
        """Get sales menu data.

        Retrieve all menu transaction data.
        Uses Basic Auth on Master POS URL.

        Args:
            sales_date_from: Start date filter (YYYY-MM-DD).
            sales_date_to: End date filter (YYYY-MM-DD).
            branch_code: Optional filter by branch code.
            sales_num: Optional filter by sales number.
            page: Page number for pagination (default: 1).

        Returns:
            List of sales menu report items.

        Raises:
            ESBValidationError: If date parameters are missing.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            menus = client.report.get_sales_menu(
                sales_date_from="2024-01-01",
                sales_date_to="2024-01-31",
                branch_code="BR001",
            )
            for menu in menus:
                print(f"Menu: {menu.menu_name}")
                print(f"  Qty: {menu.qty}, Total: {menu.total}")
            ```
        """
        request = SalesMenuRequest(
            filter_sales_date_from=sales_date_from,
            filter_sales_date_to=sales_date_to,
            filter_branch_code=branch_code,
            filter_sales_num=sales_num,
        )
        response = self._master_pos_http.post(
            "/external/general/sales-menu",
            params={"page": page},
            json=request.model_dump(by_alias=True, exclude_none=True),
            headers={"Content-Type": "application/json"},
        )
        if isinstance(response, list):
            adapter = TypeAdapter(list[SalesMenuReportItem])
            return adapter.validate_python(response)
        return []

    def get_sales_payment_summary(
        self,
        *,
        sales_date: str,
        branch_code: str | None = None,
        page: int = 1,
    ) -> list[SalesPaymentSummaryItem]:
        """Get sales payment summary.

        Retrieve payment summary grouped by payment method.
        Uses Bearer Token on Core URL.

        Args:
            sales_date: Sales date filter (YYYY-MM-DD).
            branch_code: Optional filter by branch code.
            page: Page number for pagination (default: 1).

        Returns:
            List of sales payment summary items.

        Raises:
            ESBValidationError: If date parameter is missing.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            summaries = client.report.get_sales_payment_summary(
                sales_date="2024-01-01",
                branch_code="BR001",
            )
            for summary in summaries:
                print(f"Branch: {summary.branch_name}")
                for payment in summary.payments:
                    print(f"  {payment.payment_method_name}:")
                    print(f"    Count: {payment.payment_count}")
                    print(f"    Amount: {payment.payment_amount}")
                    print(f"    Net: {payment.net_after_mdr}")
            ```
        """
        params: dict[str, Any] = {"salesDate": sales_date, "page": page}
        if branch_code is not None:
            params["branchCode"] = branch_code

        response = self._core_bearer_http.get(
            "/report/sales-payment-summary",
            params=params,
            headers={"Content-Type": "application/json"},
        )
        if isinstance(response, dict):
            result = response.get("result", [])
            if isinstance(result, list):
                adapter = TypeAdapter(list[SalesPaymentSummaryItem])
                return adapter.validate_python(result)
        return []
