import tabbycat_api as tc
import asyncio
from dotenv import load_dotenv
import pytest
import os

load_dotenv()

TEST_ENDPOINT = os.getenv("TEST_ENDPOINT")
TEST_TOKEN = os.getenv("TEST_TOKEN")
TEST_TOURNAMENT_SLUG = os.getenv("TEST_TOURNAMENT_SLUG")

def random_string(length=10):
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@pytest.fixture
def setup_client():
    client = tc.Client(
        tc.ClientConfig(
            TEST_ENDPOINT,
            TEST_TOKEN,
            True,
            20
        )
    )
    yield client

@pytest.mark.asyncio
async def test_institution(setup_client):
    client: tc.Client = setup_client
    tournament = await client.get_tournament(TEST_TOURNAMENT_SLUG)
    rand_name = random_string(10)
    institution = tc.models.Institution(
        name=f"Test Institution {rand_name}",
        code=f"Test {rand_name}",
    )
    # Test for creation
    inst_created = await tournament.create(institution)
    assert inst_created._loaded
    assert inst_created.id
    assert inst_created.name == f"Test Institution {rand_name}"
    assert inst_created.code == f"Test {rand_name}"
    # Test for POST
    inst_created.name = f"POST Institution {rand_name}"
    await inst_created.request_post()
    assert inst_created.name == f"POST Institution {rand_name}"
    # Test for PATCH
    await inst_created.request_patch(
        tc.models.Institution(
            name=f"PATCH Institution {rand_name}",
            code=f"Patch {rand_name}"
        )
    )
    assert inst_created.name == f"PATCH Institution {rand_name}"
    assert inst_created.code == f"Patch {rand_name}"
    # Test for DELETE
    await inst_created.request_delete()

@pytest.mark.asyncio
async def test_team(setup_client):
    client: tc.Client = setup_client
    tournament = await client.get_tournament(TEST_TOURNAMENT_SLUG)
    institutions = asyncio.create_task(tournament._links.institutions.load())
    rand_name = random_string(10)
    team = tc.models.Team(
        reference=f"Test Team {rand_name}",
        short_reference=f"Test Team {rand_name}",
        institution=None,
        speakers=[
            tc.models.Speaker(
                name="Speaker 1",
                email="speaker1@example.com",
                categories=[]
            )
        ]
    )
    # Test for creation
    team_created = await tournament.create(team)
    assert team_created._loaded
    assert team_created.id
    assert team_created.reference == f"Test Team {rand_name}"
    assert team_created.short_reference == f"Test Team {rand_name}"
    #assert team_created.institution is None
    assert len(team_created.speakers) == 1
    assert team_created.speakers[0].team == team_created
    # Test for POST
    team_created.reference = f"POST Team {rand_name}"
    await team_created.request_post()
    assert team_created.reference == f"POST Team {rand_name}"
    # Test for PATCH
    await team_created.request_patch(
        tc.models.Team(
            reference=f"PATCH Team {rand_name}",
            institution=(await institutions)[0],
        )
    )
    assert team_created.reference == f"PATCH Team {rand_name}"
    assert team_created.institution is not None
    # Test for DELETE
    await team_created.request_delete()

@pytest.mark.asyncio
async def test_speaker(setup_client):
    client: tc.Client = setup_client
    tournament = await client.get_tournament(TEST_TOURNAMENT_SLUG)
    rand_name = random_string(10)
    teams = asyncio.create_task(tournament._links.teams.load())
    # Test for creation
    speaker = tc.models.Speaker(
        name=f"Test Speaker {rand_name}",
        team=(await teams)[0],
        categories=[],
    )
    speaker_created = await tournament.create(speaker)
    assert speaker_created._loaded
    assert speaker_created.id
    assert speaker_created.name == f"Test Speaker {rand_name}"
    assert speaker_created.team == (await teams)[0]
    assert len(speaker_created.categories) == 0
    # Test for POST
    speaker_created.name = f"POST Speaker {rand_name}"
    await speaker_created.request_post()
    assert speaker_created.name == f"POST Speaker {rand_name}"
    # Test for PATCH
    await speaker_created.request_patch(
        tc.models.Speaker(
            name=f"PATCH Speaker {rand_name}",
            team=(await teams)[1]
        )
    )
    assert speaker_created.name == f"PATCH Speaker {rand_name}"
    assert speaker_created.team == (await teams)[1]
    # Test for DELETE
    await speaker_created.request_delete()

@pytest.mark.asyncio
async def test_adjudicator(setup_client):
    client: tc.Client = setup_client
    tournament = await client.get_tournament(TEST_TOURNAMENT_SLUG)
    rand_name = random_string(10)
    institutions = asyncio.create_task(tournament._links.institutions.load())
    # Test for creation
    institution = tc.models.Adjudicator(
        name=f"Test Adjudicator {rand_name}",
        institution=(await institutions)[0],
        institution_conflicts=(await institutions)[0:2],
        team_conflicts=[],
        adjudicator_conflicts=[]
    )
    adj_created = await tournament.create(institution)
    assert adj_created._loaded
    assert adj_created.id
    assert adj_created.name == f"Test Adjudicator {rand_name}"
    assert adj_created.institution == (await institutions)[0]
    assert len(adj_created.institution_conflicts) == 2
    # Test for POST
    adj_created.name = f"POST Adjudicator {rand_name}"
    await adj_created.request_post()
    assert adj_created.name == f"POST Adjudicator {rand_name}"
    # Test for PATCH
    await adj_created.request_patch(
        tc.models.Adjudicator(
            name=f"PATCH Adjudicator {rand_name}",
            institution=(await institutions)[1]
        )
    )
    assert adj_created.name == f"PATCH Adjudicator {rand_name}"
    assert adj_created.institution == (await institutions)[1]
    # Test for DELETE
    await adj_created.request_delete()