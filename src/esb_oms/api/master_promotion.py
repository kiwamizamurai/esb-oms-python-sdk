"""Master Promotion API for ESB OMS.

This module provides APIs for creating and managing promotions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from esb_oms.api._base import BaseAPI
from esb_oms.models.promotion import (
    CreateDiscountAmountESORequest,
    CreateDiscountLimitPercentageRequest,
    CreateDiscountPercentageESORequest,
    CreateDiscountPercentageRequest,
    CreateFreeItemRequest,
    CreatePromotionResult,
    PromotionResult,
)

if TYPE_CHECKING:
    from esb_oms._http import BearerHTTPClient


class MasterPromotionAPI(BaseAPI):
    """Master Promotion API endpoints.

    This API provides operations for creating and listing promotions.
    Supports multiple promotion types including discounts, free items,
    and ESO (E-Self Order) specific promotions.

    Promotion Types:
        - Discount Percentage (Type 1): Percentage discount on items
        - Free Item (Type 4): Free items with purchase
        - Discount Percentage ESO (Type 5): ESO-specific percentage discount
        - Discount Amount ESO (Type 6): ESO-specific fixed amount discount
        - Discount Limit Percentage (Type 10): Percentage discount with maximum limit

    Example:
        ```python
        from esb_oms.models.promotion import CreateDiscountPercentageRequest
        from decimal import Decimal

        # Create a 10% discount promotion
        request = CreateDiscountPercentageRequest(
            promotion_master_code="PROMO001",
            branch_code="BR001",
            discount=Decimal("10"),
            start_date="2024-01-01",
            end_date="2024-12-31",
            all_categories=True,
        )
        result = client.promotion.create_discount_percentage(request)
        print(f"Created promotion ID: {result.promotion_id}")

        # List all promotions
        promotions = client.promotion.list(page=1)
        for promo in promotions:
            print(f"Promotion: {promo.promotion_code}")
        ```
    """

    def __init__(self, http_client: BearerHTTPClient) -> None:
        """Initialize the Master Promotion API.

        Args:
            http_client: Bearer HTTP client configured for the API URL.
        """
        super().__init__(http_client)

    def create_discount_percentage(
        self, request: CreateDiscountPercentageRequest
    ) -> CreatePromotionResult:
        """Create a Discount (%) Promotion (Type 1).

        Creates a percentage-based discount promotion that can be applied
        to all categories or specific menu items.

        Args:
            request: The promotion data to create.

        Returns:
            The created promotion result with promotion ID.

        Raises:
            ESBValidationError: If the request data is invalid.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            from esb_oms.models.promotion import (
                CreateDiscountPercentageRequest,
                PromotionTimeInput,
            )
            from decimal import Decimal

            request = CreateDiscountPercentageRequest(
                promotion_master_code="DISC10",
                branch_code="BR001",
                discount=Decimal("10"),
                start_date="2024-01-01",
                end_date="2024-12-31",
                all_categories=True,
                promotion_days_id=[1, 2, 3, 4, 5],  # Mon-Fri
                promotion_time=[
                    PromotionTimeInput(start_time="11:00", end_time="14:00"),
                ],
                promotion_code="LUNCH10",
                promotion_desc="10% lunch discount",
            )
            result = client.promotion.create_discount_percentage(request)
            ```
        """
        response = self._post(
            "/corev1/promotion/",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(response, dict):
            return CreatePromotionResult.model_validate(response.get("result", {}))
        msg = "Unexpected response format from create_discount_percentage API"
        raise TypeError(msg)

    def create_discount_limit_percentage(
        self, request: CreateDiscountLimitPercentageRequest
    ) -> CreatePromotionResult:
        """Create a Discount Limit (%) Promotion (Type 10).

        Creates a percentage-based discount promotion with a maximum
        discount limit.

        Args:
            request: The promotion data to create.

        Returns:
            The created promotion result with promotion ID.

        Raises:
            ESBValidationError: If the request data is invalid.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            from esb_oms.models.promotion import CreateDiscountLimitPercentageRequest
            from decimal import Decimal

            request = CreateDiscountLimitPercentageRequest(
                promotion_master_code="DISC20MAX",
                branch_code="BR001",
                discount=Decimal("20"),
                start_date="2024-01-01",
                end_date="2024-12-31",
                all_categories=True,
                max_sales_price=Decimal("100000"),  # Max discount limit
                promotion_code="MAX20",
                promotion_desc="20% discount up to 100k",
            )
            result = client.promotion.create_discount_limit_percentage(request)
            ```
        """
        response = self._post(
            "/corev1/promotion/",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(response, dict):
            return CreatePromotionResult.model_validate(response.get("result", {}))
        msg = "Unexpected response format from create_discount_limit_percentage API"
        raise TypeError(msg)

    def create_free_item(self, request: CreateFreeItemRequest) -> CreatePromotionResult:
        """Create a Free Item Promotion (Type 4).

        Creates a promotion that provides free items with purchase.

        Args:
            request: The promotion data to create.

        Returns:
            The created promotion result with promotion ID.

        Raises:
            ESBValidationError: If the request data is invalid.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            from esb_oms.models.promotion import CreateFreeItemRequest
            from decimal import Decimal

            request = CreateFreeItemRequest(
                promotion_master_code="FREEITEM",
                branch_code="BR001",
                start_date="2024-01-01",
                end_date="2024-12-31",
                all_categories=False,
                menu_id=[101, 102],  # Free items
                min_sales_price=Decimal("50000"),  # Minimum purchase
                max_usage=1,  # Per transaction
                promotion_code="FREEDRINK",
                promotion_desc="Free drink with purchase over 50k",
            )
            result = client.promotion.create_free_item(request)
            ```
        """
        response = self._post(
            "/corev1/promotion/",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(response, dict):
            return CreatePromotionResult.model_validate(response.get("result", {}))
        msg = "Unexpected response format from create_free_item API"
        raise TypeError(msg)

    def create_discount_percentage_eso(
        self, request: CreateDiscountPercentageESORequest
    ) -> CreatePromotionResult:
        """Create a Discount (%) ESO Promotion (Type 5).

        Creates a percentage-based discount promotion specifically for
        E-Self Order (ESO) channels.

        Args:
            request: The promotion data to create.

        Returns:
            The created promotion result with promotion ID.

        Raises:
            ESBValidationError: If the request data is invalid.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            from esb_oms.models.promotion import CreateDiscountPercentageESORequest
            from decimal import Decimal

            request = CreateDiscountPercentageESORequest(
                promotion_master_code="ESODISC",
                branch_code="BR001",
                discount=Decimal("15"),
                start_date="2024-01-01",
                end_date="2024-12-31",
                all_categories=True,
                max_discount=Decimal("50000"),
                show_promotion_ezo=True,
                promotion_code="ESO15",
                promotion_desc="15% ESO discount",
                self_order_payment_method_code=["GOPAY", "OVO"],
            )
            result = client.promotion.create_discount_percentage_eso(request)
            ```
        """
        response = self._post(
            "/corev1/promotion/",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(response, dict):
            return CreatePromotionResult.model_validate(response.get("result", {}))
        msg = "Unexpected response format from create_discount_percentage_eso API"
        raise TypeError(msg)

    def create_discount_amount_eso(
        self, request: CreateDiscountAmountESORequest
    ) -> CreatePromotionResult:
        """Create a Discount (RP) ESO Promotion (Type 6).

        Creates a fixed amount discount promotion specifically for
        E-Self Order (ESO) channels.

        Args:
            request: The promotion data to create.

        Returns:
            The created promotion result with promotion ID.

        Raises:
            ESBValidationError: If the request data is invalid.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            from esb_oms.models.promotion import CreateDiscountAmountESORequest
            from decimal import Decimal

            request = CreateDiscountAmountESORequest(
                promotion_master_code="ESORP",
                branch_code="BR001",
                discount=Decimal("10000"),  # Fixed 10k discount
                start_date="2024-01-01",
                end_date="2024-12-31",
                all_categories=True,
                min_sales_price=Decimal("50000"),
                show_promotion_ezo=True,
                promotion_code="ESO10K",
                promotion_desc="10k ESO discount for orders over 50k",
            )
            result = client.promotion.create_discount_amount_eso(request)
            ```
        """
        response = self._post(
            "/corev1/promotion/",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(response, dict):
            return CreatePromotionResult.model_validate(response.get("result", {}))
        msg = "Unexpected response format from create_discount_amount_eso API"
        raise TypeError(msg)

    def list(
        self,
        *,
        page: int = 1,
        branch_id: int | None = None,
        promotion_type: int | None = None,
    ) -> list[PromotionResult]:
        """Get promotion list.

        Retrieve a paginated list of promotions with optional filters.

        Args:
            page: Page number for pagination (default: 1).
            branch_id: Optional filter by branch ID.
            promotion_type: Optional filter by promotion type.

        Returns:
            List of promotions matching the filters.

        Raises:
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            # Get all promotions
            promotions = client.promotion.list(page=1)
            for promo in promotions:
                print(f"{promo.promotion_code}: {promo.discount}%")
                print(f"  Valid: {promo.start_date} - {promo.end_date}")

            # Filter by branch
            promotions = client.promotion.list(branch_id=1)

            # Filter by promotion type
            from esb_oms.models.promotion import PromotionType
            promotions = client.promotion.list(
                promotion_type=PromotionType.DISCOUNT_PERCENTAGE
            )
            ```
        """
        params: dict[str, Any] = {"page": page}
        if branch_id is not None:
            params["branchID"] = branch_id
        if promotion_type is not None:
            params["promotionType"] = promotion_type

        response = self._get("/extv1/promotion", params=params)
        if isinstance(response, dict):
            result = response.get("result", [])
            if isinstance(result, dict):
                # Handle paginated response
                data = result.get("data", [])
                return [PromotionResult.model_validate(item) for item in data]
            if isinstance(result, list):
                return [PromotionResult.model_validate(item) for item in result]
        return []
