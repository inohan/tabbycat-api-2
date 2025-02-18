from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield, ResponseHandler

from .enums import EmojiEnum, BlankEnum

def _from_team_speaker(resp_team: dict, href: str):
    resp_process = {
        **resp_team,
        "speakers": [
            {
                **speaker,
                "team": resp_team["url"]
            }
            for speaker in resp_team["speakers"]
        ]
    }
    return resp_process

@dataclass(repr=False)
class Team(IdentifiableBase):
    institution: UrlStr[Institution | None] = datafield(False, False)
    break_categories: UrlStr[list[BreakCategory]] = datafield(False, False)
    institution_conflicts: UrlStr[list[Institution]] = datafield(False, False)
    venue_constraints: list[VenueConstraint] = datafield(False, False)
    reference: str = datafield(False, False)
    short_reference: str = datafield(False, False)
    code_name: str = datafield(False, False)
    use_institution_prefix: bool = datafield(False, False)
    seed: int = datafield(False, False)
    emoji: EmojiEnum | BlankEnum = datafield(False, False)
    speakers: list[Speaker] = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    short_name: str = datafield(True, True)
    long_name: str = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}
    JSON_ATTRIBUTES = {
        "GET": None,
        "POST": {"institution", "break_categories", "institution_conflicts", "venue_constraints", "reference", "short_reference", "code_name", "use_institution_prefix", "seed", "emoji"},
        "PATCH": {"institution", "break_categories", "institution_conflicts", "venue_constraints", "reference", "short_reference", "code_name", "use_institution_prefix", "seed", "emoji"},
        "DELETE": None
    }
    RESPONSE_HANDLER = ResponseHandler(
        all=_from_team_speaker
    )

@dataclass(repr=False)
class PaginatedTeams(PaginatedBase[Team]):
    _data: list[Team] = datafield(True, True)
    
    RESPONSE_HANDLER = ResponseHandler(
        all=lambda resp, _: [_from_team_speaker(team, _) for team in resp]
    )

from .institution import Institution
from .break_category import BreakCategory
from .venue_constraints import VenueConstraint
from .speaker import Speaker
