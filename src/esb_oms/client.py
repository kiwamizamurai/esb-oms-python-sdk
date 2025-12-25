"""ESB OMS API Client."""

from __future__ import annotations

from typing import TYPE_CHECKING

from esb_oms._base import BaseClient
from esb_oms.environments import Environment

if TYPE_CHECKING:
    from esb_oms.api.auth import AuthAPI
    from esb_oms.api.master_member import MasterMemberAPI
    from esb_oms.api.master_menu import (
        MasterMenuAPI,
        MasterMenuCategoryAPI,
        MasterMenuTemplateAPI,
    )
    from esb_oms.api.master_pos import MasterPOSAPI
    from esb_oms.api.master_promotion import MasterPromotionAPI
    from esb_oms.api.other import OtherAPI
    from esb_oms.api.report import ReportAPI
    from esb_oms.api.sales import SalesAPI


class ESBClient(BaseClient):
    """ESB OMS API Client.

    The main entry point for interacting with the ESB OMS API.
    Provides access to all API endpoints through property accessors.

    Example:
        ```python
        from esb_oms import ESBClient, Environment

        # Using username/password authentication
        client = ESBClient(
            username="your_username",
            password="your_password",
            environment=Environment.PRODUCTION,
        )

        # Or using static token (API key)
        client = ESBClient(
            static_token="your_api_key",
            environment=Environment.PRODUCTION,
        )

        # Access APIs
        menus = client.master.get_menu(branch_code="BR001", visit_purpose_id="1")
        client.sales.push_sales_data(sales_head=data)

        # Use as context manager for automatic cleanup
        with ESBClient(username="user", password="pass") as client:
            result = client.auth.login()
        ```

    Attributes:
        environment: The target ESB environment.
        auto_refresh: Whether to automatically refresh expired tokens.

    API Properties:
        auth: Authentication operations (login, refresh token).
        sales: Sales data operations (push sales, shift data).
        master: Master POS data (menus, branches, payment methods) - uses Basic Auth.
        menu: Menu CRUD operations.
        menu_category: Menu category CRUD operations.
        menu_template: Menu template CRUD operations.
        promotion: Promotion management.
        member: Member lookup.
        report: Sales reports and summaries.
        other: Other utilities (branch summaries, material usage).
    """

    def __init__(
        self,
        *,
        username: str | None = None,
        password: str | None = None,
        static_token: str | None = None,
        environment: Environment = Environment.PRODUCTION,
        auto_refresh: bool = True,
        timeout: float = 30.0,
    ) -> None:
        """Initialize the ESB OMS API client.

        You must provide either (username, password) or static_token for
        authentication.

        Args:
            username: ESB Core username for login authentication.
            password: ESB Core password for login authentication.
            static_token: Static API token (API key) for authentication.
            environment: Target environment (STAGING_INT, STAGING, PRODUCTION).
            auto_refresh: Automatically refresh expired access tokens.
            timeout: Request timeout in seconds (default: 30).

        Raises:
            ValueError: If neither credentials nor static token provided.

        Example:
            ```python
            # Production with username/password
            client = ESBClient(
                username="user",
                password="pass",
                environment=Environment.PRODUCTION,
            )

            # Staging with API key
            client = ESBClient(
                static_token="your_api_key",
                environment=Environment.STAGING,
            )
            ```
        """
        super().__init__(
            username=username,
            password=password,
            static_token=static_token,
            environment=environment,
            auto_refresh=auto_refresh,
            timeout=timeout,
        )

        # Lazy-loaded API instances
        self._sales: SalesAPI | None = None
        self._master: MasterPOSAPI | None = None
        self._menu: MasterMenuAPI | None = None
        self._menu_category: MasterMenuCategoryAPI | None = None
        self._menu_template: MasterMenuTemplateAPI | None = None
        self._promotion: MasterPromotionAPI | None = None
        self._member: MasterMemberAPI | None = None
        self._report: ReportAPI | None = None
        self._other: OtherAPI | None = None

    @property
    def auth(self) -> AuthAPI:
        """Access the Authentication API.

        Handles login and token refresh operations.

        Returns:
            AuthAPI instance.

        Example:
            ```python
            # Login and get tokens
            result = client.auth.login("user", "pass")
            print(f"Token: {result.access_token}")

            # Refresh token
            new_result = client.auth.refresh(result.refresh_token)
            ```
        """
        return self._auth

    @property
    def sales(self) -> SalesAPI:
        """Access the Sales API.

        Push sales data and shift data to ESB Core.
        Uses Bearer token authentication.

        Returns:
            SalesAPI instance.

        Example:
            ```python
            client.sales.push_sales_data(sales_head=data)
            client.sales.push_shift_data(shift_data=shift)
            ```
        """
        if self._sales is None:
            from esb_oms.api.sales import SalesAPI

            self._sales = SalesAPI(self._api_http)
        return self._sales

    @property
    def master(self) -> MasterPOSAPI:
        """Access the Master POS API.

        Retrieve master data for POS systems including menus, branches,
        payment methods, visit purposes, and stock information.
        Uses Basic authentication with username/password.

        Returns:
            MasterPOSAPI instance.

        Example:
            ```python
            menus = client.master.get_menu(
                branch_code="BR001",
                visit_purpose_id="1",
            )
            branches = client.master.get_branch()
            payment_methods = client.master.get_payment_method(branch_code="BR001")
            ```
        """
        if self._master is None:
            from esb_oms.api.master_pos import MasterPOSAPI

            self._master = MasterPOSAPI(self._master_pos_http)
        return self._master

    @property
    def menu(self) -> MasterMenuAPI:
        """Access the Master Menu API.

        CRUD operations for menus.
        Uses Bearer token authentication.

        Returns:
            MasterMenuAPI instance.

        Example:
            ```python
            menus = client.menu.get()
            client.menu.create(menu_data)
            client.menu.update(menu_id, updated_data)
            ```
        """
        if self._menu is None:
            from esb_oms.api.master_menu import MasterMenuAPI

            self._menu = MasterMenuAPI(self._api_http)
        return self._menu

    @property
    def menu_category(self) -> MasterMenuCategoryAPI:
        """Access the Master Menu Category API.

        CRUD operations for menu categories.
        Uses Bearer token authentication.

        Returns:
            MasterMenuCategoryAPI instance.

        Example:
            ```python
            categories = client.menu_category.get()
            client.menu_category.create(category_data)
            ```
        """
        if self._menu_category is None:
            from esb_oms.api.master_menu import MasterMenuCategoryAPI

            self._menu_category = MasterMenuCategoryAPI(self._api_http)
        return self._menu_category

    @property
    def menu_template(self) -> MasterMenuTemplateAPI:
        """Access the Master Menu Template API.

        CRUD operations for menu templates.
        Uses Bearer token authentication.

        Returns:
            MasterMenuTemplateAPI instance.

        Example:
            ```python
            templates = client.menu_template.get()
            client.menu_template.create(template_data)
            ```
        """
        if self._menu_template is None:
            from esb_oms.api.master_menu import MasterMenuTemplateAPI

            self._menu_template = MasterMenuTemplateAPI(self._api_http)
        return self._menu_template

    @property
    def promotion(self) -> MasterPromotionAPI:
        """Access the Master Promotion API.

        Create and manage promotions.
        Uses Bearer token authentication.

        Returns:
            MasterPromotionAPI instance.

        Example:
            ```python
            promos = client.promotion.list()
            client.promotion.create_discount_percentage(promo_data)
            ```
        """
        if self._promotion is None:
            from esb_oms.api.master_promotion import MasterPromotionAPI

            self._promotion = MasterPromotionAPI(self._api_http)
        return self._promotion

    @property
    def member(self) -> MasterMemberAPI:
        """Access the Master Member API.

        Retrieve member information.
        Uses Bearer token authentication.

        Returns:
            MasterMemberAPI instance.

        Example:
            ```python
            member = client.member.get(member_code="M001")
            ```
        """
        if self._member is None:
            from esb_oms.api.master_member import MasterMemberAPI

            self._member = MasterMemberAPI(self._api_http)
        return self._member

    @property
    def report(self) -> ReportAPI:
        """Access the Report API.

        Generate sales reports and summaries.
        Different endpoints use different authentication methods:
        - Sales Head, Sales Menu, Sales Menu Completion: Basic Auth (Master POS URL)
        - Sales Information, Sales Menu Summary: Bearer Token (API URL)
        - Sales Payment Summary: Bearer Token (Core URL)

        Returns:
            ReportAPI instance.

        Example:
            ```python
            # Get sales information
            sales = client.report.get_sales_information(
                sales_date_from="2024-01-01",
                sales_date_to="2024-01-31",
                branch_code="BR001",
            )

            # Get sales menu summary
            summary = client.report.get_sales_menu_summary(
                sales_date="2024-01-01",
                branch_code="BR001",
            )
            ```
        """
        if self._report is None:
            from esb_oms.api.report import ReportAPI

            self._report = ReportAPI(
                self._api_http,
                self._master_pos_http,
                self._core_bearer_http,
            )
        return self._report

    @property
    def other(self) -> OtherAPI:
        """Access other utility APIs.

        Various utility endpoints like branch summaries, material usage,
        and individual sales lookup.
        Different endpoints use different authentication methods:
        - Branch Sales Summary, Get Sales: Basic Auth (Master POS URL)
        - Daily Material Usage: Bearer Token (API URL)

        Returns:
            OtherAPI instance.

        Example:
            ```python
            # Get branch sales summary
            summaries = client.other.get_branch_sales_summary(
                sales_date_from="2024-01-01",
                sales_date_to="2024-01-31",
            )

            # Get daily material usage
            usage = client.other.get_daily_material_usage(
                sales_date="2024-01-01",
                flag_unit="stockUnit",
            )

            # Get specific sales
            sales = client.other.get_sales(bill_num="BILL001")
            ```
        """
        if self._other is None:
            from esb_oms.api.other import OtherAPI

            self._other = OtherAPI(self._api_http, self._master_pos_http)
        return self._other
