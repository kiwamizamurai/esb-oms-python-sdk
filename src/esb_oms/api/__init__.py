"""API modules for ESB OMS."""

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

__all__ = [
    "AuthAPI",
    "MasterMemberAPI",
    "MasterMenuAPI",
    "MasterMenuCategoryAPI",
    "MasterMenuTemplateAPI",
    "MasterPOSAPI",
    "MasterPromotionAPI",
    "OtherAPI",
    "ReportAPI",
    "SalesAPI",
]
