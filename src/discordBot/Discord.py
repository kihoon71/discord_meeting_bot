import discord
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context
from discord.ext.commands import CommandError

class Discord:
    def __init__(self, token: str, guild: str):
        self.token = token
        self.guild = guild
        self.client = None
        self.recording = None

    ## Create a discord bot
    def create_bot(self):
        intents = discord.Intents.all()
        self.client = Bot(command_prefix='!', intents=intents)

    ## commands on !회의시작
    ### this command recognize whether the channel is for voice chat or not
    ### this command record the voice in the voice channel
    ### this command save the text 
    ### this command send a message to the user that the meeting has started
    @commands.command(name='회의시작', help='Start a meeting')
    async def start_meeting(self, ctx: Context):

        ## check if the channel is for voice chat
        if ctx.author.voice is None:
            await ctx.send('You are not in a voice channel')
            return
        
        ## get the voice channel
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()

        ## start recording the voice
        self.recording = await voice_client.listen(discord.AudioSource)
        await ctx.send('Starting a meeting')


    
    ## commands on !회의종료
    ## clear the text in the Text class
    ## send a message to the user that the meeting has ended
    ## transport the text in the Text class to the agent
    @commands.command(name='회의종료', help='End a meeting')
    async def end_meeting(self, ctx: Context):
        await ctx.send('Ending a meeting')

    ## run the bot
    def run(self):

        @self.client.event
        async def on_ready():
            guild = discord.utils.get(self.client.guilds, name=self.guild)

            print(f'{self.client.user} has connected to Discord! {guild.name}(id: {guild.id})')
        self.client.run(self.token)


    


    

    
        