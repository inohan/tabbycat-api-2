from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

from .enums import PermissionsEnum

@dataclass(repr=False)
class TournamentPermissions(BaseClass):
    tournament: UrlStr[Tournament] = datafield(True, True)
    groups: UrlStr[list[Group]] = datafield(False, False)
    permissions: list[PermissionsEnum] = datafield(False, False)

@dataclass(repr=False)
class User(IdentifiableBase):
    username: str = datafield(False, True)
    password: str = datafield(False, True)
    is_superuser: bool = datafield(False, False)
    is_staff: bool = datafield(False, False)
    email: str = datafield(False, False)
    is_active: bool = datafield(False, False)
    tournaments: list[TournamentPermissions] = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    date_joined: str = datafield(True, True)
    last_login: str = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}

@dataclass(repr=False)
class PaginatedUsers(PaginatedBase[User]):
    _data: list[User] = datafield(True, True)

from .group import Group
from .tournament import Tournament