from typing import Literal

AnswerTypeEnum = Literal["bc", "bs", "i", "is", "f", "t", "tl", "ss", "ms"]

BlankEnum = Literal[""]

BreakCategoryRuleEnum = Literal["standard", "aida-1996", "aida-2016-easters", "aida-2016-australs", "aida-2019-australs-open"]

RemarkEnum = Literal["C", "I", "D", "d", "t", "w"]

GenderEnum = Literal["M", "F", "O"]

VenueCategoryDisplayEnum = Literal["-", "P", "S"]

PreformedPanelImportanceEnum = Literal[-2, -1, 0, 1, 2]

ResultStatusEnum = Literal["N", "P", "D", "C"]

RoundStageEnum = Literal["P", "E"]

RoundDrawTypeEnum = Literal["R", "M", "D", "P", "E", "S"]

RoundDrawStatusEnum = Literal["N", "D", "C", "R"]

SubmitterTypeEnum = Literal["T", "P", "A"]

SideEnum = Literal["aff", "neg", "cg", "co", "bye"]

SpeakerStandingsMetricEnum = Literal["total", "average", "trimmed_mean", "team_points", "stdev", "count", "replies_sum", "replies_avg", "replies_stdev", "replies_count", "srank"]

TeamStandingsMetricEnum = Literal["points", "wins", "speaks_sum", "speaks_avg", "speaks_ind_avg", "speaks_stddev", "draw_strength", "draw_strength_speaks", "margin_sum", "margin_avg", "npullups", "pullup_debates", "num_adjs", "firsts", "seconds", "thirds", "num_iron", "wbw"]

EmojiEnum = Literal[":)", ":("] #TODO: add all emojis

PermissionsEnum = Literal[
    "view.adjudicatorteamconflict",
    "edit.adjudicatorteamconflict",
    "view.adjudicatoradjudicatorconflict",
    "edit.adjudicatoradjudicatorconflict",
    "view.adjudicatorinstitutionconflict",
    "edit.adjudicatorinstitutionconflict",
    "view.teaminstitutionconflict",
    "edit.teaminstitutionconflict",
    "view.actionlogentry",
    "view.team",
    "add.team",
    "view.teamname",
    "view.anonymous",
    "view.adj",
    "add.adj",
    "view.room",
    "add.room",
    "view.inst",
    "add.inst",
    "view.participants",
    "view.participants.gender",
    "view.participants.contact",
    "view.participants.decoded",
    "view.participants.inst",
    "view.roundavailability.team",
    "view.roundavailability.adjudicator",
    "view.roundavailability.venue",
    "edit.roundavailability.team",
    "edit.roundavailability.adjudicator",
    "edit.roundavailability.venue",
    "view.roundavailability",
    "edit.roundavailability",
    "view.roomconstraints",
    "view.roomcategories",
    "edit.roomconstraints",
    "edit.roomcategories",
    "view.debate",
    "view.debate.admin",
    "generate.debate",
    "edit.debateteam",
    "view.debateadjudicator",
    "edit.debateadjudicator",
    "view.roomallocations",
    "edit.roomallocations",
    "edit.allocatesides",
    "view.ballotsubmission.new",
    "view.ballotsubmission.old",
    "view.ballotsubmission",
    "edit.ballotsubmission",
    "add.ballotsubmission",
    "mark.ballotsubmission",
    "mark.ballotsubmission.others",
    "view.ballotsubmission.graph",
    "view.results",
    "view.roundmotion",
    "edit.roundmotion",
    "release.draw",
    "release.motion",
    "unrelease.draw",
    "unrelease.motion",
    "edit.starttime",
    "view.draw",
    "view.briefingdraw",
    "display.motion",
    "view.tournamentpreferencemodel",
    "edit.tournamentpreferencemodel",
    "view.preformedpanels",
    "edit.preformedpanels",
    "view.standingsoverview",
    "view.teamstandings",
    "view.speakerstandings",
    "view.repliesstandings",
    "view.motionstab",
    "view.diversitytab",
    "view.feedbackoverview",
    "edit.judgescoresbulk",
    "edit.judgescoresind",
    "view.feedback",
    "edit.feedbackignore",
    "edit.feedbackconfirm",
    "view.feedbackunsubmitted",
    "add.feedback",
    "view.adj.break",
    "edit.adj.break",
    "edit.feedbackquestion",
    "edit.breakeligibility",
    "view.breakeligibility",
    "edit.breakcategories",
    "view.breakcategories",
    "view.speakercategories",
    "edit.speakercategories",
    "view.speakereligibility",
    "edit.speakereligibility",
    "view.break.overview",
    "view.break",
    "generate.break",
    "view.privateurls",
    "view.privateurls.emaillist",
    "generate.privateurls",
    "send.privateurls",
    "view.checkin",
    "edit.participantcheckin",
    "edit.roomcheckin",
    "edit.round",
    "delete.round",
    "add.round",
    "view.emails",
    "send.emails",
    "export.xml",
    "view.settings",
    "edit.settings"
]