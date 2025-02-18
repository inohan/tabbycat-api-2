from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

@dataclass(repr=False)
class VenueLinks(BaseClass):
    checkin: UrlStr[Checkin] = datafield(True, True)

@dataclass(repr=False)
class Venue(IdentifiableBase):
    categories: UrlStr[list[VenueCategory]] = datafield(False, True)
    name: str = datafield(False, True)
    priority: int = datafield(False, True)
    external_url: str = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    _links: str = datafield(True, True)
    display_name: str = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}

@dataclass(repr=False)
class PaginatedVenues(PaginatedBase[Venue]):
    _data: list[Venue] = datafield(True, True)

from .venue_category import VenueCategory
from .checkin import Checkin