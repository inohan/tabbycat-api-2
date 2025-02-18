from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield
from .enums import SideEnum

@dataclass(repr=False)
class DebateAdjudicator(BaseClass):
    chair: UrlStr[Adjudicator] = datafield(False, True)
    panellists: UrlStr[list[Adjudicator]] = datafield(False, True)
    trainees: UrlStr[list[Adjudicator]] = datafield(False, True)

@dataclass(repr=False)
class DebateTeam(BaseClass):
    team: Team = datafield(False, True)
    side: int|SideEnum = datafield(False, False)

from .team import Team
from .adjudicator import Adjudicator