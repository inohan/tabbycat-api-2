from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

@dataclass(repr=False)
class SpeakerCategoryLinks(BaseClass):
    eligibility: UrlStr[SpeakerEligibility] = datafield(True, True)

@dataclass(repr=False)
class SpeakerCategory(IdentifiableBase):
    name: str = datafield(False, True)
    slug: str = datafield(False, True)
    seq: int = datafield(False, True)
    limit: int = datafield(False, False)
    public: bool = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    _links: SpeakerCategoryLinks = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}

@dataclass(repr=False)
class PaginatedSpeakerCategories(PaginatedBase[SpeakerCategory]):
    _data: list[SpeakerCategory] = datafield(True, True)

from .speaker_eligibility import SpeakerEligibility