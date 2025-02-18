from __future__ import annotations
from dataclasses import dataclass
from typing import override
from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield
from .team import Team

@dataclass(repr=False)
class BreakEligibility(IdentifiableBase):
    team_set: UrlStr[list[Team]] = datafield(False, True)
    slug: str = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET"}
    #TODO: Add PUT/PATCH