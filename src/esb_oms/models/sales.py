"""Sales data models for ESB OMS API."""

from __future__ import annotations

from decimal import Decimal
from enum import IntEnum

from pydantic import Field

from esb_oms.models.common import ESBBaseModel


class SalesStatus(IntEnum):
    """Sales transaction status."""

    NEW = 1
    FINISHED = 8
    CANCELLED = 12
    VOID = 24


class MenuStatus(IntEnum):
    """Menu item status in a transaction."""

    PREPARING = 13
    PREPARED = 34
    SERVED = 14
    PRINT_CANCELLED = 19


class MenuExtra(ESBBaseModel):
    """Menu extra/add-on item.

    Extras are additional items that can be added to a menu item.
    """

    menu_extra_id: int = Field(..., alias="menuExtraID")
    menu_extra_code: str = Field(..., alias="menuExtraCode", max_length=50)
    menu_extra_name: str = Field(..., alias="menuExtraName", max_length=100)
    qty: int
    price: Decimal
    discount: Decimal = Decimal("0")
    other_tax: Decimal = Field(Decimal("0"), alias="otherTax")
    other_tax_value: Decimal = Field(Decimal("0"), alias="otherTaxValue")
    vat: Decimal = Decimal("0")
    vat_value: Decimal = Field(Decimal("0"), alias="vatValue")
    other_vat: Decimal = Field(Decimal("0"), alias="otherVat")
    other_vat_value: Decimal = Field(Decimal("0"), alias="otherVatValue")
    other_tax_on_vat: int = Field(0, alias="otherTaxOnVat")
    total: Decimal
    status_id: int = Field(MenuStatus.PREPARING, alias="statusID")


class MenuPackage(ESBBaseModel):
    """Menu package item.

    Packages are bundled items that come with the main menu item.
    """

    menu_id: int = Field(..., alias="menuID")
    menu_group_id: int | None = Field(default=None, alias="menuGroupID")
    menu_name: str = Field(..., alias="menuName", max_length=50)
    menu_code: str = Field(..., alias="menuCode", max_length=50)
    qty: int
    original_price: Decimal = Field(Decimal("0"), alias="originalPrice")
    price: Decimal
    discount: Decimal = Decimal("0")
    other_tax: Decimal = Field(Decimal("0"), alias="otherTax")
    other_tax_value: Decimal = Field(Decimal("0"), alias="otherTaxValue")
    vat: Decimal = Decimal("0")
    vat_value: Decimal = Field(Decimal("0"), alias="vatValue")
    other_vat: Decimal = Field(Decimal("0"), alias="otherVat")
    other_vat_value: Decimal = Field(Decimal("0"), alias="otherVatValue")
    other_tax_on_vat: int = Field(0, alias="otherTaxOnVat")
    total: Decimal
    notes: str = ""
    status_id: int = Field(MenuStatus.PREPARING, alias="statusID")


class SalesMenuItem(ESBBaseModel):
    """Menu item in a sales transaction."""

    menu_id: int = Field(..., alias="menuID")
    menu_code: str = Field(..., alias="menuCode", max_length=50)
    qty: int
    original_price: Decimal = Field(..., alias="originalPrice")
    price: Decimal
    discount: Decimal = Decimal("0")
    discount_value: Decimal = Field(Decimal("0"), alias="discountValue")
    other_tax: Decimal = Field(Decimal("0"), alias="otherTax")
    other_tax_value: Decimal = Field(Decimal("0"), alias="otherTaxValue")
    vat: Decimal = Decimal("0")
    vat_value: Decimal = Field(Decimal("0"), alias="vatValue")
    other_vat: Decimal = Field(Decimal("0"), alias="otherVat")
    other_vat_value: Decimal = Field(Decimal("0"), alias="otherVatValue")
    other_tax_on_vat: int = Field(0, alias="otherTaxOnVat")
    total: Decimal
    notes: str = ""
    status_id: int = Field(MenuStatus.PREPARING, alias="statusID")
    promotion_detail_id: int | None = Field(default=None, alias="promotionDetailID")
    promotion_id: int | None = Field(default=None, alias="promotionID")
    cancel_notes: str = Field("", alias="cancelNotes")
    created_by: str = Field(..., alias="createdBy", max_length=100)
    created_date: str = Field(..., alias="createdDate")
    edited_date: str = Field("", alias="editedDate")
    packages: list[MenuPackage] = Field(default_factory=list)
    extras: list[MenuExtra] = Field(default_factory=list)


class Payment(ESBBaseModel):
    """Payment information for a sales transaction."""

    payment_method: str = Field(..., alias="paymentMethod", max_length=50)
    coa_no: str = Field("", alias="coaNo", max_length=20)
    voucher_code: str = Field("", alias="voucherCode", max_length=50)
    notes: str = Field("", max_length=100)
    card_number: str = Field("", alias="cardNumber", max_length=20)
    card_holder: str = Field("", alias="cardHolder", max_length=100)
    amount: Decimal
    charge: Decimal = Decimal("0")
    change: Decimal = Decimal("0")


class SalesHead(ESBBaseModel):
    """Sales transaction header (main data).

    This is the main structure for pushing sales data to ESB OMS.
    """

    sales_num: str = Field(..., alias="salesNum", max_length=20)
    bill_num: str = Field("", alias="billNum", max_length=20)
    sales_date: str = Field(..., alias="salesDate")
    sales_date_in: str = Field(..., alias="salesDateIn")
    sales_date_out: str = Field("", alias="salesDateOut")
    branch_code: str = Field(..., alias="branchCode", max_length=20)
    member_code: str = Field("", alias="memberCode", max_length=20)
    customer_name: str = Field("", alias="customerName", max_length=100)
    visit_purpose_name: str = Field("", alias="visitPurposeName", max_length=50)
    pax_total: int = Field(1, alias="paxTotal")
    subtotal: Decimal
    discount_total: Decimal = Field(Decimal("0"), alias="discountTotal")
    menu_discount_total: Decimal = Field(Decimal("0"), alias="menuDiscountTotal")
    promotion_discount: Decimal = Field(Decimal("0"), alias="promotionDiscount")
    other_tax_total: Decimal = Field(Decimal("0"), alias="otherTaxTotal")
    vat_total: Decimal = Field(Decimal("0"), alias="vatTotal")
    other_vat_total: Decimal = Field(Decimal("0"), alias="otherVatTotal")
    delivery_fee: Decimal = Field(Decimal("0"), alias="deliveryFee")
    order_fee: Decimal = Field(Decimal("0"), alias="orderFee")
    grand_total: Decimal = Field(..., alias="grandTotal")
    voucher_total: Decimal = Field(Decimal("0"), alias="voucherTotal")
    rounding_total: Decimal = Field(Decimal("0"), alias="roundingTotal")
    payment_total: Decimal = Field(..., alias="paymentTotal")
    billing_print_count: int = Field(0, alias="billingPrintCount")
    payment_print_count: int = Field(0, alias="paymentPrintCount")
    additional_info: str = Field("", alias="additionalInfo", max_length=200)
    promotion_id: int | None = Field(default=None, alias="promotionID")
    flag_inclusive: int = Field(0, alias="flagInclusive")
    status_id: int = Field(SalesStatus.NEW, alias="statusID")
    created_by: str = Field(..., alias="createdBy", max_length=100)
    edited_by: str = Field("", alias="editedBy", max_length=100)
    edited_date: str = Field("", alias="editedDate")
    menu: list[SalesMenuItem] = Field(default_factory=list)
    payment: list[Payment] = Field(default_factory=list)


class PushSalesDataRequest(ESBBaseModel):
    """Request body for Push Sales Data API."""

    sales_head: SalesHead = Field(..., alias="salesHead")


class ShiftData(ESBBaseModel):
    """Shift data for shift-based reporting."""

    branch_code: str = Field(..., alias="branchCode", max_length=20)
    shift_num: str = Field(..., alias="shiftNum", max_length=20)
    shift_date: str = Field(..., alias="shiftDate")
    shift_start: str = Field(..., alias="shiftStart")
    shift_end: str = Field("", alias="shiftEnd")
    cashier_name: str = Field(..., alias="cashierName", max_length=100)
    opening_cash: Decimal = Field(Decimal("0"), alias="openingCash")
    closing_cash: Decimal = Field(Decimal("0"), alias="closingCash")
    total_sales: Decimal = Field(Decimal("0"), alias="totalSales")
    total_void: Decimal = Field(Decimal("0"), alias="totalVoid")
    total_discount: Decimal = Field(Decimal("0"), alias="totalDiscount")
    total_refund: Decimal = Field(Decimal("0"), alias="totalRefund")
    status_id: int = Field(1, alias="statusID")
    created_by: str = Field(..., alias="createdBy", max_length=100)


class PushShiftDataRequest(ESBBaseModel):
    """Request body for Push Shift Data API."""

    shift_data: ShiftData = Field(..., alias="shiftData")


class PushSalesDataResult(ESBBaseModel):
    """Result from Push Sales Data API."""

    sales_id: int | None = Field(default=None, alias="salesID")
    sales_num: str = Field(..., alias="salesNum")
    message: str = ""


class PushShiftDataResult(ESBBaseModel):
    """Result from Push Shift Data API."""

    shift_id: int | None = Field(default=None, alias="shiftID")
    shift_num: str = Field(..., alias="shiftNum")
    message: str = ""
