from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .base import BaseClass

class BaseCache(ABC):
    def get(self, identifier: str) -> BaseClass|None:
        pass
    
    def set(self, identifier: str, obj: BaseClass) -> None:
        pass

class ApiCache:
    _cache: dict[str, BaseClass]
    def __init__(self):
        self._cache = {}
    
    def get(self, identifier: str) -> BaseClass|None:
        return self._cache.get(identifier, None)
    
    def set(self, identifier: str, obj: BaseClass) -> None:
        if identifier in self._cache:
            raise ValueError(f"Object with identifier {identifier} already exists in cache")
        self._cache[identifier] = obj