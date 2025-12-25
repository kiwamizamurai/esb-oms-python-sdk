"""Report models for ESB OMS API."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from esb_oms.models.common import ESBBaseModel


class SalesHeadRequest(ESBBaseModel):
    """Request body for Sales Head API."""

    filter_sales_date_from: str = Field(..., alias="filterSalesDateFrom")
    filter_sales_date_to: str = Field(..., alias="filterSalesDateTo")
    filter_branch_code: str | None = Field(default=None, alias="filterBranchCode")
    filter_bill_num: str | None = Field(default=None, alias="filterBillNum")
    filter_sales_num: str | None = Field(default=None, alias="filterSalesNum")


class SalesPaymentItem(ESBBaseModel):
    """Sales payment item in response."""

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
    self_order_id: str = Field("", alias="selfOrderID")
    verification_code: str = Field("", alias="verificationCode")
    payment_amount: Decimal = Field(Decimal("0"), alias="paymentAmount")
    full_payment_amount: Decimal = Field(Decimal("0"), alias="fullPaymentAmount")


class SalesMenuPackageItem(ESBBaseModel):
    """Sales menu package item in response."""

    menu_id: int = Field(0, alias="menuID")
    menu_name: str = Field("", alias="menuName")
    menu_code: str = Field("", alias="menuCode")
    qty: int = 0
    original_price: Decimal = Field(Decimal("0"), alias="originalPrice")
    price: Decimal = Decimal("0")
    discount: Decimal = Decimal("0")
    discount_value: Decimal = Field(Decimal("0"), alias="discountValue")
    other_tax: Decimal = Field(Decimal("0"), alias="otherTax")
    other_tax_value: Decimal = Field(Decimal("0"), alias="otherTaxValue")
    vat: Decimal = Decimal("0")
    vat_value: Decimal = Field(Decimal("0"), alias="vatValue")
    other_vat: Decimal = Field(Decimal("0"), alias="otherVat")
    other_vat_value: Decimal = Field(Decimal("0"), alias="otherVatValue")
    other_tax_on_vat: bool = Field(False, alias="otherTaxOnVat")
    total: Decimal = Decimal("0")
    notes: str = ""
    status_id: int = Field(0, alias="statusID")
    status_name: str = Field("", alias="statusName")


class SalesMenuExtraItem(ESBBaseModel):
    """Sales menu extra item in response."""

    menu_extra_id: int = Field(0, alias="menuExtraID")
    menu_extra_name: str = Field("", alias="menuExtraName")
    qty: int = 0
    price: Decimal = Decimal("0")
    discount: Decimal = Decimal("0")
    discount_value: Decimal = Field(Decimal("0"), alias="discountValue")
    other_tax: Decimal = Field(Decimal("0"), alias="otherTax")
    other_tax_value: Decimal = Field(Decimal("0"), alias="otherTaxValue")
    vat: Decimal = Decimal("0")
    vat_value: Decimal = Field(Decimal("0"), alias="vatValue")
    other_vat: Decimal = Field(Decimal("0"), alias="otherVat")
    other_vat_value: Decimal = Field(Decimal("0"), alias="otherVatValue")
    other_tax_on_vat: bool = Field(False, alias="otherTaxOnVat")
    total: Decimal = Decimal("0")
    status_id: int = Field(0, alias="statusID")
    status_name: str = Field("", alias="statusName")


class SalesMenuItem(ESBBaseModel):
    """Sales menu item in response."""

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
    other_tax: Decimal = Field(Decimal("0"), alias="otherTax")
    other_tax_value: Decimal = Field(Decimal("0"), alias="otherTaxValue")
    vat: Decimal = Decimal("0")
    vat_value: Decimal = Field(Decimal("0"), alias="vatValue")
    other_vat: Decimal = Field(Decimal("0"), alias="otherVat")
    other_vat_value: Decimal = Field(Decimal("0"), alias="otherVatValue")
    other_tax_on_vat: bool = Field(False, alias="otherTaxOnVat")
    total: Decimal = Decimal("0")
    notes: str = ""
    status_id: int = Field(0, alias="statusID")
    status_name: str = Field("", alias="statusName")
    promotion_detail_id: int = Field(0, alias="promotionDetailID")
    promotion_id: int = Field(0, alias="promotionID")
    cancel_notes: str = Field("", alias="cancelNotes")
    created_by: str = Field("", alias="createdBy")
    created_date: str = Field("", alias="createdDate")
    edited_by: str = Field("", alias="editedBy")
    edited_date: str = Field("", alias="editedDate")
    packages: list[SalesMenuPackageItem] = Field(default_factory=list)
    extras: list[SalesMenuExtraItem] = Field(default_factory=list)


class SalesHeadItem(ESBBaseModel):
    """Sales head item in response."""

    sales_num: str = Field("", alias="salesNum")
    parent_link_sales_num: str = Field("", alias="parentLinkSalesNum")
    bill_num: str = Field("", alias="billNum")
    sales_date: str = Field("", alias="salesDate")
    sales_date_in: str = Field("", alias="salesDateIn")
    sales_date_out: str = Field("", alias="salesDateOut")
    branch_id: int = Field(0, alias="branchID")
    branch_code: str = Field("", alias="branchCode")
    member_id: str = Field("", alias="memberID")
    member_code: str = Field("", alias="memberCode")
    member_name: str = Field("", alias="memberName")
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
    promotion_id: int = Field(0, alias="promotionID")
    promotion_name: str = Field("", alias="promotionName")
    status_id: int = Field(0, alias="statusID")
    status_name: str = Field("", alias="statusName")
    created_by: str = Field("", alias="createdBy")
    edited_by: str = Field("", alias="editedBy")
    edited_date: str = Field("", alias="editedDate")
    sales_payments: list[SalesPaymentItem] = Field(
        default_factory=list, alias="salesPayments"
    )
    sales_menus: list[SalesMenuItem] = Field(default_factory=list, alias="salesMenus")


class MergeTableItem(ESBBaseModel):
    """Merge table item in response."""

    id: int = Field(0, alias="ID")
    local_id: int = Field(0, alias="localID")
    sales_num: str = Field("", alias="salesNum")
    table_id: int = Field(0, alias="tableID")
    sync_date: str = Field("", alias="syncDate")


class ChildLinkSalesItem(ESBBaseModel):
    """Child link sales item in response."""

    sales_num: str = Field("", alias="salesNum")


class SalesInformationItem(ESBBaseModel):
    """Sales information item in response."""

    sales_num: str = Field("", alias="salesNum")
    bill_num: str = Field("", alias="billNum")
    sales_date: str = Field("", alias="salesDate")
    sales_date_in: str = Field("", alias="salesDateIn")
    sales_date_out: str = Field("", alias="salesDateOut")
    branch_id: int = Field(0, alias="branchID")
    branch_code: str = Field("", alias="branchCode")
    ext_branch_code: str = Field("", alias="extBranchCode")
    member_code: str = Field("", alias="memberCode")
    member_name: str = Field("", alias="memberName")
    external_member_code: str = Field("", alias="externalMemberCode")
    table_id: int = Field(0, alias="tableID")
    table_name: str = Field("", alias="tableName")
    visit_purpose_id: int = Field(0, alias="visitPurposeID")
    visit_purpose_name: str = Field("", alias="visitPurposeName")
    visitor_type_id: int = Field(0, alias="visitorTypeID")
    pax_total: int = Field(0, alias="paxTotal")
    subtotal: Decimal = Decimal("0")
    discount_total: Decimal = Field(Decimal("0"), alias="discountTotal")
    menu_discount_total: Decimal = Field(Decimal("0"), alias="menuDiscountTotal")
    promotion_discount: Decimal = Field(Decimal("0"), alias="promotionDiscount")
    voucher_discount_total: Decimal = Field(Decimal("0"), alias="voucherDiscountTotal")
    other_tax_total: Decimal = Field(Decimal("0"), alias="otherTaxTotal")
    vat_total: Decimal = Field(Decimal("0"), alias="vatTotal")
    other_vat_total: Decimal = Field(Decimal("0"), alias="otherVatTotal")
    delivery_cost: Decimal = Field(Decimal("0"), alias="deliveryCost")
    order_fee: Decimal = Field(Decimal("0"), alias="orderFee")
    grand_total: Decimal = Field(Decimal("0"), alias="grandTotal")
    voucher_total: Decimal = Field(Decimal("0"), alias="voucherTotal")
    rounding_total: Decimal = Field(Decimal("0"), alias="roundingTotal")
    payment_total: Decimal = Field(Decimal("0"), alias="paymentTotal")
    billing_print_count: int = Field(0, alias="billingPrintCount")
    payment_print_count: int = Field(0, alias="paymentPrintCount")
    additional_info: str = Field("", alias="additionalInfo")
    promotion_id: int = Field(0, alias="promotionID")
    promotion_name: str = Field("", alias="promotionName")
    flag_inclusive: bool = Field(False, alias="flagInclusive")
    status_id: int = Field(0, alias="statusID")
    status_name: str = Field("", alias="statusName")
    full_name: str = Field("", alias="fullName")
    email: str = ""
    phone_number: str = Field("", alias="phoneNumber")
    created_by: str = Field("", alias="createdBy")
    edited_by: str = Field("", alias="editedBy")
    edited_date: str = Field("", alias="editedDate")
    sales_payments: list[SalesPaymentItem] = Field(
        default_factory=list, alias="salesPayments"
    )
    sales_menus: list[SalesMenuItem] = Field(default_factory=list, alias="salesMenus")
    parent_link_sales_num: str = Field("", alias="parentlinkSalesNum")
    child_link_sales_num: list[ChildLinkSalesItem] = Field(
        default_factory=list, alias="childlinkSalesNum"
    )
    merge_table: list[MergeTableItem] = Field(default_factory=list, alias="mergetable")


class SalesMenuCompletionRequest(ESBBaseModel):
    """Request body for Sales Menu Completion API."""

    filter_sales_date_from: str = Field(..., alias="filterSalesDateFrom")
    filter_sales_date_to: str = Field(..., alias="filterSalesDateTo")
    filter_branch_code: str | None = Field(default=None, alias="filterBranchCode")


class SalesMenuCompletionItem(ESBBaseModel):
    """Sales menu completion item in response."""

    sales_date: str = Field("", alias="salesDate")
    order_time: str = Field("", alias="orderTime")
    branch_code: str = Field("", alias="branchCode")
    branch_name: str = Field("", alias="branchName")
    sales_num: str = Field("", alias="salesNum")
    bill_num: str = Field("", alias="billNum")
    menu_category_detail: str = Field("", alias="menuCategoryDetail")
    menu_category: str = Field("", alias="menuCategory")
    sales_menu_id: int = Field(0, alias="salesMenuID")
    menu_code: str = Field("", alias="menuCode")
    menu: str = ""
    kitchen_qty: Decimal = Field(Decimal("0"), alias="kitchenQty")
    kitchen_process: Decimal = Field(Decimal("0"), alias="kitchenProcess")
    checker_qty: Decimal = Field(Decimal("0"), alias="checkerQty")
    checker_process: Decimal = Field(Decimal("0"), alias="checkerProcess")
    total_process: Decimal = Field(Decimal("0"), alias="totalProcess")


class MenuSummaryItem(ESBBaseModel):
    """Menu summary item in response."""

    menu_id: int = Field(0, alias="menuID")
    menu_code: str = Field("", alias="menuCode")
    menu_name: str = Field("", alias="menuName")
    menu_category_detail_desc: str = Field("", alias="menuCategoryDetailDesc")
    menu_category_desc: str = Field("", alias="menuCategoryDesc")
    qty: int = 0
    amount: Decimal = Decimal("0")
    tax: Decimal = Decimal("0")
    vat: Decimal = Decimal("0")
    sc: Decimal = Decimal("0")
    discount: Decimal = Decimal("0")
    total: Decimal = Decimal("0")


class SalesMenuSummaryResult(ESBBaseModel):
    """Sales menu summary result in response."""

    sales_date: str = Field("", alias="salesDate")
    branch_code: str = Field("", alias="branchCode")
    branch_name: str = Field("", alias="branchName")
    menus: list[MenuSummaryItem] = Field(default_factory=list)


class GetSalesMenuSummaryResponse(ESBBaseModel):
    """Response for Sales Menu Summary API."""

    path: str = ""
    code: int = 200
    timestamp: str = ""
    message: str = ""
    data: SalesMenuSummaryResult | None = None


class SalesMenuRequest(ESBBaseModel):
    """Request body for Sales Menu API."""

    filter_sales_date_from: str = Field(..., alias="filterSalesDateFrom")
    filter_sales_date_to: str = Field(..., alias="filterSalesDateTo")
    filter_branch_code: str | None = Field(default=None, alias="filterBranchCode")
    filter_sales_num: str | None = Field(default=None, alias="filterSalesNum")


class SalesMenuReportPackageItem(ESBBaseModel):
    """Sales menu report package item."""

    menu_id: int = Field(0, alias="menuID")
    menu_name: str = Field("", alias="menuName")
    menu_code: str = Field("", alias="menuCode")
    qty: Decimal = Decimal("0")
    original_price: Decimal = Field(Decimal("0"), alias="originalPrice")
    price: Decimal = Decimal("0")
    discount: Decimal = Decimal("0")
    other_tax: Decimal = Field(Decimal("0"), alias="otherTax")
    vat: Decimal = Decimal("0")
    other_tax_on_vat: Decimal = Field(Decimal("0"), alias="otherTaxOnVat")
    total: Decimal = Decimal("0")
    notes: str = ""
    status_id: int = Field(0, alias="statusID")
    status_name: str = Field("", alias="statusName")


class SalesMenuReportExtraItem(ESBBaseModel):
    """Sales menu report extra item."""

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


class SalesMenuReportItem(ESBBaseModel):
    """Sales menu report item in response."""

    sales_date: str = Field("", alias="salesDate")
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
    qty: Decimal = Decimal("0")
    original_price: Decimal = Field(Decimal("0"), alias="originalPrice")
    price: Decimal = Decimal("0")
    inclusive_price: Decimal = Field(Decimal("0"), alias="inclusivePrice")
    discount: Decimal = Decimal("0")
    discount_value: Decimal = Field(Decimal("0"), alias="discountValue")
    inclusive_discount_value: Decimal = Field(
        Decimal("0"), alias="inclusiveDiscountValue"
    )
    other_tax_value: Decimal = Field(Decimal("0"), alias="otherTaxValue")
    other_tax: Decimal = Field(Decimal("0"), alias="otherTax")
    vat: Decimal = Decimal("0")
    vat_value: Decimal = Field(Decimal("0"), alias="vatValue")
    other_tax_on_vat: Decimal = Field(Decimal("0"), alias="otherTaxOnVat")
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
    packages: list[SalesMenuReportPackageItem] = Field(default_factory=list)
    extras: list[SalesMenuReportExtraItem] = Field(default_factory=list)


class PaymentSummaryItem(ESBBaseModel):
    """Payment summary item in response."""

    payment_method_type_id: int = Field(0, alias="paymentMethodTypeID")
    payment_method_type_name: str = Field("", alias="paymentMethodTypeName")
    payment_method_id: int = Field(0, alias="paymentMethodID")
    payment_method_code: str = Field("", alias="paymentMethodCode")
    payment_method_name: str = Field("", alias="paymentMethodName")
    payment_count: int = Field(0, alias="paymentCount")
    payment_amount: Decimal = Field(Decimal("0"), alias="paymentAmount")
    mdr: Decimal = Decimal("0")
    net_after_mdr: Decimal = Field(Decimal("0"), alias="netAfterMDR")


class SalesPaymentSummaryItem(ESBBaseModel):
    """Sales payment summary item in response."""

    sales_date: str = Field("", alias="salesDate")
    branch_code: str = Field("", alias="branchCode")
    branch_name: str = Field("", alias="branchName")
    payments: list[PaymentSummaryItem] = Field(default_factory=list)


class GetSalesPaymentSummaryResponse(ESBBaseModel):
    """Response for Sales Payment Summary API."""

    path: str = ""
    timestamp: str = ""
    status: str = ""
    code: str = ""
    message: str = ""
    result: list[SalesPaymentSummaryItem] | None = None
    errors: list[dict[str, str]] | None = None
