from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield, ResponseHandler

@dataclass(repr=False)
class Institution(IdentifiableBase):
    name:str = datafield(False, True)
    code:str = datafield(False, True)
    region:str = datafield(False, False)
    venue_constraints:list[VenueConstraint] = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}

@dataclass(repr=False)
class PaginatedInstitutions(PaginatedBase[Institution]):
    _data: list[Institution] = datafield(True, True)

@dataclass(repr=False)
class PaginatedPerTournamentInstitutions(PaginatedBase[Institution]):
    _data: list[Institution] = datafield(True, True)
    
    RESPONSE_HANDLER = ResponseHandler(
        get=lambda response, _: [{k: v for k, v in item.items() if k not in {"teams", "adjudicators"}} for item in response]
    )

from .venue_constraints import VenueConstraint