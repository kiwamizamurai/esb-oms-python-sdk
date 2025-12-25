# ESB OMS Python Client

A Python client library for the [ESB OMS (Order Management System) API](https://developers.esb.co.id/esb-oms/).

> [!NOTE]
> This library provides a type-safe interface to the ESB OMS API with automatic token management.
> For detailed API specifications, refer to the [official documentation](https://developers.esb.co.id/esb-oms/).

## Installation

```bash
pip install esb-oms
```

## Quick Start

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

# Get menu data
menus = client.master.get_menu(branch_code="BR001", visit_purpose_id="1")
for category in menus:
    print(f"Category: {category.menu_category_desc}")
    for detail in category.menu_category_details:
        for menu in detail.menus:
            print(f"  - {menu.menu_name}: {menu.price}")

# Push sales data
from esb_oms.models import SalesHead, SalesMenuItem, Payment
from decimal import Decimal

sales_head = SalesHead(
    sales_num="S001",
    bill_num="B001",
    branch_code="BR001",
    visit_purpose_id=1,
    sales_date="2024-01-01",
    sales_date_in="2024-01-01 12:00:00",
    sales_date_out="2024-01-01 12:30:00",
    subtotal=Decimal("100000"),
    grand_total=Decimal("110000"),
    payment_total=Decimal("110000"),
    status_id=8,
    sales_menus=[
        SalesMenuItem(
            menu_id=1,
            menu_code="M001",
            qty=1,
            price=Decimal("100000"),
            original_price=Decimal("100000"),
            total=Decimal("110000"),
            status_id=14,
        ),
    ],
    payments=[
        Payment(
            payment_method_id=1,
            payment_method_name="Cash",
            payment_amount=Decimal("110000"),
        ),
    ],
)

result = client.sales.push_sales_data(sales_head=sales_head)
print(f"Sales pushed: {result}")
```

## API Reference

### Client Initialization

> [!CAUTION]
> Always verify you are using the correct environment.
> Using `Environment.PRODUCTION` will affect real business data.

```python
from esb_oms import ESBClient, Environment

# Available environments
Environment.PRODUCTION     # Production environment
Environment.STAGING        # Staging environment
Environment.STAGING_INT    # Internal staging environment

# With credentials (recommended for server-side)
client = ESBClient(
    username="your_username",
    password="your_password",
    environment=Environment.PRODUCTION,
    auto_refresh=True,  # Automatically refresh tokens
    timeout=30.0,       # Request timeout in seconds
)

# With static token (API key)
client = ESBClient(
    static_token="your_api_key",
    environment=Environment.PRODUCTION,
)

# Using as context manager
with ESBClient(username="user", password="pass") as client:
    menus = client.master.get_menu(branch_code="BR001", visit_purpose_id="1")
```

### Available APIs

| API | Description | Authentication | Documentation |
|-----|-------------|----------------|---------------|
| `client.auth` | Login and token refresh | N/A | [Auth API](https://developers.esb.co.id/esb-oms/#api-Authorization) |
| `client.sales` | Push sales and shift data | Bearer Token | [Push Sales API](https://developers.esb.co.id/esb-oms/#api-Push_Sales_Data) |
| `client.master` | Master POS data (menus, branches, etc.) | Basic Auth | [Master POS API](https://developers.esb.co.id/esb-oms/#api-Master_POS) |
| `client.menu` | Menu CRUD operations | Bearer Token | [Master Menu API](https://developers.esb.co.id/esb-oms/#api-Master_Menu) |
| `client.menu_category` | Menu category CRUD operations | Bearer Token | [Menu Category API](https://developers.esb.co.id/esb-oms/#api-Master_Menu_Category) |
| `client.menu_template` | Menu template CRUD operations | Bearer Token | [Menu Template API](https://developers.esb.co.id/esb-oms/#api-Master_Menu_Template) |
| `client.promotion` | Promotion management | Bearer Token | [Promotion API](https://developers.esb.co.id/esb-oms/#api-Master_Promotion) |
| `client.member` | Member lookup | Bearer Token | [Member API](https://developers.esb.co.id/esb-oms/#api-Master_Member) |
| `client.report` | Sales reports and summaries | Mixed | [Report API](https://developers.esb.co.id/esb-oms/#api-Report) |
| `client.other` | Utility APIs | Mixed | [Other API](https://developers.esb.co.id/esb-oms/#api-Other) |

### Authentication API

> [!TIP]
> When using `auto_refresh=True` (default), the client automatically handles token refresh.
> Manual login is only needed for explicit token management.

```python
# Manual login (usually not needed if using auto_refresh)
client.login()

# Refresh token
client.refresh_token()

# Check authentication status
if client.is_authenticated:
    print("Client is authenticated")
```

### Sales API

> [!WARNING]
> Ensure all required fields are populated before pushing sales data.
> Invalid data will result in `ESBValidationError`.

```python
# Push sales data
result = client.sales.push_sales_data(sales_head=sales_head)

# Push shift data
result = client.sales.push_shift_data(shift_data=shift_data)
```

### Master POS API

```python
# Get menus for a branch
menus = client.master.get_menu(branch_code="BR001", visit_purpose_id="1")

# Get branches
branches = client.master.get_branch()

# Get payment methods
payment_methods = client.master.get_payment_method(branch_code="BR001")

# Get visit purposes
purposes = client.master.get_visit_purpose()

# Get stock by branch
stocks = client.master.get_stock_branch(branch_code="BR001")
```

### Menu API

```python
# Get menus
response = client.menu.get(page=1, menu_code="M001")

# Create menu
from esb_oms.models import CreateMenuRequest
request = CreateMenuRequest(
    menu_category_detail_id=1,
    menu_name="New Menu",
    menu_code="NM001",
    flag_tax=1,
)
result = client.menu.create(request)

# Update menu
from esb_oms.models import UpdateMenuRequest
request = UpdateMenuRequest(
    menu_id=123,
    menu_category_detail_id=1,
    menu_name="Updated Menu",
    menu_code="NM001",
    flag_tax=1,
)
result = client.menu.update(request)
```

### Menu Category API

```python
# Get categories
response = client.menu_category.get(page=1)

# Create category
from esb_oms.models import CreateMenuCategoryRequest, MenuCategoryDetailInput
request = CreateMenuCategoryRequest(
    menu_category_name="Beverages",
    sales_account="4100001",
    cogs_account="5100001",
    discount_account="4200001",
    menu_category_details=[
        MenuCategoryDetailInput(menu_category_detail_name="Hot Drinks"),
    ],
)
result = client.menu_category.create(request)
```

### Menu Template API

```python
# Get templates
response = client.menu_template.get(page=1)

# Create template
from esb_oms.models import CreateMenuTemplateRequest, MenuTemplateDetailInput
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
        ),
    ],
)
result = client.menu_template.create(request)
```

### Promotion API

```python
# List promotions
promotions = client.promotion.list(page=1)

# Create discount percentage promotion
from esb_oms.models import CreateDiscountPercentageRequest
from decimal import Decimal

request = CreateDiscountPercentageRequest(
    promotion_master_code="PROMO001",
    branch_code="BR001",
    discount=Decimal("10"),
    start_date="2024-01-01",
    end_date="2024-12-31",
    all_categories=True,
)
result = client.promotion.create_discount_percentage(request)

# Other promotion types
client.promotion.create_discount_limit_percentage(request)
client.promotion.create_free_item(request)
client.promotion.create_discount_percentage_eso(request)
client.promotion.create_discount_amount_eso(request)
```

### Member API

```python
# Search member by code, phone, or email
member = client.member.get(search_member="WGG00000009")
if member:
    print(f"Name: {member.member_name}")
    print(f"Balance: {member.balance}")
```

### Report API

```python
# Get sales information
sales = client.report.get_sales_information(
    sales_date_from="2024-01-01",
    sales_date_to="2024-01-31",
    branch_code="BR001",
)

# Get sales head
heads = client.report.get_sales_head(
    sales_date_from="2024-01-01",
    sales_date_to="2024-01-31",
)

# Get sales menu summary
summary = client.report.get_sales_menu_summary(
    sales_date="2024-01-01",
    branch_code="BR001",
)

# Get sales payment summary
payments = client.report.get_sales_payment_summary(
    sales_date="2024-01-01",
    branch_code="BR001",
)
```

### Other API

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
    branch_code="BR001",
)

# Get specific sales
sales = client.other.get_sales(bill_num="BILL001")
```

## Error Handling

> [!IMPORTANT]
> Always wrap API calls in try-except blocks to handle potential errors gracefully.
> Each error type provides additional context via `code`, `status_code`, and `response_data` attributes.

```python
from esb_oms import (
    ESBError,
    ESBAuthenticationError,
    ESBAuthorizationError,
    ESBValidationError,
    ESBNotFoundError,
    ESBMethodNotAllowedError,
    ESBRateLimitError,
    ESBServerError,
)

try:
    result = client.sales.push_sales_data(sales_head=data)
except ESBAuthenticationError as e:
    print(f"Authentication failed: {e}")
except ESBValidationError as e:
    print(f"Validation error: {e}")
    # Access detailed validation errors
    # validation_errors can be a list of strings or a dict of field -> errors
    if e.validation_errors:
        print(f"Details: {e.validation_errors}")
except ESBNotFoundError as e:
    print(f"Resource not found: {e}")
except ESBMethodNotAllowedError as e:
    print(f"Method not allowed: {e}")
except ESBRateLimitError as e:
    print(f"Rate limited: {e}")
except ESBServerError as e:
    print(f"Server error: {e}")
except ESBError as e:
    print(f"API error: {e}")
```

## Development

### Requirements

- Python 3.11+
- uv (for dependency management)

### Setup

```bash
uv sync --dev
```

### Code Quality

```bash
poe lint        # Check code
poe fix         # Auto-fix issues
poe format      # Format code
poe typecheck   # Type checking
poe check       # Run all checks
```

## Requirements

- Python 3.11+
- pydantic >= 2.0, < 3.0
- httpx >= 0.27, < 1.0

## License

MIT License

## Links

- [ESB OMS API Documentation](https://developers.esb.co.id/esb-oms/)
