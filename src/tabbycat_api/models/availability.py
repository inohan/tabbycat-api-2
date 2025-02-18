from __future__ import annotations
from dataclasses import dataclass
from typing import override
from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

@dataclass(repr=False)
class PaginatedAvailabilities(PaginatedBase[UrlStr["Adjudicator | Team | Venue"]]):
    _data: UrlStr[list[Adjudicator | Team | Venue]] = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PUT", "PATCH"}
    #TODO: Add DELETE method
    
    @override
    async def request_get(self) -> list[Adjudicator | Team | Venue]:
        """Get availabilities of a round.

        Returns:
            list[Adjudicator  |  Team  |  Venue]: List of available objects.
        """
        return await super()._request_async("GET", params={"adjudicators": True, "teams": True, "venues": True})
    
    @override
    async def request_post(self, unavailable: list[Adjudicator | Team | Venue]) -> None:
        """Mark objects as unavailable.

        Args:
            unavailable (list[Adjudicator  |  Team  |  Venue]): List of objects to mark as unavailable.

        Returns:
            None
        """
        return await super()._request_async("POST", [obj.url for obj in unavailable])
    
    @override
    async def request_put(self, available: list[Adjudicator | Team | Venue]) -> None:
        """Mark objects as available.

        Args:
            available (list[Adjudicator  |  Team  |  Venue]): List of objects to mark as available.

        Returns:
            None
        """
        return await super()._request_async("PUT", [obj.url for obj in available])
    
    @override
    async def request_patch(self, toggle: list[Adjudicator | Team | Venue]) -> None:
        """Toggle availability of objects.

        Args:
            toggle (list[Adjudicator  |  Team  |  Venue]): List of objects to toggle availability.

        Returns:
            None
        """
        return await super()._request_async("PATCH", [obj.url for obj in toggle])

from .adjudicator import Adjudicator
from .team import Team
from .venue import Venue