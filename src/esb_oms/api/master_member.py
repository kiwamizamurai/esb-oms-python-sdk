"""Master Member API for ESB OMS.

This module provides APIs for retrieving member information.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from esb_oms.api._base import BaseAPI
from esb_oms.models.member import MemberResult

if TYPE_CHECKING:
    from esb_oms._http import BearerHTTPClient


class MasterMemberAPI(BaseAPI):
    """Master Member API endpoints.

    This API provides operations for retrieving member information
    including balance and contact details.

    Example:
        ```python
        # Search by member code
        member = client.member.get(search_member="WGG00000009")
        if member:
            print(f"Name: {member.member_name}")
            print(f"Balance: {member.balance}")
            print(f"Active Balance: {member.active_balance}")

        # Search by phone
        member = client.member.get(search_member="081234567890")

        # Search by email
        member = client.member.get(search_member="john.doe@esb.co.id")
        ```
    """

    def __init__(self, http_client: BearerHTTPClient) -> None:
        """Initialize the Master Member API.

        Args:
            http_client: Bearer HTTP client configured for the API URL.
        """
        super().__init__(http_client)

    def get(self, search_member: str) -> MemberResult | None:
        """Get member information.

        Search for a member by member code, phone number, or email address.

        Args:
            search_member: Member code, phone number, or email to search for.

        Returns:
            Member information if found, None if not found.

        Raises:
            ESBAuthenticationError: If authentication fails.

        Example:
            ```python
            # Search by member code
            member = client.member.get(search_member="WGG00000009")
            if member:
                print(f"Member: {member.member_name}")
                print(f"Code: {member.member_code}")
                print(f"Phone: {member.member_phone}")
                print(f"Email: {member.member_email}")
                print(f"Balance: {member.balance}")
                print(f"Active Balance: {member.active_balance}")
            else:
                print("Member not found")

            # Search by phone number
            member = client.member.get(search_member="081234567890")

            # Search by email
            member = client.member.get(search_member="john.doe@example.com")
            ```
        """
        response = self._get(
            "/extv1/member",
            params={"searchMember": search_member},
        )
        if isinstance(response, dict):
            result = response.get("result")
            if result:
                return MemberResult.model_validate(result)
        return None
