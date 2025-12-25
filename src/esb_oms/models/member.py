"""Member models for ESB OMS API."""

from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from esb_oms.models.common import ESBBaseModel


class MemberResult(ESBBaseModel):
    """Member data result."""

    member_code: str = Field("", alias="memberCode")
    member_name: str = Field("", alias="memberName")
    member_phone: str = Field("", alias="memberPhone")
    member_email: str = Field("", alias="memberEmail")
    balance: Decimal = Decimal("0")
    active_balance: Decimal = Field(Decimal("0"), alias="activeBalance")


class GetMemberResponse(ESBBaseModel):
    """Response data for Get Member API."""

    path: str = ""
    timestamp: str = ""
    code: str = ""
    status: str = ""
    message: str | None = None
    result: MemberResult | None = None
