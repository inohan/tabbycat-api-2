from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

from .enums import TeamStandingsMetricEnum

@dataclass(repr=False)
class TeamStandingMetric(BaseClass):
    metric: TeamStandingsMetricEnum = datafield(False, False)
    value: float|int = datafield(False, False)

@dataclass(repr=False)
class TeamStanding(BaseClass):
    metrics: list[TeamStandingMetric] = datafield(False, True)
    rank: int = datafield(True, True)
    tied: bool = datafield(True, True)
    team: UrlStr[Team] = datafield(True, True)

@dataclass(repr=False)
class PaginatedTeamStandings(PaginatedBase[TeamStanding]):
    _data: list[TeamStanding] = datafield(True, True)

from .team import Team