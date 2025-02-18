from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

from .enums import PermissionsEnum

@dataclass(repr=False)
class Group(IdentifiableBase):
    name: str = datafield(False, True)
    permissions: list[PermissionsEnum] = datafield(False, False)
    id: str = datafield(True, True)
    url: str = datafield(True, True)
    users: list[int] = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}

@dataclass(repr=False)
class PaginatedGroups(PaginatedBase[Group]):
    _data: list[Group] = datafield(True, True)