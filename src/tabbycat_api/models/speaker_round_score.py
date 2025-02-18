from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

@dataclass(repr=False)
class RoundSpeech(BaseClass):
    score: float|int = datafield(False, True)
    position: int = datafield(False, True)
    ghost: bool = datafield(False, False)

@dataclass(repr=False)
class RoundScores(BaseClass):
    round: UrlStr[Round] = datafield(False, True)
    speeches: list[RoundSpeech] = datafield(False, True)

@dataclass(repr=False)
class SpeakerRoundScore(BaseClass):
    rounds: list[RoundScores] = datafield(False, True)
    speaker: UrlStr[Speaker] = datafield(True, True)

@dataclass(repr=False)
class PaginatedSpeakerRoundScores(PaginatedBase[SpeakerRoundScore]):
    _data: list[SpeakerRoundScore] = datafield(True, True)

from .speaker import Speaker
from .round import Round