from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

@dataclass(repr=False)
class VenueConstraint(BaseClass):
    category: UrlStr[VenueCategory] = datafield(False, True)
    priority: int = datafield(False, True)

from .venue_category import VenueCategory