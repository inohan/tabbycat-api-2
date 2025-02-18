from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

from .enums import SubmitterTypeEnum

@dataclass(repr=False)
class FeedbackAnswer(BaseClass):
    question: UrlStr[FeedbackQuestion] = datafield(False, True)
    answer: str|float|int|bool = datafield(False, True)

@dataclass(repr=False)
class Feedback(IdentifiableBase):
    adjudicator: UrlStr[Adjudicator] = datafield(False, True)
    source: UrlStr[Adjudicator|Team] = datafield(False, True)
    participant_submitter: UrlStr[Adjudicator|Speaker] = datafield(False, True)
    debate: UrlStr[RoundPairing] = datafield(False, True)
    score: float|int = datafield(False, True)
    answers: list[FeedbackAnswer] = datafield(False, False)
    confirmed: bool = datafield(False, False)
    ignored: bool = datafield(False, False)
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

@dataclass(repr=False)
class PaginatedFeedbacks(PaginatedBase[Feedback]):
    _data: list[Feedback] = datafield(True, True)

from .feedback_question import FeedbackQuestion
from .adjudicator import Adjudicator
from .team import Team
from .speaker import Speaker
from .round_pairing import RoundPairing