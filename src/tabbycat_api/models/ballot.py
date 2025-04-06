from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

from .enums import SideEnum, SubmitterTypeEnum

@dataclass(repr=False)
class Criteria(BaseClass):
    criterion: UrlStr[ScoreCriterion] = datafield(False, True)
    score: float|int = datafield(False, True)

@dataclass(repr=False)
class Speech(BaseClass):
    score: float|int = datafield(False, True)
    speaker: UrlStr[Speaker] = datafield(False, True)
    ghost: bool = datafield(False, False)
    rank: int = datafield(False, False)
    criteria: Criteria = datafield(False, False)

@dataclass(repr=False)
class TeamResult(BaseClass):
    team: UrlStr[Team] = datafield(False, True)
    side: int | SideEnum = datafield(False, False)
    points: int = datafield(False, False)
    win: bool = datafield(False, False)
    score: float|int = datafield(False, False)
    speeches: list[Speech] = datafield(False, False)

@dataclass(repr=False)
class Sheet(BaseClass):
    teams: list[TeamResult] = datafield(False, True)
    adjudicator: UrlStr[Adjudicator] = datafield(False, False)

@dataclass(repr=False)
class Result(BaseClass):
    sheets: list[Sheet] = datafield(False, True)

@dataclass(repr=False)
class Veto(BaseClass):
    team: UrlStr[Team] = datafield(True, True)
    motion: UrlStr[Motion] = datafield(True, True)

@dataclass(repr=False)
class Ballot(IdentifiableBase):
    result: Result = datafield(False, True)
    motion: UrlStr[Motion] = datafield(False, False)
    participant_submitter: UrlStr[Adjudicator] = datafield(False, False)
    vetos: list[Veto] = datafield(False, False)
    confirmed: bool = datafield(False, False)
    discarded: bool = datafield(False, False)
    single_adj: bool = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    timestamp: str = datafield(True, True)
    version: int = datafield(True, True)
    submitter_type: SubmitterTypeEnum = datafield(True, True)
    private_url: bool = datafield(True, True)
    confirm_timestamp: str = datafield(True, True)
    ip_address: str = datafield(True, True)
    submitter: int = datafield(True, True)
    confirmer: int = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}
    JSON_ATTRIBUTES = {
        "GET": None,
        "POST": {"confirmed", "discarded"},
        "PATCH": {"confirmed", "discarded"},
        "DELETE": None
    }

class PaginatedBallots(PaginatedBase[Ballot]):
    _data: list[Ballot] = datafield(True, True)

from .adjudicator import Adjudicator
from .motion import Motion
from .speaker import Speaker
from .team import Team
from .score_criteria import ScoreCriterion