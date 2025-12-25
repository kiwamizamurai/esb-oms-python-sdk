"""Promotion models for ESB OMS API."""

from __future__ import annotations

from decimal import Decimal
from enum import IntEnum

from pydantic import Field

from esb_oms.models.common import ESBBaseModel


class PromotionType(IntEnum):
    """Promotion type enum."""

    DISCOUNT_PERCENTAGE = 1
    FREE_ITEM = 4
    DISCOUNT_PERCENTAGE_ESO = 5
    DISCOUNT_AMOUNT_ESO = 6
    DISCOUNT_LIMIT_PERCENTAGE = 10


class ApplyDiscountTo(IntEnum):
    """Apply discount to target enum."""

    MENU_CATEGORY = 1
    MENU_CATEGORY_DETAIL = 2
    MENU = 3


class PromotionDay(IntEnum):
    """Promotion day enum."""

    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class ApplyTo(IntEnum):
    """Apply to target enum."""

    ALL_TRANSACTION = 1
    MEMBER_AND_STAFF = 2
    STAFF_ONLY = 3
    MEMBER_ONLY = 4


class PromotionTimeInput(ESBBaseModel):
    """Promotion time window input."""

    start_time: str = Field(..., alias="startTime")
    end_time: str = Field(..., alias="endTime")


class CreateDiscountPercentageRequest(ESBBaseModel):
    """Request body for Create Discount (%) Promotion API."""

    promotion_master_code: str = Field(..., alias="promotionMasterCode")
    branch_code: str = Field(..., alias="branchCode")
    promotion_type: int = Field(
        PromotionType.DISCOUNT_PERCENTAGE, alias="promotionType"
    )
    notes: str = ""
    discount: Decimal
    authorization_needed: bool = Field(False, alias="authorizationNeeded")
    promotion_days_id: list[int] = Field(default_factory=list, alias="promotionDaysID")
    start_date: str = Field(..., alias="startDate")
    end_date: str = Field(..., alias="endDate")
    min_sales_price: Decimal = Field(Decimal("0"), alias="minSalesPrice")
    all_categories: bool = Field(True, alias="allCategories")
    apply_discount_to: int | None = Field(default=None, alias="applyDiscountTo")
    menu_category_id: list[int] = Field(default_factory=list, alias="menuCategoryID")
    menu_category_detail_id: list[int] = Field(
        default_factory=list, alias="menuCategoryDetailID"
    )
    menu_id: list[int] = Field(default_factory=list, alias="menuID")
    max_sales_price: Decimal | None = Field(default=None, alias="maxSalesPrice")
    used_for_loyalty: bool = Field(False, alias="usedForLoyalty")
    apply_to: int | None = Field(default=None, alias="applyTo")
    employee_group_name: list[str] = Field(
        default_factory=list, alias="employeeGroupName"
    )
    include_package_content: bool = Field(False, alias="includePackageContent")
    include_menu_extra: bool = Field(False, alias="includeMenuExtra")
    promotion_time: list[PromotionTimeInput] = Field(
        default_factory=list, alias="promotionTime"
    )
    promotion_code: str = Field("", alias="promotionCode")
    promotion_desc: str = Field("", alias="promotionDesc")
    payment_method_name: str | None = Field(default=None, alias="paymentMethodName")


class CreateDiscountLimitPercentageRequest(ESBBaseModel):
    """Request body for Create Discount Limit (%) Promotion API."""

    promotion_master_code: str = Field(..., alias="promotionMasterCode")
    branch_code: str = Field(..., alias="branchCode")
    promotion_type: int = Field(
        PromotionType.DISCOUNT_LIMIT_PERCENTAGE, alias="promotionType"
    )
    notes: str = ""
    discount: Decimal
    authorization_needed: bool = Field(False, alias="authorizationNeeded")
    promotion_days_id: list[int] = Field(default_factory=list, alias="promotionDaysID")
    start_date: str = Field(..., alias="startDate")
    end_date: str = Field(..., alias="endDate")
    min_sales_price: Decimal = Field(Decimal("0"), alias="minSalesPrice")
    all_categories: bool = Field(True, alias="allCategories")
    apply_discount_to: int | None = Field(default=None, alias="applyDiscountTo")
    menu_category_id: list[int] = Field(default_factory=list, alias="menuCategoryID")
    menu_category_detail_id: list[int] = Field(
        default_factory=list, alias="menuCategoryDetailID"
    )
    menu_id: list[int] = Field(default_factory=list, alias="menuID")
    max_sales_price: Decimal | None = Field(default=None, alias="maxSalesPrice")
    used_for_loyalty: bool = Field(False, alias="usedForLoyalty")
    apply_to: int | None = Field(default=None, alias="applyTo")
    employee_group_name: list[str] = Field(
        default_factory=list, alias="employeeGroupName"
    )
    include_package_content: bool = Field(False, alias="includePackageContent")
    include_menu_extra: bool = Field(False, alias="includeMenuExtra")
    promotion_time: list[PromotionTimeInput] = Field(
        default_factory=list, alias="promotionTime"
    )
    promotion_code: str = Field("", alias="promotionCode")
    promotion_desc: str = Field("", alias="promotionDesc")
    payment_method_name: str | None = Field(default=None, alias="paymentMethodName")


class CreateFreeItemRequest(ESBBaseModel):
    """Request body for Create Free Item Promotion API."""

    promotion_master_code: str = Field(..., alias="promotionMasterCode")
    branch_code: str = Field(..., alias="branchCode")
    promotion_type: int = Field(PromotionType.FREE_ITEM, alias="promotionType")
    notes: str = ""
    authorization_needed: bool = Field(False, alias="authorizationNeeded")
    promotion_days_id: list[int] = Field(default_factory=list, alias="promotionDaysID")
    start_date: str = Field(..., alias="startDate")
    end_date: str = Field(..., alias="endDate")
    all_categories: bool = Field(True, alias="allCategories")
    apply_discount_to: int | None = Field(default=None, alias="applyDiscountTo")
    menu_category_id: list[int] = Field(default_factory=list, alias="menuCategoryID")
    menu_category_detail_id: list[int] = Field(
        default_factory=list, alias="menuCategoryDetailID"
    )
    menu_id: list[int] = Field(default_factory=list, alias="menuID")
    used_for_loyalty: bool = Field(False, alias="usedForLoyalty")
    apply_to: int | None = Field(default=None, alias="applyTo")
    employee_group_name: list[str] = Field(
        default_factory=list, alias="employeeGroupName"
    )
    apply_to_application_id: list[str] = Field(
        default_factory=list, alias="applyToApplicationID"
    )
    self_order_payment_method_code: list[str] = Field(
        default_factory=list, alias="selfOrderPaymentMethodCode"
    )
    max_usage: int | None = Field(default=None, alias="maxUsage")
    max_usage_total: int | None = Field(default=None, alias="maxUsageTotal")
    visit_purpose_id: list[int] = Field(default_factory=list, alias="visitPurposeID")
    promotion_time: list[PromotionTimeInput] = Field(
        default_factory=list, alias="promotionTime"
    )
    promotion_code: str = Field("", alias="promotionCode")
    promotion_desc: str = Field("", alias="promotionDesc")
    payment_method_name: str | None = Field(default=None, alias="paymentMethodName")
    voucher_source_name: str | None = Field(default=None, alias="voucherSourceName")
    min_sales_price: Decimal | None = Field(default=None, alias="minSalesPrice")
    prefix_promotion: str | None = Field(default=None, alias="prefixPromotion")


class CreateDiscountPercentageESORequest(ESBBaseModel):
    """Request body for Create Discount (%) ESO Promotion API."""

    promotion_master_code: str = Field(..., alias="promotionMasterCode")
    branch_code: str = Field(..., alias="branchCode")
    promotion_type: int = Field(
        PromotionType.DISCOUNT_PERCENTAGE_ESO, alias="promotionType"
    )
    notes: str = ""
    discount: Decimal
    promotion_days_id: list[int] = Field(default_factory=list, alias="promotionDaysID")
    start_date: str = Field(..., alias="startDate")
    end_date: str = Field(..., alias="endDate")
    all_categories: bool = Field(True, alias="allCategories")
    apply_discount_to: int | None = Field(default=None, alias="applyDiscountTo")
    menu_category_id: list[int] = Field(default_factory=list, alias="menuCategoryID")
    menu_category_detail_id: list[int] = Field(
        default_factory=list, alias="menuCategoryDetailID"
    )
    menu_id: list[int] = Field(default_factory=list, alias="menuID")
    min_sales_price: Decimal = Field(Decimal("0"), alias="minSalesPrice")
    max_discount: Decimal | None = Field(default=None, alias="maxDiscount")
    used_for_loyalty: bool = Field(False, alias="usedForLoyalty")
    promotion_code: str = Field("", alias="promotionCode")
    promotion_desc: str = Field("", alias="promotionDesc")
    show_promotion_ezo: bool = Field(False, alias="showPromotionEzo")
    max_usage: int | None = Field(default=None, alias="maxUsage")
    max_usage_total: int | None = Field(default=None, alias="maxUsageTotal")
    payment_method_name: str | None = Field(default=None, alias="paymentMethodName")
    visit_purpose_id: list[int] = Field(default_factory=list, alias="visitPurposeID")
    self_order_payment_method_code: list[str] = Field(
        default_factory=list, alias="selfOrderPaymentMethodCode"
    )
    bank_identification_numbers: list[int] = Field(
        default_factory=list, alias="bankIdentificationNumbers"
    )


class CreateDiscountAmountESORequest(ESBBaseModel):
    """Request body for Create Discount (RP) ESO Promotion API."""

    promotion_master_code: str = Field(..., alias="promotionMasterCode")
    branch_code: str = Field(..., alias="branchCode")
    promotion_type: int = Field(
        PromotionType.DISCOUNT_AMOUNT_ESO, alias="promotionType"
    )
    notes: str = ""
    discount: Decimal
    promotion_days_id: list[int] = Field(default_factory=list, alias="promotionDaysID")
    start_date: str = Field(..., alias="startDate")
    end_date: str = Field(..., alias="endDate")
    min_sales_price: Decimal = Field(Decimal("0"), alias="minSalesPrice")
    all_categories: bool = Field(True, alias="allCategories")
    apply_discount_to: int | None = Field(default=None, alias="applyDiscountTo")
    menu_category_id: list[int] = Field(default_factory=list, alias="menuCategoryID")
    menu_category_detail_id: list[int] = Field(
        default_factory=list, alias="menuCategoryDetailID"
    )
    menu_id: list[int] = Field(default_factory=list, alias="menuID")
    used_for_loyalty: bool = Field(False, alias="usedForLoyalty")
    promotion_code: str = Field("", alias="promotionCode")
    promotion_desc: str = Field("", alias="promotionDesc")
    show_promotion_ezo: bool = Field(False, alias="showPromotionEzo")
    max_usage: int | None = Field(default=None, alias="maxUsage")
    max_usage_total: int | None = Field(default=None, alias="maxUsageTotal")
    payment_method_name: str | None = Field(default=None, alias="paymentMethodName")
    visit_purpose_id: list[int] = Field(default_factory=list, alias="visitPurposeID")
    self_order_payment_method_code: list[str] = Field(
        default_factory=list, alias="selfOrderPaymentMethodCode"
    )
    bank_identification_numbers: list[int] = Field(
        default_factory=list, alias="bankIdentificationNumbers"
    )


class CreatePromotionResult(ESBBaseModel):
    """Result from creating a promotion."""

    promotion_id: int = Field(..., alias="promotionID")
    notes: str = ""


class CreatePromotionResponse(ESBBaseModel):
    """Response data for Create Promotion API."""

    path: str = ""
    code: int = 200
    timestamp: str = ""
    message: str = ""
    data: CreatePromotionResult | None = None


class PromotionCategoryResult(ESBBaseModel):
    """Promotion category item in response."""

    menu_category_id: int | None = Field(default=None, alias="menuCategoryID")
    menu_category_detail_id: int | None = Field(
        default=None, alias="menuCategoryDetailID"
    )
    menu_id: int | None = Field(default=None, alias="menuID")


class PromotionBranchResult(ESBBaseModel):
    """Promotion branch item in response."""

    branch_id: int = Field(..., alias="branchID")
    branch_code: str = Field("", alias="branchCode")
    branch_name: str = Field("", alias="branchName")


class SelfOrderPaymentMethodResult(ESBBaseModel):
    """Self order payment method in response."""

    self_order_payment_method_id: str = Field("", alias="selfOrderPaymentMethodID")
    self_order_payment_method_name: str = Field("", alias="selfOrderPaymentMethodName")


class PaymentMethodResult(ESBBaseModel):
    """Payment method in response."""

    payment_method_id: int = Field(..., alias="paymentMethodID")
    payment_method_name: str = Field("", alias="paymentMethodName")


class PromotionResult(ESBBaseModel):
    """Promotion item in response."""

    promotion_id: int = Field(..., alias="promotionID")
    promotion_code: str = Field("", alias="promotionCode")
    promotion_type_desc: str = Field("", alias="promotionTypeDesc")
    notes: str = ""
    discount: Decimal = Decimal("0")
    min_subtotal: Decimal = Field(Decimal("0"), alias="minSubtotal")
    start_date: str = Field("", alias="startDate")
    end_date: str = Field("", alias="endDate")
    flag_show: bool = Field(False, alias="flagShow")
    promotion_category: list[PromotionCategoryResult] = Field(
        default_factory=list, alias="promotionCategory"
    )
    branches: list[PromotionBranchResult] = Field(default_factory=list)
    self_order_payment_methods: list[SelfOrderPaymentMethodResult] = Field(
        default_factory=list, alias="selfOrderPaymentMethods"
    )
    payment_method: PaymentMethodResult | None = Field(
        default=None, alias="paymentMethod"
    )
