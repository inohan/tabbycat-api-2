from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

from .enums import BreakCategoryRuleEnum
from .break_eligibility import BreakEligibility
from .breaking_team import PaginatedBreakingTeams

@dataclass(repr=False)
class BreakCategoryLinks(BaseClass):
    eligibility: UrlStr[BreakEligibility] = datafield(True, True)
    breaking_teams: UrlStr[PaginatedBreakingTeams] = datafield(True, True)

@dataclass(repr=False)
class BreakCategory(IdentifiableBase):
    name: str = datafield(False, True)
    slug: str = datafield(False, True)
    seq: int = datafield(False, True)
    break_size: int = datafield(False, True)
    is_general: bool = datafield(False, True)
    priority: int = datafield(False, True)
    limit: int = datafield(False, False)
    rule: BreakCategoryRuleEnum = datafield(False, False)
    _links: BreakCategoryLinks = datafield(True, True)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}

@dataclass(repr=False)
class PaginatedBreakCategories(PaginatedBase[BreakCategory]):
    _data: list[BreakCategory] = datafield(True, True)