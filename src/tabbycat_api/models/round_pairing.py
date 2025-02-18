from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield
from .enums import ResultStatusEnum

@dataclass(repr=False)
class PairingLinks(BaseClass):
    ballots: UrlStr[PaginatedBallots] = datafield(True, True)

@dataclass(repr=False)
class RoundPairing(IdentifiableBase):
    teams: list[DebateTeam] = datafield(False, True)
    venue: UrlStr[Venue] = datafield(False, False)
    adjudicators: DebateAdjudicator = datafield(False, False)
    bracket: float|int = datafield(False, False)
    room_rank: int = datafield(False, False)
    importance: int = datafield(False, False)
    result_status: ResultStatusEnum = datafield(False, False)
    sides_confirmed: bool = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    _links: PairingLinks = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}

@dataclass(repr=False)
class PaginatedRoundPairings(PaginatedBase[RoundPairing]):
    _data: list[RoundPairing] = datafield(True, True)

from .debate import DebateTeam, DebateAdjudicator
from .venue import Venue
from .ballot import PaginatedBallots