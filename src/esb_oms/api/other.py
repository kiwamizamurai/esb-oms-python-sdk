"""Other API for ESB OMS.

This module provides miscellaneous utility APIs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import TypeAdapter

from esb_oms.api._base import BaseAPI
from esb_oms.models.other import (
    BranchSalesSummaryItem,
    BranchSalesSummaryRequest,
    DailySalesMaterialUsageItem,
    GetSalesRequest,
    SalesDetailItem,
)

if TYPE_CHECKING:
    from esb_oms._http import BasicAuthHTTPClient, BearerHTTPClient


class OtherAPI(BaseAPI):
    """Other utility API endpoints.

    This API provides miscellaneous utility operations including:
    - Branch sales summaries
    - Daily material usage reports
    - Individual sales lookup

    Different endpoints use different authentication methods:
    - Branch Sales Summary: Basic Auth (Master POS URL)
    - Daily Sales Material Usage: Bearer Token (API URL)
    - Get Sales: Basic Auth (Master POS URL)

    Example:
        ```python
        # Get branch sales summary
        summaries = client.other.get_branch_sales_summary(
            sales_date_from="2024-01-01",
            sales_date_to="2024-01-31",
        )
        for summary in summaries:
            print(f"{summary.branch_name}: {summary.grand_total}")

        # Get daily material usage
        usage = client.other.get_daily_material_usage(
            sales_date="2024-01-01",
            flag_unit="stockUnit",
            branch_code="BR001",
        )
        for item in usage:
            print(f"{item.product_name}: {item.total_qty} {item.unit}")
        ```
    """

    def __init__(
        self,
        api_http: BearerHTTPClient,
        master_pos_http: BasicAuthHTTPClient,
    ) -> None:
        """Initialize the Other API.

        Args:
            api_http: Bearer HTTP client for API URL endpoints.
            master_pos_http: Basic Auth HTTP client for Master POS URL endpoints.
        """
        super().__init__(api_http)
        self._master_pos_http = master_pos_http

    def get_branch_sales_summary(
        self,
        *,
        sales_date_from: str,
        sales_date_to: str,
        sales_type: str | None = None,
    ) -> list[BranchSalesSummaryItem]:
        """Get branch sales summary.

        Retrieve sales summary grouped by branch for a date range.
        Uses Basic Auth on Master POS URL.

        Args:
            sales_date_from: Start date filter (YYYY-MM-DD).
            sales_date_to: End date filter (YYYY-MM-DD).
            sales_type: Optional filter by sales type ("Sales" or "Non Sales").

        Returns:
            List of branch sales summary items.

        Raises:
            ESBValidationError: If date parameters are missing or sales_type is invalid.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            summaries = client.other.get_branch_sales_summary(
                sales_date_from="2024-01-01",
                sales_date_to="2024-01-31",
                sales_type="Sales",
            )
            for summary in summaries:
                print(f"Branch: {summary.branch_name}")
                print(f"  Date: {summary.sales_date}")
                print(f"  Bills: {summary.bill_total}")
                print(f"  Pax: {summary.pax_total}")
                print(f"  Subtotal: {summary.subtotal}")
                print(f"  Discount: {summary.discount_total}")
                print(f"  Service Charge: {summary.sc_total}")
                print(f"  Tax: {summary.tax_total}")
                print(f"  Grand Total: {summary.grand_total}")
            ```
        """
        request = BranchSalesSummaryRequest(
            filter_sales_date_from=sales_date_from,
            filter_sales_date_to=sales_date_to,
            sales_type=sales_type,
        )
        response = self._master_pos_http.post(
            "/external/general/sales-branch-summary",
            json=request.model_dump(by_alias=True, exclude_none=True),
            headers={"Content-Type": "application/json"},
        )
        if isinstance(response, list):
            adapter = TypeAdapter(list[BranchSalesSummaryItem])
            return adapter.validate_python(response)
        return []

    def get_daily_material_usage(
        self,
        *,
        sales_date: str,
        flag_unit: str,
        branch_code: str | None = None,
    ) -> list[DailySalesMaterialUsageItem]:
        """Get daily sales material usage.

        Retrieve material usage based on sales transactions.
        Uses Bearer Token on API URL.

        Args:
            sales_date: Sales date filter (YYYY-MM-DD).
            flag_unit: Unit conversion flag. Valid values:
                - "stockUnit"
                - "purchaseUnit"
                - "baseUnit"
                - "transferUnit"
                - "salesUnit"
            branch_code: Optional filter by branch code.

        Returns:
            List of daily material usage items.

        Raises:
            ESBValidationError: If required parameters are missing or invalid.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            usage = client.other.get_daily_material_usage(
                sales_date="2024-01-01",
                flag_unit="stockUnit",
                branch_code="BR001",
            )
            for item in usage:
                print(f"Product: {item.product_name} ({item.product_code})")
                print(f"  Branch: {item.branch}")
                print(f"  Qty: {item.total_qty} {item.unit}")
                print(f"  Conversion: {item.total_conversion_qty}")
            ```
        """
        params: dict[str, Any] = {
            "salesDate": sales_date,
            "flagUnit": flag_unit,
        }
        if branch_code is not None:
            params["branchCode"] = branch_code

        response = self._get(
            "/corev1/sales/get-daily-sales-material-usage",
            params=params,
        )
        # Response can be a list directly or wrapped in result
        if isinstance(response, list):
            adapter = TypeAdapter(list[DailySalesMaterialUsageItem])
            return adapter.validate_python(response)
        result = response.get("result", [])
        if isinstance(result, list):
            adapter = TypeAdapter(list[DailySalesMaterialUsageItem])
            return adapter.validate_python(result)
        return []

    def get_sales(
        self,
        *,
        bill_num: str | None = None,
        sales_num: str | None = None,
    ) -> list[SalesDetailItem]:
        """Get specific sales by bill number or sales number.

        Retrieve detailed sales information for a specific transaction.
        Uses Basic Auth on Master POS URL.

        At least one of bill_num or sales_num must be provided.

        Args:
            bill_num: Optional filter by bill number.
            sales_num: Optional filter by sales number.

        Returns:
            List of sales detail items (usually single item).

        Raises:
            ESBValidationError: If neither bill_num nor sales_num is provided,
                or if the values don't match any transaction.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            # Get by bill number
            sales = client.other.get_sales(bill_num="MOOD202301050001")

            # Get by sales number
            sales = client.other.get_sales(sales_num="SMOOD167291257329")

            for sale in sales:
                print(f"Sales: {sale.sales_num}")
                print(f"Bill: {sale.bill_num}")
                print(f"Date: {sale.sales_date}")
                print(f"Branch: {sale.branch_name}")
                print(f"Status: {sale.status_name}")
                print(f"Grand Total: {sale.grand_total}")
                print(f"Payment Total: {sale.payment_total}")

                print("Payments:")
                for payment in sale.sales_payments:
                    print(f"  {payment.payment_method_name}: {payment.payment_amount}")

                print("Menus:")
                for menu in sale.sales_menus:
                    print(f"  {menu.menu_name} x{menu.qty}: {menu.total}")
            ```
        """
        if bill_num is None and sales_num is None:
            msg = "At least one of bill_num or sales_num must be provided"
            raise ValueError(msg)

        request = GetSalesRequest(
            bill_num=bill_num,
            sales_num=sales_num,
        )
        response = self._master_pos_http.post(
            "/external/general/get-sales",
            json=request.model_dump(by_alias=True, exclude_none=True),
            headers={"Content-Type": "application/json"},
        )
        if isinstance(response, list):
            adapter = TypeAdapter(list[SalesDetailItem])
            return adapter.validate_python(response)
        return []
