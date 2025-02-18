from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

@dataclass(repr=False)
class V1Links(BaseClass):
    tournaments: UrlStr[PaginatedTournaments] = datafield(True, True)
    institutions: UrlStr[PaginatedInstitutions] = datafield(True, True)
    users: UrlStr[PaginatedUsers] = datafield(True, True)

@dataclass(repr=False)
class V1Root(IdentifiableBase):
    _links: V1Links = datafield(True, True)

from .tournament import PaginatedTournaments
from .institution import PaginatedInstitutions
from .user import PaginatedUsers