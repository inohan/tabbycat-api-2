from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

from .enums import SpeakerStandingsMetricEnum

@dataclass(repr=False)
class SpeakerStandingMetric(BaseClass):
    metric: SpeakerStandingsMetricEnum = datafield(False, False)
    value: float|int = datafield(False, False)

@dataclass(repr=False)
class SpeakerStanding(BaseClass):
    speaker: UrlStr[Speaker] = datafield(False, True)
    rank: int = datafield(True, True)
    tied: bool = datafield(True, True)
    metrics: list[SpeakerStandingMetric] = datafield(True, True)

@dataclass(repr=False)
class PaginatedSpeakerStandings(PaginatedBase[SpeakerStanding]):
    _data: list[SpeakerStanding] = datafield(True, True)

from .speaker import Speaker