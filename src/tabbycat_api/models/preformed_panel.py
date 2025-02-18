from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield, ResponseHandler
from .enums import PreformedPanelImportanceEnum

@dataclass(repr=False)
class PreformedPanel(IdentifiableBase):
    adjudicators: DebateAdjudicator = datafield(False, False)
    importance: PreformedPanelImportanceEnum = datafield(False, False)
    bracket_min: float|int = datafield(False, False)
    bracket_max: float|int = datafield(False, False)
    room_rank: int = datafield(False, False)
    liveness: int = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    
    #TODO: Add method support

@dataclass(repr=False)
class PaginatedPreformedPanels(PaginatedBase[PreformedPanel]):
    _data: list[PreformedPanel] = datafield(True, True)

from .debate import DebateAdjudicator