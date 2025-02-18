from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, datafield

@dataclass(repr=False)
class RootLinks(BaseClass):
    v1: UrlStr[V1Root] = datafield(True, True)

@dataclass(repr=False)
class Root(IdentifiableBase):
    _links: RootLinks = datafield(True, True)
    timezone: str = datafield(True, True)
    version: str = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET"}

from .v1root import V1Root