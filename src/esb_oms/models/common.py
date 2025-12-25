"""Common Pydantic models for ESB OMS API."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

# Type variable for generic response result
T = TypeVar("T")


class ESBBaseModel(BaseModel):
    """Base model with common configuration for all ESB models.

    This model is configured to:
    - Support both camelCase (API) and snake_case (Python) field names
    - Validate data on assignment
    - Forbid extra fields to catch API changes early
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",  # Ignore extra fields for forward compatibility
        str_strip_whitespace=True,
    )


class APIResponse(ESBBaseModel, Generic[T]):
    """Standard API response wrapper.

    All ESB OMS API responses follow this structure:

    ```json
    {
        "path": "https://...",
        "timestamp": "2024-05-20 13:35:29",
        "status": "ok",
        "code": "EC03100000",
        "message": "OK",
        "result": { ... },
        "errors": null
    }
    ```

    Attributes:
        path: The API endpoint URL that was called.
        timestamp: When the request was processed.
        status: Response status ("ok" or "fail").
        code: ESB API status code.
        message: Human-readable message.
        result: The actual response data (type varies by endpoint).
        errors: Error details if status is "fail".
    """

    path: str
    timestamp: str
    status: str
    code: str
    message: str
    result: T | None = None
    errors: list[dict[str, Any]] | None = None

    @property
    def is_success(self) -> bool:
        """Check if the response indicates success."""
        return self.status.lower() == "ok"


class PaginatedResult(ESBBaseModel, Generic[T]):
    """Paginated result container.

    Attributes:
        items: List of items in the current page.
        total: Total number of items across all pages.
        page: Current page number (1-based).
        page_size: Number of items per page.
        total_pages: Total number of pages.
    """

    items: list[T]
    total: int = Field(default=0, alias="totalData")
    page: int = Field(default=1)
    page_size: int = Field(default=10, alias="pageSize")
    total_pages: int = Field(default=1, alias="totalPage")

    @property
    def has_next(self) -> bool:
        """Check if there are more pages after the current one."""
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        """Check if there are pages before the current one."""
        return self.page > 1


class DateRange(ESBBaseModel):
    """Date range for filtering.

    Attributes:
        start_date: Start date of the range.
        end_date: End date of the range.
    """

    start_date: datetime = Field(..., alias="startDate")
    end_date: datetime = Field(..., alias="endDate")


class BranchFilter(ESBBaseModel):
    """Branch filter for requests.

    Attributes:
        branch_id: Branch ID to filter by.
        branch_code: Branch code to filter by.
    """

    branch_id: int | None = Field(default=None, alias="branchID")
    branch_code: str | None = Field(default=None, alias="branchCode")
