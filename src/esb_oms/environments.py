"""Environment configuration for ESB OMS API."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    class EnvironmentUrls(TypedDict):
        """URL configuration for an environment."""

        core: str
        api: str
        master_pos: str


class Environment(Enum):
    """ESB OMS API environments.

    Attributes:
        STAGING_INT: Internal staging environment for integration testing.
        STAGING: Staging environment for pre-production testing.
        PRODUCTION: Production environment.
    """

    STAGING_INT = "staging_int"
    STAGING = "staging"
    PRODUCTION = "production"


ENVIRONMENT_URLS: dict[Environment, EnvironmentUrls] = {
    Environment.STAGING_INT: {
        "core": "https://stg7.esb.co.id/core",
        "api": "https://stg7.esb.co.id/api-fnb-backend-int/web",
        "master_pos": "https://int-erp.esb.co.id",
    },
    Environment.STAGING: {
        "core": "https://stg7.esb.co.id/core-stg",
        "api": "https://stg7.esb.co.id/api-fnb-backend/web",
        "master_pos": "https://int-erp.esb.co.id",
    },
    Environment.PRODUCTION: {
        "core": "https://services.esb.co.id/core",
        "api": "https://core-api.esb.co.id",
        "master_pos": "https://esbcore.co.id",
    },
}


def get_core_url(environment: Environment) -> str:
    """Get the core API base URL for an environment.

    Args:
        environment: The target environment.

    Returns:
        The core API base URL.
    """
    return ENVIRONMENT_URLS[environment]["core"]


def get_api_url(environment: Environment) -> str:
    """Get the main API base URL for an environment.

    Args:
        environment: The target environment.

    Returns:
        The main API base URL.
    """
    return ENVIRONMENT_URLS[environment]["api"]


def get_master_pos_url(environment: Environment) -> str:
    """Get the Master POS API base URL for an environment.

    The Master POS API uses different base URLs than the main API.

    Args:
        environment: The target environment.

    Returns:
        The Master POS API base URL.
    """
    return ENVIRONMENT_URLS[environment]["master_pos"]
