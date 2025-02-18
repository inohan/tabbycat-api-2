from __future__ import annotations
from dataclasses import dataclass
from typing import override

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

@dataclass(repr=False)
class Checkin(IdentifiableBase):
    barcode: str = datafield(False, True)
    checked: bool = datafield(False, True)
    timestamp: str = datafield(False, True)
    object: UrlStr[Adjudicator | Speaker | Venue] = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}
    JSON_ATTRIBUTES = {
        "GET": None,
        "POST": None,
        "PUT": None,
        "PATCH": None,
        "DELETE": None
    }
    
    @override
    async def request_post(self) -> None:
        """Create object checkin identifier.

        Returns:
            None
        """
        return await super().request_post()
    
    @override
    async def request_put(self) -> None:
        """Check in object.

        Returns:
            None
        """
        return await super().request_put()
    
    @override
    async def request_patch(self) -> None:
        """Toggle object checkin status.

        Returns:
            None
        """
        return await super().request_patch(None)
    
    @override
    async def request_delete(self) -> None:
        """Check out object.

        Returns:
            None
        """
        return await super().request_delete()

from .adjudicator import Adjudicator
from .speaker import Speaker
from .venue import Venue