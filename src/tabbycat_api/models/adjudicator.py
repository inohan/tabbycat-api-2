from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield
from .enums import GenderEnum, BlankEnum

@dataclass(repr=False)
class AdjudicatorLinks(BaseClass):
    checkin: UrlStr[Checkin] = datafield(True, True)

@dataclass(repr=False)
class Adjudicator(IdentifiableBase):
    name: str = datafield(False, True)
    institution: UrlStr[Institution | None] = datafield(False, True)
    institution_conflicts: UrlStr[list[Institution]] = datafield(False, True)
    team_conflicts: UrlStr[list[Team]] = datafield(False, True)
    adjudicator_conflicts: UrlStr[list[Adjudicator]] = datafield(False, False)
    venue_constraints: list[VenueConstraint] = datafield(False, False)
    email: str = datafield(False, False)
    phone: str = datafield(False, False)
    anonymous: bool = datafield(False, False)
    code_name: str = datafield(False, False)
    url_key: str = datafield(False, False)
    gender: GenderEnum|BlankEnum = datafield(False, False)
    pronoun: str = datafield(False, False)
    base_score: float = datafield(False, False)
    trainee: bool = datafield(False, False)
    breaking: bool = datafield(False, False)
    independent: bool = datafield(False, False)
    adj_core: bool = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    _links: AdjudicatorLinks = datafield(True, True)
    barcode: str = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}

@dataclass(repr=False)
class PaginatedAdjudicators(PaginatedBase[Adjudicator]):
    _data: list[Adjudicator] = datafield(True, True)

from .institution import Institution
from .venue_constraints import VenueConstraint
from .checkin import Checkin
from .team import Team