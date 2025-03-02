import pytest
import os
import discord
from unittest.mock import MagicMock, patch
from dotenv import load_dotenv, find_dotenv


@pytest.fixture(scope='module')
def token():
    # Load .env file and fetch the token
    env_path = find_dotenv()
    load_dotenv(env_path)

    TOKEN = os.getenv('DISCORD_TOKEN')
    assert TOKEN is not None
    return TOKEN

@pytest.fixture(scope='module')
def guild():
    guild = os.getenv('DISCORD_GUILD')
    assert guild is not None
    return guild

