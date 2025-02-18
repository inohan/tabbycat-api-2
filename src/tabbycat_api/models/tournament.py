from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield

@dataclass(repr=False)
class TournamentLinks(BaseClass):
    rounds: UrlStr[PaginatedRounds] = datafield(True, True)
    break_categories: UrlStr[PaginatedBreakCategories] = datafield(True, True)
    speaker_categories: UrlStr[PaginatedSpeakerCategories] = datafield(True, True)
    institutions: UrlStr[PaginatedPerTournamentInstitutions] = datafield(True, True)
    teams: UrlStr[PaginatedTeams] = datafield(True, True)
    adjudicators: UrlStr[PaginatedAdjudicators] = datafield(True, True)
    speakers: UrlStr[PaginatedSpeakers] = datafield(True, True)
    venues: UrlStr[PaginatedVenues] = datafield(True, True)
    venue_categories: UrlStr[PaginatedVenueCategories] = datafield(True, True)
    motions: UrlStr[PaginatedMotions] = datafield(True, True)
    feedback: UrlStr[PaginatedFeedbacks] = datafield(True, True)
    feedback_questions: UrlStr[PaginatedFeedbackQuestions] = datafield(True, True)
    preferences: UrlStr[PaginatedPreferences] = datafield(True, True)

@dataclass(repr=False)
class Tournament(IdentifiableBase):
    name: str = datafield(False, True)
    slug: str = datafield(False, True)
    short_name: str = datafield(False, False)
    seq: int = datafield(False, False)
    active: bool = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    current_rounds: UrlStr[list[Round]] = datafield(True, True)
    _links: TournamentLinks = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}
    
    async def create[T: IdentifiableBase](self, object: T) -> T:
        if self._client is None:
            raise ValueError("This object is not associated with a client")
        from ..route_model import route_create_path
        path = self._client._config.base_url + route_create_path(type(object)).format(tournament_slug = self.slug)
        json = object.to_json("CREATE")
        resp = await self._client._request_async("POST", path, body=json)
        response_handler = type(object).RESPONSE_HANDLER.get_handler("POST") if type(object).RESPONSE_HANDLER is not None else None
        if response_handler:
            resp = response_handler(resp, resp["url"])
        obj = self._client.get_and_set_data(resp["url"], type(object), resp)
        return obj
    
    async def get_speaker_standings(self) -> PaginatedSpeakerStandings:
        """Get the speaker standings for the tournament

        Returns:
            PaginatedSpeakerStandings: Result of the request
        """
        return await self._client.get_from_url(f"{self._href}/speakers/standings")
    
    async def get_reply_standings(self) -> PaginatedSpeakerStandings:
        """Get the reply speaker standings for the tournament

        Returns:
            PaginatedTeamStandings: Result of the request
        """
        return await self._client.get_from_url(f"{self._href}/speakers/standings/replies")
    
    async def get_team_standings(self) -> PaginatedTeamStandings:
        """Get the team standings for the tournament

        Returns:
            PaginatedTeamStandings: Result of the request
        """
        return await self._client.get_from_url(f"{self._href}/teams/standings")

@dataclass(repr=False)
class PaginatedTournaments(PaginatedBase[Tournament]):
    _data: list[Tournament] = datafield(True, True)

from .institution import PaginatedPerTournamentInstitutions
from .break_category import PaginatedBreakCategories
from .round import PaginatedRounds, Round
from .motion import PaginatedMotions
from .team import PaginatedTeams
from .speaker import PaginatedSpeakers
from .adjudicator import PaginatedAdjudicators
from .speaker_category import PaginatedSpeakerCategories
from .venue_category import PaginatedVenueCategories
from .venue import PaginatedVenues
from .feedback import PaginatedFeedbacks
from .feedback_question import PaginatedFeedbackQuestions
from .preference import PaginatedPreferences
from .speaker_standing import PaginatedSpeakerStandings
from .team_standing import PaginatedTeamStandings