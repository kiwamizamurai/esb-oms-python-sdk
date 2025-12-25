"""Master Menu APIs for ESB OMS.

This module provides APIs for managing menu categories, menus, and menu templates.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from esb_oms.api._base import BaseAPI
from esb_oms.models.menu import (
    CreateMenuCategoryRequest,
    CreateMenuRequest,
    CreateMenuTemplateRequest,
    GetMenuCategoryResponse,
    GetMenuResponse,
    GetMenuTemplateResponse,
    MenuCategoryResult,
    MenuResult,
    MenuTemplateResult,
    UpdateMenuCategoryRequest,
    UpdateMenuRequest,
    UpdateMenuTemplateRequest,
)

if TYPE_CHECKING:
    from esb_oms._http import BearerHTTPClient


class MasterMenuCategoryAPI(BaseAPI):
    """Master Menu Category API endpoints.

    This API provides CRUD operations for menu categories.

    Example:
        ```python
        # Get menu categories
        response = client.menu_category.get(page=1)
        for category in response.data:
            print(f"Category: {category.menu_category_name}")

        # Create a menu category
        from esb_oms.models.menu import (
            CreateMenuCategoryRequest,
            MenuCategoryDetailInput,
        )

        request = CreateMenuCategoryRequest(
            menu_category_name="Beverages",
            sales_account="4100001",
            cogs_account="5100001",
            discount_account="4200001",
            menu_category_details=[
                MenuCategoryDetailInput(
                    menu_category_detail_name="Hot Drinks",
                )
            ],
        )
        result = client.menu_category.create(request)
        print(f"Created category ID: {result.menu_category_id}")
        ```
    """

    def __init__(self, http_client: BearerHTTPClient) -> None:
        """Initialize the Master Menu Category API.

        Args:
            http_client: Bearer HTTP client configured for the API URL.
        """
        super().__init__(http_client)

    def get(
        self,
        *,
        page: int = 1,
        menu_category_id: int | None = None,
    ) -> GetMenuCategoryResponse:
        """Get menu categories.

        Retrieve a paginated list of menu categories.

        Args:
            page: Page number for pagination (default: 1).
            menu_category_id: Optional filter by specific category ID.

        Returns:
            Response containing paginated menu category data.

        Raises:
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            # Get first page of categories
            response = client.menu_category.get(page=1)
            print(f"Total categories: {response.count}")
            for category in response.data:
                print(f"  - {category.menu_category_name}")

            # Get specific category
            response = client.menu_category.get(menu_category_id=123)
            ```
        """
        params: dict[str, Any] = {"page": page}
        if menu_category_id is not None:
            params["menuCategoryID"] = menu_category_id

        response = self._get("/corev1/master/get-menu-category", params=params)
        if isinstance(response, dict):
            return GetMenuCategoryResponse.model_validate(response.get("result", {}))
        msg = "Unexpected response format from get menu category API"
        raise TypeError(msg)

    def create(self, request: CreateMenuCategoryRequest) -> MenuCategoryResult:
        """Create a new menu category.

        Args:
            request: The menu category data to create.

        Returns:
            The created menu category.

        Raises:
            ESBValidationError: If the request data is invalid.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            from esb_oms.models.menu import (
                CreateMenuCategoryRequest,
                MenuCategoryDetailInput,
            )

            request = CreateMenuCategoryRequest(
                menu_category_name="Main Courses",
                sales_account="4100001",
                cogs_account="5100001",
                discount_account="4200001",
                menu_category_details=[
                    MenuCategoryDetailInput(
                        menu_category_detail_name="Rice Dishes",
                    ),
                    MenuCategoryDetailInput(
                        menu_category_detail_name="Noodles",
                    ),
                ],
            )
            result = client.menu_category.create(request)
            print(f"Created: {result.menu_category_name}")
            ```
        """
        response = self._post(
            "/corev1/master/create-menu-category",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(response, dict):
            return MenuCategoryResult.model_validate(response.get("result", {}))
        msg = "Unexpected response format from create menu category API"
        raise TypeError(msg)

    def update(self, request: UpdateMenuCategoryRequest) -> MenuCategoryResult:
        """Update an existing menu category.

        Args:
            request: The menu category data to update (must include menu_category_id).

        Returns:
            The updated menu category.

        Raises:
            ESBValidationError: If the request data is invalid.
            ESBAuthenticationError: If authentication fails.
            ESBNotFoundError: If the category does not exist.

        Example:
            ```python
            from esb_oms.models.menu import (
                UpdateMenuCategoryRequest,
                MenuCategoryDetailInput,
            )

            request = UpdateMenuCategoryRequest(
                menu_category_id=123,
                menu_category_name="Updated Category Name",
                sales_account="4100001",
                cogs_account="5100001",
                discount_account="4200001",
                menu_category_details=[
                    MenuCategoryDetailInput(
                        menu_category_detail_id=456,
                        menu_category_detail_name="Updated Detail",
                    ),
                ],
            )
            result = client.menu_category.update(request)
            ```
        """
        response = self._post(
            "/corev1/master/update-menu-category",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(response, dict):
            return MenuCategoryResult.model_validate(response.get("result", {}))
        msg = "Unexpected response format from update menu category API"
        raise TypeError(msg)


class MasterMenuAPI(BaseAPI):
    """Master Menu API endpoints.

    This API provides CRUD operations for menus.

    Example:
        ```python
        # Get menus
        response = client.menu.get(page=1)
        for menu in response.data:
            print(f"Menu: {menu.menu_name} ({menu.menu_code})")

        # Create a menu
        from esb_oms.models.menu import CreateMenuRequest
        from decimal import Decimal

        request = CreateMenuRequest(
            menu_category_detail_id=1,
            menu_name="Nasi Goreng",
            menu_code="NG001",
            flag_tax=1,
        )
        result = client.menu.create(request)
        print(f"Created menu ID: {result.menu_id}")
        ```
    """

    def __init__(self, http_client: BearerHTTPClient) -> None:
        """Initialize the Master Menu API.

        Args:
            http_client: Bearer HTTP client configured for the API URL.
        """
        super().__init__(http_client)

    def get(
        self,
        *,
        page: int = 1,
        menu_code: str | None = None,
        flag_active: int = 1,
    ) -> GetMenuResponse:
        """Get menus.

        Retrieve a paginated list of menus with optional filters.

        Args:
            page: Page number for pagination (default: 1).
            menu_code: Optional filter by menu code.
            flag_active: Filter by active status (1=Active, 0=Inactive, default: 1).

        Returns:
            Response containing paginated menu data.

        Raises:
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            # Get first page of active menus
            response = client.menu.get(page=1)
            print(f"Total menus: {response.count}")

            # Filter by menu code
            response = client.menu.get(menu_code="NG001")
            for menu in response.data:
                print(f"  - {menu.menu_name}")
            ```
        """
        params: dict[str, Any] = {"page": page, "flagActive": flag_active}
        if menu_code is not None:
            params["menuCode"] = menu_code

        response = self._get("/corev1/master/get-menu", params=params)
        if isinstance(response, dict):
            return GetMenuResponse.model_validate(response.get("result", {}))
        msg = "Unexpected response format from get menu API"
        raise TypeError(msg)

    def create(self, request: CreateMenuRequest) -> list[MenuResult]:
        """Create a new menu.

        Args:
            request: The menu data to create.

        Returns:
            List containing the created menu.

        Raises:
            ESBValidationError: If the request data is invalid.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            from esb_oms.models.menu import (
                CreateMenuRequest,
                MenuTemplatePriceInput,
                MenuPackageGroupInput,
                MenuPackageMenuInput,
            )
            from decimal import Decimal

            request = CreateMenuRequest(
                menu_category_detail_id=1,
                menu_name="Nasi Goreng Special",
                menu_code="NGS001",
                menu_short_name="Nasi Goreng",
                flag_tax=1,
                flag_other_tax=True,
                menu_templates=[
                    MenuTemplatePriceInput(
                        menu_template_id=1,
                        price=Decimal("50000"),
                    ),
                ],
            )
            results = client.menu.create(request)
            print(f"Created: {results[0].menu_name}")
            ```
        """
        response = self._post(
            "/corev1/master/create-menu",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(response, dict):
            result = response.get("result", [])
            if isinstance(result, list):
                return [MenuResult.model_validate(item) for item in result]
            return [MenuResult.model_validate(result)]
        msg = "Unexpected response format from create menu API"
        raise TypeError(msg)

    def update(self, request: UpdateMenuRequest) -> list[MenuResult]:
        """Update an existing menu.

        Args:
            request: The menu data to update (must include menu_id).

        Returns:
            List containing the updated menu.

        Raises:
            ESBValidationError: If the request data is invalid.
            ESBAuthenticationError: If authentication fails.
            ESBNotFoundError: If the menu does not exist.

        Example:
            ```python
            from esb_oms.models.menu import UpdateMenuRequest
            from decimal import Decimal

            request = UpdateMenuRequest(
                menu_id=123,
                menu_category_detail_id=1,
                menu_name="Updated Menu Name",
                menu_code="UMN001",
                flag_tax=1,
            )
            results = client.menu.update(request)
            ```
        """
        response = self._post(
            "/corev1/master/update-menu",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(response, dict):
            result = response.get("result", [])
            if isinstance(result, list):
                return [MenuResult.model_validate(item) for item in result]
            return [MenuResult.model_validate(result)]
        msg = "Unexpected response format from update menu API"
        raise TypeError(msg)


class MasterMenuTemplateAPI(BaseAPI):
    """Master Menu Template API endpoints.

    This API provides CRUD operations for menu templates.
    Menu templates define pricing and availability schedules for menus.

    Example:
        ```python
        # Get menu templates
        response = client.menu_template.get(page=1)
        for template in response.data:
            print(f"Template: {template.menu_template_name}")

        # Create a menu template
        from esb_oms.models.menu import (
            CreateMenuTemplateRequest,
            MenuTemplateDetailInput,
        )
        from decimal import Decimal

        request = CreateMenuTemplateRequest(
            menu_template_name="Dine-In Template",
            active_date="2024-01-01",
            flag_inclusive=False,
            menu_template_details=[
                MenuTemplateDetailInput(
                    menu_id=1,
                    price=Decimal("50000"),
                    show_on_eso=True,
                    days=["Monday", "Tuesday", "Wednesday"],
                ),
            ],
        )
        results = client.menu_template.create(request)
        print(f"Created template ID: {results[0].menu_template_id}")
        ```
    """

    def __init__(self, http_client: BearerHTTPClient) -> None:
        """Initialize the Master Menu Template API.

        Args:
            http_client: Bearer HTTP client configured for the API URL.
        """
        super().__init__(http_client)

    def get(
        self,
        *,
        page: int = 1,
    ) -> GetMenuTemplateResponse:
        """Get menu templates.

        Retrieve a paginated list of menu templates.

        Args:
            page: Page number for pagination (default: 1).

        Returns:
            Response containing paginated menu template data.

        Raises:
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            # Get first page of templates
            response = client.menu_template.get(page=1)
            print(f"Total templates: {response.count}")
            for template in response.data:
                print(f"  - {template.menu_template_name}")
                for detail in template.menu_template_details:
                    print(f"      Menu: {detail.menu_name}, Price: {detail.price}")
            ```
        """
        params: dict[str, Any] = {"page": page}

        response = self._get("/corev1/master/get-menu-template", params=params)
        if isinstance(response, dict):
            return GetMenuTemplateResponse.model_validate(response.get("result", {}))
        msg = "Unexpected response format from get menu template API"
        raise TypeError(msg)

    def create(self, request: CreateMenuTemplateRequest) -> list[MenuTemplateResult]:
        """Create a new menu template.

        Args:
            request: The menu template data to create.

        Returns:
            List containing the created menu template.

        Raises:
            ESBValidationError: If the request data is invalid.
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            from esb_oms.models.menu import (
                CreateMenuTemplateRequest,
                MenuTemplateDetailInput,
            )
            from decimal import Decimal

            request = CreateMenuTemplateRequest(
                menu_template_name="Take Away Template",
                active_date="2024-01-01",
                notes="Template for take away orders",
                flag_inclusive=False,
                menu_template_details=[
                    MenuTemplateDetailInput(
                        menu_id=1,
                        price=Decimal("45000"),
                        show_on_eso=True,
                        start_time="08:00",
                        end_time="22:00",
                        days=["Monday", "Tuesday", "Wednesday",
                              "Thursday", "Friday", "Saturday", "Sunday"],
                    ),
                    MenuTemplateDetailInput(
                        menu_id=2,
                        price=Decimal("35000"),
                        show_on_eso=False,
                    ),
                ],
            )
            results = client.menu_template.create(request)
            print(f"Created: {results[0].menu_template_name}")
            ```
        """
        response = self._post(
            "/corev1/master/create-menu-template",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(response, dict):
            result = response.get("result", [])
            if isinstance(result, list):
                return [MenuTemplateResult.model_validate(item) for item in result]
            return [MenuTemplateResult.model_validate(result)]
        msg = "Unexpected response format from create menu template API"
        raise TypeError(msg)

    def update(self, request: UpdateMenuTemplateRequest) -> list[MenuTemplateResult]:
        """Update an existing menu template.

        Args:
            request: The menu template data to update (must include menu_template_id).

        Returns:
            List containing the updated menu template.

        Raises:
            ESBValidationError: If the request data is invalid.
            ESBAuthenticationError: If authentication fails.
            ESBNotFoundError: If the template does not exist.

        Example:
            ```python
            from esb_oms.models.menu import (
                UpdateMenuTemplateRequest,
                MenuTemplateDetailInput,
            )
            from decimal import Decimal

            request = UpdateMenuTemplateRequest(
                menu_template_id=123,
                menu_template_name="Updated Template Name",
                active_date="2024-01-01",
                notes="Updated notes",
                flag_inclusive=False,
                menu_template_details=[
                    MenuTemplateDetailInput(
                        menu_id=1,
                        price=Decimal("55000"),
                        show_on_eso=True,
                    ),
                ],
            )
            results = client.menu_template.update(request)
            ```
        """
        response = self._post(
            "/corev1/master/update-menu-template",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(response, dict):
            result = response.get("result", [])
            if isinstance(result, list):
                return [MenuTemplateResult.model_validate(item) for item in result]
            return [MenuTemplateResult.model_validate(result)]
        msg = "Unexpected response format from update menu template API"
        raise TypeError(msg)
