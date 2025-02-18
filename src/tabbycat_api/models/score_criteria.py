from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

@dataclass(repr=False)
class ScoreCriterion(IdentifiableBase):
    name: str = datafield(False, True)
    seq: int = datafield(False, True)
    weight: float = datafield(False, True)
    min_score: float = datafield(False, True)
    max_score: float = datafield(False, True)
    step: float = datafield(False, True)
    required: bool = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}

@dataclass(repr=False)
class PaginatedScoreCriteria(PaginatedBase[ScoreCriterion]):
    _data: list[ScoreCriterion] = datafield(True, True)