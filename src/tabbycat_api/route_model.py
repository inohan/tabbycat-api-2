from __future__ import annotations
from typing import TYPE_CHECKING
from urllib.parse import urlparse
from . import models

if TYPE_CHECKING:
    from .base import IdentifiableBase

MODEL_URL = {
    "api": {
        "": models.Root,
        "v1": {
            "": models.V1Root,
            "tournaments": {
                "": models.PaginatedTournaments,
                "*": {
                    "": models.Tournament,
                    "institutions": {
                        "": models.PaginatedPerTournamentInstitutions
                    },
                    "rounds": {
                        "": models.PaginatedRounds,
                        "*": {
                            "": models.Round,
                            "pairings": {
                                "": models.PaginatedRoundPairings,
                                "*": {
                                    "": models.RoundPairing,
                                    "ballots": {
                                        "": models.PaginatedBallots,
                                        "*": {
                                            "": models.Ballot
                                        }
                                    }
                                }
                            },
                            "availabilities": {
                                "": models.PaginatedAvailabilities
                            },
                            "preformed-panels": {
                                "": models.PaginatedPreformedPanels,
                                "*": {
                                    "": models.PreformedPanel
                                }
                            }
                        }
                    },
                    "break-categories": {
                        "": models.PaginatedBreakCategories,
                        "*": {
                            "": models.BreakCategory,
                            "eligibility": {
                                "": models.BreakEligibility
                            },
                            "break": {
                                "": models.PaginatedBreakingTeams
                            }
                        }
                    },
                    "speaker-categories": {
                        "": models.PaginatedSpeakerCategories,
                        "*": {
                            "": models.SpeakerCategory,
                            "eligibility": {
                                "": models.SpeakerEligibility
                            }
                        }
                    },
                    "teams": {
                        "": models.PaginatedTeams,
                        "standings": {
                            "": models.PaginatedTeamStandings,
                            "rounds": {
                                "": models.PaginatedTeamRoundScores
                            }
                        },
                        "*": {
                            "": models.Team,
                        }
                    },
                    "adjudicators": {
                        "": models.PaginatedAdjudicators,
                        "*": {
                            "": models.Adjudicator,
                            "checkin": {
                                "": models.Checkin
                            }
                        }
                    },
                    "score-criteria": {
                        "": models.PaginatedScoreCriteria,
                        "*": {
                            "": models.ScoreCriterion
                        }
                    },
                    "speakers": {
                        "": models.PaginatedSpeakers,
                        "standings": {
                            "": models.PaginatedSpeakerStandings,
                            "replies": {
                                "": models.PaginatedSpeakerStandings
                            },
                            "rounds": {
                                "": models.PaginatedSpeakerRoundScores
                            }
                        },
                        "*": {
                            "": models.Speaker,
                            "checkin": {
                                "": models.Checkin
                            }
                        }
                    },
                    "venues": {
                        "": models.PaginatedVenues,
                        "*": {
                            "": models.Venue,
                            "checkin": {
                                "": models.Checkin
                            }
                        }
                    },
                    "venue-categories": {
                        "": models.PaginatedVenueCategories,
                        "*": {
                            "": models.VenueCategory
                        }
                    },
                    "motions": {
                        "": models.PaginatedMotions,
                        "*": {
                            "": models.Motion
                        }
                    },
                    "feedback": {
                        "": models.PaginatedFeedbacks,
                        "*": {
                            "": models.Feedback,
                        }
                    },
                    "feedback-questions": {
                        "": models.PaginatedFeedbackQuestions,
                        "*": {
                            "": models.FeedbackQuestion,
                        }
                    },
                    "preferences": {
                        "": models.PaginatedPreferences,
                        "*": {
                            "": models.Preference,
                        }
                    }
                }
            },
            "institutions": {
                "": models.PaginatedInstitutions,
                "*": {
                    "": models.Institution
                }
            },
            "user-groups": {
                "": models.PaginatedGroups,
                "*": {
                    "": models.Group
                }
            },
            "users": {
                "": models.PaginatedUsers,
                "*": {
                    "": models.User
                }
            }
        }
    }
}

CREATE_URL: dict[IdentifiableBase, str] = {
    models.Institution: "/api/v1/institutions",
    models.Adjudicator: "/api/v1/tournaments/{tournament_slug}/adjudicators",
    models.BreakCategory: "/api/v1/tournaments/{tournament_slug}/break-categories",
    models.Team: "/api/v1/tournaments/{tournament_slug}/teams",
    models.Speaker: "/api/v1/tournaments/{tournament_slug}/speakers",
    models.SpeakerCategory: "/api/v1/tournaments/{tournament_slug}/speaker-categories",
    models.Venue: "/api/v1/tournaments/{tournament_slug}/venues",
    models.VenueCategory: "/api/v1/tournaments/{tournament_slug}/venue-categories",
}

def route_model(url: str) -> type[IdentifiableBase]:
    path = urlparse(url).path
    split = path.split("/")[1:]
    cur = MODEL_URL
    for part in split:
        if part in cur:
            cur = cur[part]
        elif "*" in cur:
            cur = cur["*"]
        else:
            raise ValueError(f"Invalid URL: {url}")
    if "" in cur:
        return cur[""]
    else:
        raise ValueError(f"Invalid URL: {url}")

def route_create_path(type_: type[IdentifiableBase]) -> str:
    return CREATE_URL[type_]