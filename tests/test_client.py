import tabbycat_api as tc
import asyncio
from dotenv import load_dotenv
import pytest
import os

load_dotenv()

TEST_ENDPOINT = os.getenv("TEST_ENDPOINT")
TEST_TOKEN = os.getenv("TEST_TOKEN")
TEST_TOURNAMENT_SLUG = os.getenv("TEST_TOURNAMENT_SLUG")

@pytest.fixture
def setup_client():
    client = tc.Client(
        tc.ClientConfig(
            TEST_ENDPOINT,
            TEST_TOKEN,
            False,
            20
        )
    )
    yield client

@pytest.fixture
def config_no_lazy_load(monkeypatch):
    monkeypatch.setattr(tc.config, "CONFIG_LAZY_LOAD", False)

def test_invalid_update():
    with pytest.raises(KeyError):
        institution = tc.models.Institution(
            name="Foo",
            code="Bar"
        )
        institution.update_data(
            {
                "neim": "Test Institution"
            }
        )

def test_update():
    institution = tc.models.Institution(
        name="Foo",
        code="Bar"
    )
    assert institution.name == "Foo"
    institution.update_data(
        {
            "name": "Test Institution"
        }
    )
    assert institution.name == "Test Institution"

@pytest.mark.asyncio
async def test_tournament(setup_client):
    client: tc.Client = setup_client
    tournament = await client.get_tournament(TEST_TOURNAMENT_SLUG)
    assert tournament.name == "Test Tournament"

@pytest.mark.asyncio
async def test_lazyload(setup_client):
    client: tc.Client = setup_client
    tournament = await client.get_tournament(TEST_TOURNAMENT_SLUG)
    list(tournament._links.rounds)

@pytest.mark.asyncio
async def test_no_lazyload(setup_client, config_no_lazy_load):
    client: tc.Client = setup_client
    tournament = await client.get_tournament(TEST_TOURNAMENT_SLUG)
    with pytest.raises(AttributeError):
        list(tournament._links.rounds)