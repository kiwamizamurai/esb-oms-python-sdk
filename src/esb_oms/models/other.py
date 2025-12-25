"""Other models for ESB OMS API."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from esb_oms.models.common import ESBBaseModel


class BranchSalesSummaryRequest(ESBBaseModel):
    """Request body for Branch Sales Summary API."""

    filter_sales_date_from: str = Field(..., alias="filterSalesDateFrom")
    filter_sales_date_to: str = Field(..., alias="filterSalesDateTo")
    sales_type: str | None = Field(default=None, alias="salesType")


class BranchSalesSummaryItem(ESBBaseModel):
    """Branch sales summary item in response."""

    sales_date: str = Field("", alias="salesDate")
    branch_code: str = Field("", alias="branchCode")
    branch_name: str = Field("", alias="branchName")
    pax_total: int = Field(0, alias="paxTotal")
    bill_total: int = Field(0, alias="billTotal")
    subtotal: Decimal = Decimal("0")
    discount_total: Decimal = Field(Decimal("0"), alias="discountTotal")
    sc_total: Decimal = Field(Decimal("0"), alias="scTotal")
    tax_total: Decimal = Field(Decimal("0"), alias="taxTotal")
    grand_total: Decimal = Field(Decimal("0"), alias="grandTotal")


class DailySalesMaterialUsageItem(ESBBaseModel):
    """Daily sales material usage item in response."""

    branch_code: str = Field("", alias="branchCode")
    branch: str = ""
    sales_date: str = Field("", alias="salesDate")
    product_code: str = Field("", alias="productCode")
    product_name: str = Field("", alias="productName")
    total_qty: Decimal = Field(Decimal("0"), alias="totalQty")
    unit: str = ""
    total_conversion_qty: Decimal = Field(Decimal("0"), alias="totalConversionQty")
    unit_conversion: str = Field("", alias="unitConversion")


class GetSalesRequest(ESBBaseModel):
    """Request body for Get Sales API."""

    bill_num: str | None = Field(default=None, alias="billNum")
    sales_num: str | None = Field(default=None, alias="salesNum")


class SalesPackageItem(ESBBaseModel):
    """Sales package item in response."""

    menu_id: int = Field(0, alias="menuID")
    menu_name: str = Field("", alias="menuName")
    menu_code: str = Field("", alias="menuCode")
    qty: int = 0
    original_price: Decimal = Field(Decimal("0"), alias="originalPrice")
    price: Decimal = Decimal("0")
    discount: Decimal = Decimal("0")
    other_tax: Decimal = Field(Decimal("0"), alias="otherTax")
    vat: Decimal = Decimal("0")
    other_tax_on_vat: bool = Field(False, alias="otherTaxOnVat")
    total: Decimal = Decimal("0")
    notes: str = ""
    status_id: int = Field(0, alias="statusID")
    status_name: str = Field("", alias="statusName")


class SalesExtraItem(ESBBaseModel):
    """Sales extra item in response."""

    menu_extra_id: int = Field(0, alias="menuExtraID")
    menu_extra_name: str = Field("", alias="menuExtraName")
    qty: Decimal = Decimal("0")
    price: Decimal = Decimal("0")
    discount: Decimal = Decimal("0")
    other_tax: Decimal = Field(Decimal("0"), alias="otherTax")
    vat: Decimal = Decimal("0")
    other_tax_on_vat: Decimal = Field(Decimal("0"), alias="otherTaxOnVat")
    total: Decimal = Decimal("0")
    status_id: int = Field(0, alias="statusID")
    status_name: str = Field("", alias="statusName")


class SalesMenuDetailItem(ESBBaseModel):
    """Sales menu detail item in response."""

    sales_date: str = Field("", alias="salesDate")
    branch_id: int = Field(0, alias="branchID")
    branch_code: str = Field("", alias="branchCode")
    branch_name: str = Field("", alias="branchName")
    sales_num: str = Field("", alias="salesNum")
    bill_num: str = Field("", alias="billNum")
    batch_id: int = Field(0, alias="batchID")
    menu_category_id: int = Field(0, alias="menuCategoryID")
    menu_category_name: str = Field("", alias="menuCategoryName")
    menu_category_detail_id: int = Field(0, alias="menuCategoryDetailID")
    menu_category_detail_name: str = Field("", alias="menuCategoryDetailName")
    menu_id: int = Field(0, alias="menuID")
    menu_name: str = Field("", alias="menuName")
    menu_code: str = Field("", alias="menuCode")
    qty: int = 0
    original_price: Decimal = Field(Decimal("0"), alias="originalPrice")
    price: Decimal = Decimal("0")
    inclusive_price: Decimal = Field(Decimal("0"), alias="inclusivePrice")
    discount: Decimal = Decimal("0")
    discount_value: Decimal = Field(Decimal("0"), alias="discountValue")
    inclusive_discount_value: Decimal = Field(
        Decimal("0"), alias="inclusiveDiscountValue"
    )
    other_tax: Decimal = Field(Decimal("0"), alias="otherTax")
    other_tax_value: Decimal = Field(Decimal("0"), alias="otherTaxValue")
    vat: Decimal = Decimal("0")
    vat_value: Decimal = Field(Decimal("0"), alias="vatValue")
    other_tax_on_vat: bool = Field(False, alias="otherTaxOnVat")
    total: Decimal = Decimal("0")
    notes: str = ""
    status_id: int = Field(0, alias="statusID")
    status_name: str = Field("", alias="statusName")
    promotion_detail_id: int = Field(0, alias="promotionDetailID")
    menu_promotion_id: int = Field(0, alias="menuPromotionID")
    sales_type: str = Field("", alias="salesType")
    cancel_notes: str = Field("", alias="cancelNotes")
    created_by: str = Field("", alias="createdBy")
    created_date: str = Field("", alias="createdDate")
    edited_by: str = Field("", alias="editedBy")
    edited_date: str = Field("", alias="editedDate")
    packages: list[SalesPackageItem] = Field(default_factory=list)
    extras: list[SalesExtraItem] = Field(default_factory=list)


class SalesPaymentDetailItem(ESBBaseModel):
    """Sales payment detail item in response."""

    sales_payment_backend_id: int = Field(0, alias="salesPaymentBackendID")
    sales_payment_pos_id: int = Field(0, alias="salesPaymentPosID")
    payment_method_type_id: int = Field(0, alias="paymentMethodTypeID")
    payment_method_type_name: str = Field("", alias="paymentMethodTypeName")
    payment_method_id: int = Field(0, alias="paymentMethodID")
    payment_method_name: str = Field("", alias="paymentMethodName")
    voucher_code: str = Field("", alias="voucherCode")
    notes: str = ""
    card_number: str = Field("", alias="cardNumber")
    bank_name: str = Field("", alias="bankName")
    account_name: str = Field("", alias="accountName")
    self_order_id: str | None = Field(default=None, alias="selfOrderID")
    verification_code: str = Field("", alias="verificationCode")
    payment_amount: Decimal = Field(Decimal("0"), alias="paymentAmount")
    full_payment_amount: Decimal = Field(Decimal("0"), alias="fullPaymentAmount")


class SalesDetailItem(ESBBaseModel):
    """Sales detail item in response."""

    sales_num: str = Field("", alias="salesNum")
    parent_link_sales_num: str | None = Field(default=None, alias="parentLinkSalesNum")
    bill_num: str = Field("", alias="billNum")
    sales_date: str = Field("", alias="salesDate")
    sales_date_in: str = Field("", alias="salesDateIn")
    sales_date_out: str = Field("", alias="salesDateOut")
    branch_code: str = Field("", alias="branchCode")
    branch_name: str = Field("", alias="branchName")
    member_id: int | None = Field(default=None, alias="memberID")
    member_code: str | None = Field(default=None, alias="memberCode")
    member_name: str | None = Field(default=None, alias="memberName")
    table_id: int = Field(0, alias="tableID")
    table_name: str = Field("", alias="tableName")
    visit_purpose_id: int = Field(0, alias="visitPurposeID")
    visit_purpose_name: str = Field("", alias="visitPurposeName")
    pax_total: int = Field(0, alias="paxTotal")
    subtotal: Decimal = Decimal("0")
    discount_total: Decimal = Field(Decimal("0"), alias="discountTotal")
    menu_discount_total: Decimal = Field(Decimal("0"), alias="menuDiscountTotal")
    promotion_discount: Decimal = Field(Decimal("0"), alias="promotionDiscount")
    other_tax_total: Decimal = Field(Decimal("0"), alias="otherTaxTotal")
    vat_total: Decimal = Field(Decimal("0"), alias="vatTotal")
    grand_total: Decimal = Field(Decimal("0"), alias="grandTotal")
    voucher_total: Decimal = Field(Decimal("0"), alias="voucherTotal")
    rounding_total: Decimal = Field(Decimal("0"), alias="roundingTotal")
    payment_total: Decimal = Field(Decimal("0"), alias="paymentTotal")
    billing_print_count: int = Field(0, alias="billingPrintCount")
    payment_print_count: int = Field(0, alias="paymentPrintCount")
    additional_info: str = Field("", alias="additionalInfo")
    promotion_id: int | None = Field(default=None, alias="promotionID")
    promotion_name: str | None = Field(default=None, alias="promotionName")
    status_id: int = Field(0, alias="statusID")
    status_name: str = Field("", alias="statusName")
    created_by: str = Field("", alias="createdBy")
    edited_by: str = Field("", alias="editedBy")
    edited_date: str = Field("", alias="editedDate")
    sales_payments: list[SalesPaymentDetailItem] = Field(
        default_factory=list, alias="salesPayments"
    )
    sales_menus: list[SalesMenuDetailItem] = Field(
        default_factory=list, alias="salesMenus"
    )
    sales_info: list[dict[str, str]] = Field(default_factory=list, alias="salesInfo")
