"""Sales API for ESB OMS."""

from __future__ import annotations

from typing import TYPE_CHECKING

from esb_oms.api._base import BaseAPI
from esb_oms.models.sales import (
    PushSalesDataRequest,
    PushSalesDataResult,
    PushShiftDataRequest,
    PushShiftDataResult,
    SalesHead,
    ShiftData,
)

if TYPE_CHECKING:
    from esb_oms._http import BearerHTTPClient


class SalesAPI(BaseAPI):
    """Sales API endpoints.

    This API handles pushing sales data and shift data to ESB Core.

    Example:
        ```python
        # Push sales data
        result = client.sales.push_sales_data(sales_head=data)
        print(f"Sales ID: {result.sales_id}")

        # Push shift data
        result = client.sales.push_shift_data(shift_data=shift)
        print(f"Shift ID: {result.shift_id}")
        ```
    """

    def __init__(self, http_client: BearerHTTPClient) -> None:
        """Initialize the Sales API.

        Args:
            http_client: Bearer HTTP client configured for the API URL.
        """
        super().__init__(http_client)

    def push_sales_data(self, sales_head: SalesHead) -> PushSalesDataResult:
        """Push sales data to ESB Core (V2).

        Send a sales transaction to ESB Core backend. If a transaction
        with the same salesNum already exists, it will be overwritten.

        Args:
            sales_head: The sales transaction data to push.

        Returns:
            Result containing the created/updated sales ID and number.

        Raises:
            ESBValidationError: If the sales data is invalid.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            from esb_oms.models.sales import SalesHead, SalesMenuItem, Payment
            from decimal import Decimal

            menu_item = SalesMenuItem(
                menu_id=1,
                menu_code="MENU001",
                qty=2,
                original_price=Decimal("50000"),
                price=Decimal("50000"),
                total=Decimal("100000"),
                created_by="cashier1",
                created_date="2024-01-15 12:00:00",
            )

            payment = Payment(
                payment_method="Cash",
                amount=Decimal("100000"),
            )

            sales_head = SalesHead(
                sales_num="S001",
                sales_date="2024-01-15",
                sales_date_in="2024-01-15 12:00:00",
                branch_code="BR001",
                subtotal=Decimal("100000"),
                grand_total=Decimal("100000"),
                payment_total=Decimal("100000"),
                created_by="cashier1",
                menu=[menu_item],
                payment=[payment],
            )

            result = client.sales.push_sales_data(sales_head=sales_head)
            print(f"Sales ID: {result.sales_id}")
            ```
        """
        request = PushSalesDataRequest(sales_head=sales_head)
        response = self._post(
            "/extv1/push/sales-data",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(response, dict):
            return PushSalesDataResult.model_validate(response["result"])
        msg = "Unexpected response format from push_sales_data API"
        raise TypeError(msg)

    def push_shift_data(self, shift_data: ShiftData) -> PushShiftDataResult:
        """Push shift data to ESB Core (V2).

        Send shift/cashier session data to ESB Core backend.

        Args:
            shift_data: The shift data to push.

        Returns:
            Result containing the created shift ID and number.

        Raises:
            ESBValidationError: If the shift data is invalid.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            from esb_oms.models.sales import ShiftData
            from decimal import Decimal

            shift = ShiftData(
                branch_code="BR001",
                shift_num="SHIFT001",
                shift_date="2024-01-15",
                shift_start="2024-01-15 08:00:00",
                cashier_name="John Doe",
                opening_cash=Decimal("500000"),
                created_by="manager1",
            )

            result = client.sales.push_shift_data(shift_data=shift)
            print(f"Shift ID: {result.shift_id}")
            ```
        """
        request = PushShiftDataRequest(shift_data=shift_data)
        response = self._post(
            "/extv1/push/shift-data",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(response, dict):
            return PushShiftDataResult.model_validate(response["result"])
        msg = "Unexpected response format from push_shift_data API"
        raise TypeError(msg)

    def push_sales_data_v1(self, sales_head: SalesHead) -> PushSalesDataResult:
        """Push sales data to ESB Core (V1 - Legacy).

        This is the legacy V1 endpoint. Use push_sales_data() for V2.

        Args:
            sales_head: The sales transaction data to push.

        Returns:
            Result containing the created/updated sales ID and number.

        Raises:
            ESBValidationError: If the sales data is invalid.
            ESBAuthenticationError: If authentication fails.
        """
        request = PushSalesDataRequest(sales_head=sales_head)
        response = self._post(
            "/ext/push/sales-data",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(response, dict):
            return PushSalesDataResult.model_validate(response["result"])
        msg = "Unexpected response format from push_sales_data_v1 API"
        raise TypeError(msg)

    def push_shift_data_v1(self, shift_data: ShiftData) -> PushShiftDataResult:
        """Push shift data to ESB Core (V1 - Legacy).

        This is the legacy V1 endpoint. Use push_shift_data() for V2.

        Args:
            shift_data: The shift data to push.

        Returns:
            Result containing the created shift ID and number.

        Raises:
            ESBValidationError: If the shift data is invalid.
            ESBAuthenticationError: If authentication fails.
        """
        request = PushShiftDataRequest(shift_data=shift_data)
        response = self._post(
            "/ext/push/shift-data",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(response, dict):
            return PushShiftDataResult.model_validate(response["result"])
        msg = "Unexpected response format from push_shift_data_v1 API"
        raise TypeError(msg)
