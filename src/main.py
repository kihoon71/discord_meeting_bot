# from discordBot.Discord import DiscordBot
import discord
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv, find_dotenv
from UTIL.Audio import Audio
from datetime import datetime
import os
import sys

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

AUDIO = Audio()

@bot.command(name='회의시작', help='Start a meeting')
async def start_meeting(ctx):
    if ctx.author.voice is None:
            await ctx.send('You are not in a voice channel')
            return
    
    await ctx.send('Starting a meeting')
    
    # get the voice channel
    voice_channel = ctx.author.voice.channel
    channel_id = voice_channel.id
    voice_client = await voice_channel.connect()

    # get the audio data
    start_time = datetime.now()
    filename = f"./temp/{start_time.strftime('%Y%m%d%H%M%S')}.wav"

    AUDIO.set_audio(channel_id, filename)

    


@bot.command(name='회의종료', help='End a meeting')
async def end_meeting(ctx: Context):
    if ctx.author.voice is None:
            await ctx.send('You are not in a voice channel')
            return
    
    voice_channel = ctx.author.voice.channel.id
    assert AUDIO.get_audio(voice_channel) is not None, 'There is no audio data'

    AUDIO.clear_audio(voice_channel)
    
    await ctx.send('End a meeting')


if __name__ == '__main__':

    TOKEN = os.getenv('DISCORD_TOKEN')
    print(TOKEN)

    bot.run(TOKEN)


