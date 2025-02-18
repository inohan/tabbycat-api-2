from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

from .enums import VenueCategoryDisplayEnum

@dataclass(repr=False)
class VenueCategory(IdentifiableBase):
    venues: UrlStr[list[Venue]] = datafield(False, True)
    name: str = datafield(False, True)
    description: str = datafield(False, False)
    display_in_venue_name: VenueCategoryDisplayEnum = datafield(False, False)
    display_in_public_tooltip: bool = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}

@dataclass(repr=False)
class PaginatedVenueCategories(PaginatedBase[VenueCategory]):
    _data: list[VenueCategory] = datafield(True, True)

from .venue import Venue