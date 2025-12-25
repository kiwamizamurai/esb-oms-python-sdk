"""Menu management models for ESB OMS API."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from esb_oms.models.common import ESBBaseModel


class MenuCategoryDetailInput(ESBBaseModel):
    """Menu category detail for create/update requests."""

    menu_category_detail_id: int | None = Field(
        default=None, alias="menuCategoryDetailID"
    )
    menu_category_detail_name: str = Field(..., alias="menuCategoryDetailName")
    menu_category_detail_on_eso: str = Field("", alias="menuCategoryDetailOnEso")
    menu_category_detail_code: str = Field("", alias="menuCategoryDetailCode")
    description: str = ""
    max_order_qty: Decimal = Field(Decimal("1"), alias="maxOrderQty")
    menu_category_detail_theme: str = Field("", alias="menuCategoryDetailTheme")
    image_url: str = Field("", alias="imageUrl")


class CreateMenuCategoryRequest(ESBBaseModel):
    """Request body for Create Menu Category API."""

    menu_category_name: str = Field(..., alias="menuCategoryName")
    menu_category_name_on_eso: str = Field("", alias="menuCategoryNameOnEso")
    menu_category_code: str = Field("", alias="menuCategoryCode")
    sales_account: str = Field(..., alias="salesAccount")
    cogs_account: str = Field(..., alias="cogsAccount")
    discount_account: str = Field(..., alias="discountAccount")
    description: str = ""
    image_url: str = Field("", alias="imageUrl")
    theme_category_on_pos: str = Field("", alias="themeCategoryOnPos")
    theme_option_category_on_pos: str = Field("", alias="themeOptionCategoryOnPos")
    menu_category_details: list[MenuCategoryDetailInput] = Field(
        ..., alias="menuCategoryDetails"
    )


class UpdateMenuCategoryRequest(ESBBaseModel):
    """Request body for Update Menu Category API."""

    menu_category_id: int = Field(..., alias="menuCategoryID")
    menu_category_name: str = Field(..., alias="menuCategoryName")
    menu_category_name_on_eso: str = Field("", alias="menuCategoryNameOnEso")
    menu_category_code: str = Field("", alias="menuCategoryCode")
    sales_account: str = Field(..., alias="salesAccount")
    cogs_account: str = Field(..., alias="cogsAccount")
    discount_account: str = Field(..., alias="discountAccount")
    description: str = ""
    image_url: str = Field("", alias="imageUrl")
    theme_category_on_pos: str = Field("", alias="themeCategoryOnPos")
    theme_option_category_on_pos: str = Field("", alias="themeOptionCategoryOnPos")
    menu_category_details: list[MenuCategoryDetailInput] = Field(
        ..., alias="menuCategoryDetails"
    )


class MenuCategoryDetailResult(ESBBaseModel):
    """Menu category detail in response."""

    menu_category_detail_id: int = Field(..., alias="menuCategoryDetailID")
    menu_category_detail_name: str = Field(..., alias="menuCategoryDetailName")
    menu_category_detail_code: str = Field("", alias="menuCategoryDetailCode")
    max_order_qty: Decimal = Field(Decimal("1"), alias="maxOrderQty")
    status: str = "Active"
    order_id: int | None = Field(default=None, alias="orderID")
    description: str | None = None
    button_color: str = Field("", alias="buttonColor")


class MenuCategoryResult(ESBBaseModel):
    """Menu category in response."""

    menu_category_id: int = Field(..., alias="menuCategoryID")
    menu_category_name: str = Field(..., alias="menuCategoryName")
    menu_category_code: str = Field("", alias="menuCategoryCode")
    sales_account: str = Field("", alias="salesAccount")
    cogs_account: str = Field("", alias="cogsAccount")
    discount_account: str = Field("", alias="discountAccount")
    notes: str = ""
    description: str = ""
    status: str = "Active"
    button_color: str = Field("", alias="buttonColor")
    menu_category_details: list[MenuCategoryDetailResult] = Field(
        default_factory=list, alias="menuCategoryDetails"
    )


class GetMenuCategoryResponse(ESBBaseModel):
    """Response data for Get Menu Category API."""

    page: str = "1"
    limit: int = 10
    count: int = 0
    data: list[MenuCategoryResult] = Field(default_factory=list)


class MenuTemplatePackageInput(ESBBaseModel):
    """Menu template package price input."""

    menu_template_id: int = Field(..., alias="menuTemplateID")
    price: Decimal


class MenuPackageMenuInput(ESBBaseModel):
    """Menu item within a package group."""

    menu_id: int = Field(..., alias="menuID")
    menu_name: str = Field("", alias="menuName")
    menu_code: str = Field("", alias="menuCode")
    price: Decimal
    default_item: bool = Field(False, alias="defaultItem")
    menu_template_packages: list[MenuTemplatePackageInput] = Field(
        default_factory=list, alias="menuTemplatePackages"
    )


class MenuPackageGroupInput(ESBBaseModel):
    """Menu package group input."""

    menu_group_id: int | str = Field("", alias="menuGroupID")
    menu_group_name: str = Field("", alias="menuGroupName")
    min_qty: Decimal = Field(Decimal("0"), alias="minQty")
    max_qty: Decimal = Field(Decimal("999999"), alias="maxQty")
    notes: str = ""
    order_id: int = Field(0, alias="orderID")
    flag_active: bool = Field(True, alias="flagActive")
    menus: list[MenuPackageMenuInput] = Field(default_factory=list)


class MenuExtraInput(ESBBaseModel):
    """Menu extra input."""

    menu_extra_id: int | str = Field("", alias="menuExtraID")
    menu_id: int = Field(..., alias="menuID")
    menu_name: str = Field("", alias="menuName")
    price: Decimal
    min_extra_qty: Decimal = Field(Decimal("0"), alias="minExtraQty")
    max_extra_qty: Decimal = Field(Decimal("1"), alias="maxExtraQty")
    color: str = ""


class MenuIconInput(ESBBaseModel):
    """Menu icon input."""

    menu_icon_name: str = Field(..., alias="menuIconName")


class MenuTagInput(ESBBaseModel):
    """Menu tag input."""

    tag_name: str = Field(..., alias="tagName")


class RelatedMenuInput(ESBBaseModel):
    """Related menu input."""

    menu_id: int = Field(..., alias="menuID")
    menu_name: str = Field("", alias="menuName")
    menu_code: str = Field("", alias="menuCode")


class CheckerInput(ESBBaseModel):
    """Checker/station input."""

    station_name: str = Field(..., alias="stationName")


class MenuTemplatePriceInput(ESBBaseModel):
    """Menu template price input for menu creation."""

    menu_template_id: int = Field(..., alias="menuTemplateID")
    price: Decimal


class CreateMenuRequest(ESBBaseModel):
    """Request body for Create Menu API."""

    menu_category_detail_id: int = Field(..., alias="menuCategoryDetailID")
    bom_id: int = Field(0, alias="bomID")
    menu_name: str = Field(..., alias="menuName")
    menu_code: str = Field(..., alias="menuCode")
    menu_short_name: str = Field("", alias="menuShortName")
    alternative_menu_name: str = Field("", alias="alternativeMenuName")
    flag_tax: int = Field(0, alias="flagTax")
    flag_other_tax: bool = Field(False, alias="flagOtherTax")
    zero_value_text: str = Field("0", alias="zeroValueText")
    sales_account: str = Field("", alias="salesAccount")
    cogs_account: str = Field("", alias="cogsAccount")
    discount_account: str = Field("", alias="discountAccount")
    description: str = ""
    image_url: str = Field("", alias="imageUrl")
    flag_open_price: bool = Field(False, alias="flagOpenPrice")
    print_zero_value: bool = Field(False, alias="printZeroValue")
    theme_menu_on_pos: str = Field("", alias="themeMenuOnPos")
    notes: str = ""
    flag_separate_print_package: bool = Field(False, alias="flagSeparatePrintPackage")
    flag_separate_tax_calculation: bool = Field(
        False, alias="flagSeparateTaxCalculation"
    )
    menu_templates: list[MenuTemplatePriceInput] = Field(
        default_factory=list, alias="menuTemplates"
    )
    update_checker_and_station: bool = Field(False, alias="updateCheckerAndStation")
    checker_list: list[CheckerInput] = Field(default_factory=list, alias="checkerList")
    menu_packages: list[MenuPackageGroupInput] = Field(
        default_factory=list, alias="menuPackages"
    )
    menu_extras: list[MenuExtraInput] = Field(default_factory=list, alias="menuExtras")
    menu_icons: list[MenuIconInput] = Field(default_factory=list, alias="menuIcons")
    menu_tags: list[MenuTagInput] = Field(default_factory=list, alias="menuTags")
    related_menus: list[RelatedMenuInput] = Field(
        default_factory=list, alias="relatedMenus"
    )


class UpdateMenuRequest(ESBBaseModel):
    """Request body for Update Menu API."""

    menu_id: int = Field(..., alias="menuID")
    menu_category_detail_id: int = Field(..., alias="menuCategoryDetailID")
    bom_id: int = Field(0, alias="bomID")
    menu_name: str = Field(..., alias="menuName")
    menu_code: str = Field(..., alias="menuCode")
    menu_short_name: str = Field("", alias="menuShortName")
    alternative_menu_name: str = Field("", alias="alternativeMenuName")
    flag_tax: int = Field(0, alias="flagTax")
    flag_other_tax: bool = Field(False, alias="flagOtherTax")
    zero_value_text: str = Field("0", alias="zeroValueText")
    sales_account: str = Field("", alias="salesAccount")
    cogs_account: str = Field("", alias="cogsAccount")
    discount_account: str = Field("", alias="discountAccount")
    description: str = ""
    image_url: str = Field("", alias="imageUrl")
    flag_open_price: bool = Field(False, alias="flagOpenPrice")
    print_zero_value: bool = Field(False, alias="printZeroValue")
    theme_menu_on_pos: str = Field("", alias="themeMenuOnPos")
    notes: str = ""
    flag_separate_print_package: bool = Field(False, alias="flagSeparatePrintPackage")
    flag_separate_tax_calculation: bool = Field(
        False, alias="flagSeparateTaxCalculation"
    )
    menu_templates: list[MenuTemplatePriceInput] = Field(
        default_factory=list, alias="menuTemplates"
    )
    update_checker_and_station: bool = Field(False, alias="updateCheckerAndStation")
    checker_list: list[CheckerInput] = Field(default_factory=list, alias="checkerList")
    menu_packages: list[MenuPackageGroupInput] = Field(
        default_factory=list, alias="menuPackages"
    )
    menu_extras: list[MenuExtraInput] = Field(default_factory=list, alias="menuExtras")
    menu_icons: list[MenuIconInput] = Field(default_factory=list, alias="menuIcons")
    menu_tags: list[MenuTagInput] = Field(default_factory=list, alias="menuTags")
    related_menus: list[RelatedMenuInput] = Field(
        default_factory=list, alias="relatedMenus"
    )


# Menu Response Models


class MenuTemplatePackageResult(ESBBaseModel):
    """Menu template package in response."""

    menu_template_id: int = Field(..., alias="menuTemplateID")
    price: Decimal | str


class MenuPackageMenuResult(ESBBaseModel):
    """Menu item within a package in response."""

    menu_id: int = Field(..., alias="menuID")
    menu_name: str = Field("", alias="menuName")
    menu_code: str = Field("", alias="menuCode")
    flag_active: int = Field(1, alias="flagActive")
    additional_price: Decimal | str = Field("0", alias="additionalPrice")
    default_item: str = Field("No", alias="defaultItem")
    menu_template_packages: list[MenuTemplatePackageResult] = Field(
        default_factory=list, alias="menuTemplatePackages"
    )


class MenuPackageGroupResult(ESBBaseModel):
    """Menu package group in response."""

    menu_group_id: int = Field(..., alias="menuGroupID")
    menu_group_name: str = Field("", alias="menuGroupName")
    flag_active: int = Field(1, alias="flagActive")
    order_id: int = Field(0, alias="orderID")
    min_qty: Decimal | str = Field("0", alias="minQty")
    max_qty: Decimal | str = Field("999999", alias="maxQty")
    notes: str = ""
    menus: list[MenuPackageMenuResult] = Field(default_factory=list)


class MenuPackagesResult(ESBBaseModel):
    """Menu packages container in response."""

    flag_separate_print_package: str = Field("No", alias="flagSeparatePrintPackage")
    flag_separate_tax_calculation: str = Field("No", alias="flagSeparateTaxCalculation")
    menu_group: list[MenuPackageGroupResult] = Field(
        default_factory=list, alias="menuGroup"
    )


class MenuExtraResult(ESBBaseModel):
    """Menu extra in response."""

    menu_extra_id: int = Field(..., alias="menuExtraID")
    menu_id: int = Field(0, alias="menuID")
    menu_extra_name: str = Field("", alias="menuExtraName")
    flag_active: int = Field(1, alias="flagActive")
    min_extra_qty: Decimal | str = Field("0", alias="minExtraQty")
    max_extra_qty: Decimal | str = Field("1", alias="maxExtraQty")
    price: Decimal | str = Field("0")


class MenuIconResult(ESBBaseModel):
    """Menu icon in response."""

    menu_icon_name: str = Field("", alias="menuIconName")
    menu_icon_url: str = Field("", alias="menuIconUrl")


class MenuTagResult(ESBBaseModel):
    """Menu tag in response."""

    tag_name: str = Field("", alias="tagName")


class RelatedMenuResult(ESBBaseModel):
    """Related menu in response."""

    menu_id: int = Field(..., alias="menuID")
    menu_name: str = Field("", alias="menuName")
    menu_code: str = Field("", alias="menuCode")


class MenuTemplateAssignment(ESBBaseModel):
    """Menu template assignment in response."""

    menu_template_id: int = Field(..., alias="menuTemplateID")
    menu_template_name: str = Field("", alias="menuTemplateName")
    flag_active: int = Field(1, alias="flagActive")
    price: Decimal | str = Field("0")


class MenuResult(ESBBaseModel):
    """Menu item in response."""

    menu_id: int = Field(..., alias="menuID")
    category_detail: str = Field("", alias="categoryDetail")
    bom_id: int = Field(0, alias="bomID")
    bom_name: str = Field("", alias="bomName")
    menu_code: str = Field("", alias="menuCode")
    menu_name: str = Field(..., alias="menuName")
    flag_active: int = Field(1, alias="flagActive")
    menu_short_name: str = Field("", alias="menuShortName")
    alternative_menu_name: str = Field("", alias="alternativeMenuName")
    flag_tax: str = Field("No", alias="flagTax")
    flag_other_tax: str = Field("No", alias="flagOtherTax")
    zero_value_text: str = Field("0", alias="zeroValueText")
    sales_account: str = Field("", alias="salesAccount")
    cogs_account: str = Field("", alias="cogsAccount")
    discount_account: str = Field("", alias="discountAccount")
    description: str = ""
    menu_image: str = Field("No Image", alias="menuImage")
    flag_open_price: str = Field("No", alias="flagOpenPrice")
    print_zero_value: str = Field("No", alias="printZeroValue")
    theme_menu_on_pos: str = Field("", alias="themeMenuOnPos")
    notes: str = ""
    menu_templates: list[MenuTemplateAssignment] = Field(
        default_factory=list, alias="menuTemplates"
    )
    menu_packages: MenuPackagesResult | None = Field(default=None, alias="menuPackages")
    menu_extras: list[MenuExtraResult] = Field(default_factory=list, alias="menuExtras")
    menu_icons: list[MenuIconResult] = Field(default_factory=list, alias="menuIcons")
    menu_tags: list[MenuTagResult] = Field(default_factory=list, alias="menuTags")
    related_menus: list[RelatedMenuResult] = Field(
        default_factory=list, alias="relatedMenus"
    )


class GetMenuResponse(ESBBaseModel):
    """Response data for Get Menu API."""

    page: str = "1"
    limit: int = 20
    count: int = 0
    data: list[MenuResult] = Field(default_factory=list)


class MenuTemplateDetailInput(ESBBaseModel):
    """Template detail for create/update requests."""

    menu_id: int = Field(..., alias="menuID")
    price: Decimal
    show_on_eso: bool = Field(False, alias="showOnEso")
    start_time: str = Field("", alias="startTime")
    end_time: str = Field("", alias="endTime")
    days: list[str] = Field(default_factory=list)


class CreateMenuTemplateRequest(ESBBaseModel):
    """Request body for Create Menu Template API."""

    menu_template_name: str = Field(..., alias="menuTemplateName")
    active_date: str = Field(..., alias="activeDate")
    notes: str = ""
    flag_inclusive: bool = Field(False, alias="flagInclusive")
    menu_template_details: list[MenuTemplateDetailInput] = Field(
        ..., alias="menuTemplateDetails"
    )


class UpdateMenuTemplateRequest(ESBBaseModel):
    """Request body for Update Menu Template API."""

    menu_template_id: int = Field(..., alias="menuTemplateID")
    menu_template_name: str = Field(..., alias="menuTemplateName")
    active_date: str = Field(..., alias="activeDate")
    notes: str = ""
    flag_inclusive: bool = Field(False, alias="flagInclusive")
    menu_template_details: list[MenuTemplateDetailInput] = Field(
        ..., alias="menuTemplateDetails"
    )


class MenuTemplateDetailResult(ESBBaseModel):
    """Template detail in response."""

    menu_template_id: int = Field(..., alias="menuTemplateID")
    menu_name: str = Field("", alias="menuName")
    before_price: Decimal = Field(Decimal("0"), alias="beforePrice")
    price: Decimal
    status: str = "Active"
    flag_show_eso: bool = Field(False, alias="flagShowEso")
    start_time: str | None = Field(None, alias="startTime")
    end_time: str | None = Field(None, alias="endTime")
    order_id: int = Field(0, alias="orderID")
    menu_template_days: list[str] = Field(
        default_factory=list, alias="menuTemplateDays"
    )


class MenuCategoryDetailSummary(ESBBaseModel):
    """Menu category detail summary in template response."""

    menu_category_detail_name: str = Field("", alias="menuCategoryDetailName")
    order_id: int = Field(0, alias="orderID")


class MenuCategorySummary(ESBBaseModel):
    """Menu category summary in template response."""

    menu_category_name: str = Field("", alias="menuCategoryName")
    order_id: int = Field(0, alias="orderID")
    menu_category_details: list[MenuCategoryDetailSummary] = Field(
        default_factory=list, alias="menuCategoryDetails"
    )


class MenuTemplateResult(ESBBaseModel):
    """Menu template in response."""

    menu_template_id: int = Field(..., alias="menuTemplateID")
    menu_template_name: str = Field(..., alias="menuTemplateName")
    active_date: str = Field("", alias="activeDate")
    notes: str = ""
    flag_inclusive: bool = Field(False, alias="flagInclusive")
    status: str = "Active"
    menu_template_details: list[MenuTemplateDetailResult] = Field(
        default_factory=list, alias="menuTemplateDetails"
    )
    menu_categories: list[MenuCategorySummary] = Field(
        default_factory=list, alias="menuCategories"
    )


class GetMenuTemplateResponse(ESBBaseModel):
    """Response data for Get Menu Template API."""

    page: str = "1"
    limit: int = 10
    count: int = 0
    data: list[MenuTemplateResult] = Field(default_factory=list)
