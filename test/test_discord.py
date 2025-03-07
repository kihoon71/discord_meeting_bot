import pytest
import os
import discord
from discord.ext import commands
import sys
from unittest.mock import MagicMock, patch, AsyncMock
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), "../src/discordBot"))

# from TestBot import DiscordBot
from Discord import DiscordBot


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

@pytest.fixture(scope='module')
def Bot(token, guild):
    bot = DiscordBot(token)
    assert bot.token is not None
    return bot

@pytest.mark.asyncio
async def test_start_meeting_command(Bot):

    # 가짜 컨텍스트 생성
    mock_ctx = AsyncMock(spec=commands.Context)
    mock_ctx.bot = Bot
    mock_ctx.send = AsyncMock()  # ctx.send()를 가짜로 만듦
    mock_ctx.message = MagicMock()  # 'message' 속성 추가
    mock_ctx.view = MagicMock() 

    command = Bot.get_command('회의시작')

    await command.callback(Bot, mock_ctx)

    mock_ctx.send.assert_called_once_with('Starting a meeting')    

@pytest.mark.asyncio
async def test_start_meeting_command_not_in_voice_channel(Bot):

    # 가짜 컨텍스트 생성
    mock_ctx = AsyncMock(spec=commands.Context)
    mock_ctx.bot = Bot
    mock_ctx.send = AsyncMock()  # ctx.send()를 가짜로 만듦
    mock_ctx.message = MagicMock()  # 'message' 속성 추가
    mock_ctx.view = MagicMock()
    
    # Set the author attribute with a mock that has voice set to None
    mock_author = MagicMock()
    mock_author.voice = None
    mock_ctx.author = mock_author

    command = Bot.get_command('회의시작')

    await command.callback(Bot, mock_ctx)

    mock_ctx.send.assert_called_once_with('You are not in a voice channel')


@pytest.mark.asyncio
async def test_start_meeting_command_not_in_voice_channel(Bot):

    # 가짜 컨텍스트 생성
    mock_ctx = AsyncMock(spec=commands.Context)
    mock_ctx.bot = Bot
    mock_ctx.send = AsyncMock()  # ctx.send()를 가짜로 만듦
    mock_ctx.message = MagicMock()  # 'message' 속성 추가
    mock_ctx.view = MagicMock()
    
    # Set the author attribute with a mock that has voice set to None
    mock_author = MagicMock()

    command = Bot.get_command('회의종료')

    await command.callback(Bot, mock_ctx)

    mock_ctx.send.assert_called_once_with('End a meeting')


