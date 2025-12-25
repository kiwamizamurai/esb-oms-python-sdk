"""Master POS data models for ESB OMS API."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from esb_oms.models.common import ESBBaseModel


class MenuPackageItem(ESBBaseModel):
    """Individual menu package item."""

    id: int = Field(..., alias="ID")
    menu_group_id: int = Field(..., alias="menuGroupID")
    menu_id: int = Field(..., alias="menuID")
    menu_name: str = Field(..., alias="menuName")
    menu_short_name: str = Field(..., alias="menuShortName")
    menu_code: str = Field(..., alias="menuCode")
    description: str = ""
    menu_category_id: int = Field(..., alias="menuCategoryID")
    menu_category_name: str = Field(..., alias="menuCategoryName")
    price: Decimal
    image_url: str | None = Field(default=None, alias="imageUrl")
    flag_default: int = Field(0, alias="flagDefault")
    flag_active: int = Field(1, alias="flagActive")
    created_by: str = Field("", alias="createdBy")
    created_date: str = Field("", alias="createdDate")
    edited_by: str = Field("", alias="editedBy")
    edited_date: str = Field("", alias="editedDate")


class MenuPackageGroup(ESBBaseModel):
    """Menu package group containing package items."""

    menu_group_id: int = Field(..., alias="menuGroupID")
    menu_group: str = Field(..., alias="menuGroup")
    min_qty: Decimal = Field(Decimal("0"), alias="minQty")
    max_qty: Decimal = Field(Decimal("0"), alias="maxQty")
    notes: str = ""
    packages: list[MenuPackageItem] = Field(default_factory=list)


class MenuExtraItem(ESBBaseModel):
    """Individual menu extra item."""

    menu_group_id: int = Field(..., alias="menuGroupID")
    menu_extra_id: int = Field(..., alias="menuExtraID")
    menu_extra_name: str = Field(..., alias="menuExtraName")
    menu_extra_short_name: str = Field("", alias="menuExtraShortName")
    menu_extra_code: str = Field(..., alias="menuExtraCode")
    price: Decimal
    notes: str = ""


class MenuExtraGroup(ESBBaseModel):
    """Menu extra group containing extra items."""

    menu_group_id: int = Field(..., alias="menuGroupID")
    menu_group: str = Field(..., alias="menuGroup")
    min_qty: Decimal = Field(Decimal("0"), alias="minQty")
    max_qty: Decimal = Field(Decimal("0"), alias="maxQty")
    notes: str = ""
    extras: list[MenuExtraItem] = Field(default_factory=list)


class MenuIcon(ESBBaseModel):
    """Menu icon information."""

    menu_icon_id: int = Field(..., alias="menuIconID")
    menu_icon_name: str = Field(..., alias="menuIconName")
    menu_icon_url: str = Field("", alias="menuIconUrl")


class POSMenuItem(ESBBaseModel):
    """Menu item in POS menu response."""

    menu_category_id: int = Field(..., alias="menuCategoryID")
    menu_category_name: str = Field(..., alias="menuCategoryName")
    menu_id: int = Field(..., alias="menuID")
    menu_name: str = Field(..., alias="menuName")
    menu_short_name: str = Field(..., alias="menuShortName")
    menu_code: str = Field(..., alias="menuCode")
    price: Decimal
    flag_tax: int = Field(0, alias="flagTax")
    flag_other_tax: int = Field(0, alias="flagOtherTax")
    zero_value_text: str = Field("0", alias="zeroValueText")
    flag_customer_print: int = Field(1, alias="flagCustomerPrint")
    show_menu_image: int = Field(1, alias="showMenuImage")
    image_url: str | None = Field(default=None, alias="imageUrl")
    cat_detail_image_url: str | None = Field(default=None, alias="catDetailImageUrl")
    description: str = ""
    flag_sold_out: int = Field(0, alias="flagSoldOut")
    menu_icons: list[MenuIcon] = Field(default_factory=list, alias="menuIcons")
    menu_packages: list[MenuPackageGroup] = Field(
        default_factory=list, alias="menuPackages"
    )
    menu_extras: list[MenuExtraGroup] = Field(default_factory=list, alias="menuExtras")


class MenuCategoryDetail(ESBBaseModel):
    """Menu category detail containing menus."""

    id: int = Field(..., alias="ID")
    menu_category_detail_desc: str = Field(..., alias="menuCategoryDetailDesc")
    image_url: str | None = Field(default=None, alias="imageUrl")
    menus: list[POSMenuItem] = Field(default_factory=list)


class MenuCategory(ESBBaseModel):
    """Menu category in POS menu response."""

    menu_category_id: int = Field(..., alias="menuCategoryID")
    menu_category_desc: str = Field(..., alias="menuCategoryDesc")
    menu_category_details: list[MenuCategoryDetail] = Field(
        default_factory=list, alias="menuCategoryDetails"
    )


class StockBranchItem(ESBBaseModel):
    """Stock item for a branch."""

    branch_code: str = Field(..., alias="branchCode")
    branch_name: str = Field(..., alias="branchName")
    product_name: str = Field(..., alias="productName")
    product_code: str = Field(..., alias="productCode")
    uom_name: str = Field(..., alias="uomName")
    stock: Decimal
    hpp: Decimal = Decimal("0")
    sell_price_merchandise: Decimal = Field(Decimal("0"), alias="sellPriceMerchandise")


class VisitPurpose(ESBBaseModel):
    """Visit purpose information."""

    visit_purpose_id: int = Field(..., alias="visitPurposeID")
    visit_purpose_name: str = Field(..., alias="visitPurposeName")
    flag_dine_in: int = Field(0, alias="flagDineIn")
    kiosk_mode_id: int = Field(0, alias="kioskModeID")
    flag_quick_service: int = Field(0, alias="flagQuickService")
    flag_show_queue: int = Field(0, alias="flagShowQueue")
    flag_max_order: int = Field(0, alias="flagMaxOrder")
    flag_active: int = Field(1, alias="flagActive")
    created_by: str = Field("", alias="createdBy")
    created_date: str = Field("", alias="createdDate")
    edited_by: str = Field("", alias="editedBy")
    edited_date: str = Field("", alias="editedDate")


class PaymentMethodItem(ESBBaseModel):
    """Individual payment method."""

    payment_method_id: int = Field(..., alias="paymentMethodID")
    payment_method_code: str = Field(..., alias="paymentMethodCode")
    payment_method_name: str = Field(..., alias="paymentMethodName")


class PaymentMethodType(ESBBaseModel):
    """Payment method type grouping."""

    payment_method_type: str = Field(..., alias="paymentMethodType")
    payment_methods: list[PaymentMethodItem] = Field(
        default_factory=list, alias="paymentMethods"
    )


class BusinessHour(ESBBaseModel):
    """Business hour for a branch."""

    branch_id: int = Field(..., alias="branchID")
    day_id: int = Field(..., alias="dayID")
    day_name: str = Field(..., alias="dayName")
    start_time: str = Field(..., alias="startTime")
    end_time: str = Field(..., alias="endTime")
    status: int = 1


class BranchVisitPurpose(ESBBaseModel):
    """Visit purpose for a branch."""

    visit_purpose_id: int = Field(..., alias="visitPurposeID")
    visit_purpose_name: str = Field(..., alias="visitPurposeName")
    order_fee: Decimal = Field(Decimal("0"), alias="orderFee")
    flag_self_order: int = Field(0, alias="flagSelfOrder")
    url: str = ""


class Branch(ESBBaseModel):
    """Branch/outlet information."""

    branch_code: str = Field(..., alias="branchCode")
    branch_name: str = Field(..., alias="branchName")
    branch_thumbnail_image: str | None = Field(
        default=None, alias="branchThumbnailImage"
    )
    branch_banner_image: str | None = Field(default=None, alias="branchBannerImage")
    brand_name: str = Field("", alias="brandName")
    address: str = ""
    phone: str = ""
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    timezone: str = ""
    timezone_val: Decimal | None = Field(default=None, alias="timezoneVal")
    is_open: str | None = Field(default=None, alias="isOpen")
    is_forced_closed: str | None = Field(default=None, alias="isForcedClosed")
    is_forced_closed_message: str | None = Field(
        default=None, alias="isForcedClosedMessage"
    )
    distance: int | None = None
    in_coverage: int | None = Field(default=None, alias="inCoverage")
    business_hour: list[BusinessHour] = Field(
        default_factory=list, alias="businessHour"
    )
    visit_purposes: list[BranchVisitPurpose] = Field(
        default_factory=list, alias="visitPurposes"
    )


class GetMenuRequest(ESBBaseModel):
    """Request body for Get Menu API."""

    filter_branch_code: str = Field(..., alias="filterBranchCode")
    filter_visit_purpose_id: str = Field(..., alias="filterVisitPurposeID")


class GetStockBranchRequest(ESBBaseModel):
    """Request body for Get Stock Branch API."""

    filter_branch_code: str = Field(..., alias="filterBranchCode")


class GetVisitPurposeRequest(ESBBaseModel):
    """Request body for Get Visit Purpose API."""

    visit_purpose_id: str | None = Field(default=None, alias="visitPurposeID")


class GetPaymentMethodRequest(ESBBaseModel):
    """Request body for Get Payment Method API."""

    filter_branch_code: str = Field(..., alias="filterBranchCode")


class GetBranchRequest(ESBBaseModel):
    """Request body for Get Branch API."""

    filter_branch_name: str | None = Field(default=None, alias="filterBranchName")
    filter_branch_address: str | None = Field(default=None, alias="filterBranchAddress")
    filter_branch_phone: str | None = Field(default=None, alias="filterBranchPhone")
    filter_brand_id: str | None = Field(default=None, alias="filterBrandID")
