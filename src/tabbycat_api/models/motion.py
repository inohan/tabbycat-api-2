from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

@dataclass(repr=False)
class MotionRound(BaseClass):
    round: UrlStr[Round] = datafield(False, True)
    seq: int = datafield(False, False)

@dataclass(repr=False)
class Motion(IdentifiableBase):
    rounds: list[MotionRound] = datafield(False, True)
    text: str = datafield(False, True)
    reference: str = datafield(False, True)
    info_slide: str = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    info_slide_plain: str = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}

@dataclass(repr=False)
class PaginatedMotions(PaginatedBase[Motion]):
    _data: list[Motion] = datafield(True, True)

from .round import Round