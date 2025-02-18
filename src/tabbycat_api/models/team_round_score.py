from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

@dataclass(repr=False)
class Score(BaseClass):
    round: UrlStr[Round] = datafield(False, True)
    points: int = datafield(False, True)
    score: float|int = datafield(False, True)
    has_ghost: bool = datafield(False, True)

@dataclass(repr=False)
class TeamRoundScore(BaseClass):
    rounds: list[Score] = datafield(False, True)
    team: UrlStr[Team] = datafield(True, True)

@dataclass(repr=False)
class PaginatedTeamRoundScores(PaginatedBase[TeamRoundScore]):
    _data: list[TeamRoundScore] = datafield(True, True)

from .team import Team
from .round import Round