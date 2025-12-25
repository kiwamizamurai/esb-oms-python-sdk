"""Authentication models for ESB OMS API."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from esb_oms.models.common import ESBBaseModel


class LoginRequest(ESBBaseModel):
    """Request body for login API.

    Attributes:
        username: ESB Core username.
        password: ESB Core password.
    """

    username: str
    password: str


class LogInfo(ESBBaseModel):
    """Login session information.

    Attributes:
        log_id: Unique identifier for the login session.
        username: Username of the logged-in user.
        login_time: Timestamp when the user logged in.
        logout_time: Timestamp when the user logged out (None if still active).
    """

    log_id: int = Field(..., alias="logID")
    username: str
    login_time: datetime = Field(..., alias="loginTime")
    logout_time: datetime | None = Field(default=None, alias="logoutTime")


class LoginResult(ESBBaseModel):
    """Result data from login API.

    Attributes:
        username: Username of the logged-in user.
        full_name: Full name of the user.
        company_id: ID of the user's company.
        company_code: Code of the user's company.
        company_name: Name of the user's company.
        access_token: JWT access token (expires after 1 hour).
        refresh_token: JWT refresh token (expires after 24 hours).
        flag_active: Whether the user account is active (1 = active).
        log_info: Login session information.
    """

    username: str
    full_name: str = Field(..., alias="fullName")
    company_id: int = Field(..., alias="companyID")
    company_code: str = Field(..., alias="companyCode")
    company_name: str = Field(..., alias="companyName")
    access_token: str = Field(..., alias="accessToken")
    refresh_token: str = Field(..., alias="refreshToken")
    flag_active: int = Field(..., alias="flagActive")
    log_info: LogInfo = Field(..., alias="logInfo")

    @property
    def is_active(self) -> bool:
        """Check if the user account is active."""
        return self.flag_active == 1


class RefreshResult(ESBBaseModel):
    """Result data from refresh token API.

    Attributes:
        username: Username of the user.
        full_name: Full name of the user.
        company_id: ID of the user's company.
        company_code: Code of the user's company.
        company_name: Name of the user's company.
        access_token: New JWT access token.
        refresh_token: New JWT refresh token.
        flag_active: Whether the user account is active.
        log_info: Login session information.
    """

    username: str
    full_name: str = Field(..., alias="fullName")
    company_id: int = Field(..., alias="companyID")
    company_code: str = Field(..., alias="companyCode")
    company_name: str = Field(..., alias="companyName")
    access_token: str = Field(..., alias="accessToken")
    refresh_token: str = Field(..., alias="refreshToken")
    flag_active: int = Field(..., alias="flagActive")
    log_info: LogInfo = Field(..., alias="logInfo")


class TokenInfo(ESBBaseModel):
    """Token information for managing authentication state.

    This is an internal model used by the client to track token state.

    Attributes:
        access_token: Current JWT access token.
        refresh_token: Current JWT refresh token.
        username: Username associated with the tokens.
        company_code: Company code associated with the tokens.
    """

    access_token: str
    refresh_token: str
    username: str | None = None
    company_code: str | None = None
