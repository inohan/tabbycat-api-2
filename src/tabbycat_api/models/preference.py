from __future__ import annotations
from dataclasses import dataclass

from typing import Any
from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield, ResponseHandler

def _add_url(data: dict, href: str):
    return {
        **data,
        "url": href
    }

def _add_url_paginated(data: list[dict], href: str):
    return [
        {
            **d,
            "url": f"{href}/{d['identifier']}"
        }
        for d in data
    ]

@dataclass(repr=False)
class Preference(IdentifiableBase):
    value: Any = datafield(False, True)
    section: str = datafield(True, True)
    name: str = datafield(True, True)
    identifier: str = datafield(True, True)
    default: Any = datafield(True, True)
    verbose_name: str = datafield(True, True)
    help_text: str = datafield(True, True)
    additional_data: Any = datafield(True, True)
    field: Any = datafield(True, True)
    url: str = datafield(True, True) # Manual field
    
    RESPONSE_HANDLER = ResponseHandler(
        all=_add_url,
    )
    AVAILABLE_METHODS = {"GET", "PUT", "PATCH"}
    JSON_ATTRIBUTES = {
        "PUT": {"value"}
    }


@dataclass(repr=False)
class PaginatedPreferences(PaginatedBase[Preference]):
    _data: list[Preference] = datafield(True, True)
    
    RESPONSE_HANDLER = ResponseHandler(
        all=_add_url_paginated,
    )