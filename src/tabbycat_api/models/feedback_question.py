from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

from .enums import AnswerTypeEnum

@dataclass(repr=False)
class FeedbackQuestion(IdentifiableBase):
    seq: int = datafield(False, True)
    text: str = datafield(False, True)
    name: str = datafield(False, True)
    reference: str = datafield(False, True)
    from_adj: bool = datafield(False, True)
    from_team: bool = datafield(False, True)
    answer_type: AnswerTypeEnum = datafield(False, True)
    required: bool = datafield(False, False)
    min_value: float|int = datafield(False, False)
    max_value: float|int = datafield(False, False)
    choices: list[str] = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}

@dataclass(repr=False)
class PaginatedFeedbackQuestions(PaginatedBase[FeedbackQuestion]):
    _data: list[FeedbackQuestion] = datafield(True, True)