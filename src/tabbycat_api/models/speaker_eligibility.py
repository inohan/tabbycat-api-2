from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

@dataclass(repr=False)
class SpeakerEligibility(IdentifiableBase):
    slug: str = datafield(True, True)
    speaker_set: UrlStr[list[Speaker]] = datafield(False, True)

from .speaker import Speaker