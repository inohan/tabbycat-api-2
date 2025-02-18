from __future__ import annotations
from dataclasses import dataclass

from ..base import BaseClass, IdentifiableBase, UrlStr, PaginatedBase, datafield, ResponseHandler

from .enums import RoundStageEnum, RoundDrawTypeEnum, RoundDrawStatusEnum

@dataclass(repr=False)
class RoundLinks(BaseClass):
    pairing: UrlStr[PaginatedRoundPairings] = datafield(True, True)
    availabilities: UrlStr[PaginatedAvailabilities] = datafield(True, True)
    preformed_panels: UrlStr[PaginatedPreformedPanels] = datafield(True, True)

def _from_round_motion(resp: dict, href: str):
    #FIXME: Ideally, a motion may have multiple rounds
    proc = {
        **resp,
        "motions": [
            {
                **motion,
                "rounds": [
                    {
                        "round": resp["url"],
                        "seq": motion["seq"],
                    }
                ]
            }
            for motion in resp["motions"]
        ]
    }
    for motion in proc["motions"]:
        del motion["seq"]
    return proc

@dataclass(repr=False)
class Round(IdentifiableBase):
    seq: int = datafield(False, True)
    name: str = datafield(False, True)
    abbreviation: str = datafield(False, True)
    draw_type: RoundDrawTypeEnum = datafield(False, True)
    break_category: UrlStr[BreakCategory] = datafield(False, False)
    motions: list[Motion] = datafield(False, False) #Process RoundMotion
    starts_at: str = datafield(False, False)
    completed: bool = datafield(False, False)
    stage: RoundStageEnum = datafield(False, False)
    draw_status:RoundDrawStatusEnum = datafield(False, False)
    feedback_weight: float|int = datafield(False, False)
    silent: bool = datafield(False, False)
    motions_released: bool = datafield(False, False)
    weight: float|int = datafield(False, False)
    id: int = datafield(True, True)
    url: str = datafield(True, True)
    _links: RoundLinks = datafield(True, True)
    
    AVAILABLE_METHODS = {"GET", "POST", "PATCH", "DELETE"}
    RESPONSE_HANDLER = ResponseHandler(
        _from_round_motion
    )

@dataclass(repr=False)
class PaginatedRounds(PaginatedBase[Round]):
    _data: list[Round] = datafield(True, True)
    
    RESPONSE_HANDLER = ResponseHandler(
        all=lambda resp, _: [_from_round_motion(round, _) for round in resp]
    )

from .break_category import BreakCategory
from .motion import Motion
from .round_pairing import PaginatedRoundPairings
from .availability import PaginatedAvailabilities
from .preformed_panel import PaginatedPreformedPanels