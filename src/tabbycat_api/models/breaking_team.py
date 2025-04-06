from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

from .enums import RemarkEnum, BlankEnum
from .team import Team

@dataclass(repr=False)
class BreakingTeam(BaseClass):
    team: UrlStr[Team] = datafield(False, True)
    rank: int = datafield(False, True)
    break_rank: int = datafield(False, False)
    remark: RemarkEnum | BlankEnum = datafield(False, False)

class PaginatedBreakingTeams(PaginatedBase[BreakingTeam]):
    _data: list[BreakingTeam] = datafield(True, True)
    
    #TODO: Add methods for POST/PATCH of breaking teams