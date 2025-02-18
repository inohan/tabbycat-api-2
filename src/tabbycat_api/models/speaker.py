from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

@dataclass(repr=False)
class SpeakerLinks(BaseClass):
    checkin: UrlStr[Checkin] = datafield(True, True)

@dataclass(repr=False)
class Speaker(IdentifiableBase):
    name: str = datafield(False, True)
    team: UrlStr[Team] = datafield(False, True)
    categories: UrlStr[list[SpeakerCategory]] = datafield(False, True)
    email: str = datafield(False, False)
    phone: str = datafield(False, False)
    anonymous: bool = datafield(False, False)
    code_name: str = datafield(False, False)
    url_key: str = datafield(False, False)
    gender: str = datafield(False, False)
    pronoun: str = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    barcode: str = datafield(True, True)
    _links: SpeakerLinks = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}

@dataclass(repr=False)
class PaginatedSpeakers(PaginatedBase[Speaker]):
    _data: list[Speaker] = datafield(True, True)

from .speaker_category import SpeakerCategory
from .team import Team
from .checkin import Checkin