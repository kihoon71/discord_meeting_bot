import discord
from datetime import datetime
from discord.ext import commands, tasks
from discord.ext.commands import Context, CommandError, bot

class DiscordBot(commands.Bot):
    def __init__(self, token: str):
        self.token = token
        self.recording = {}
        self.monitoring_channel = {} # {channel1: set(speaker1, speaekr2...), chanel2 : set(speaker1, speaker2...)}

        intents = discord.Intents.all()
        super().__init__(command_prefix='!', intents=intents)

        self.add_command(self.start_meeting)
        self.add_command(self.end_meeting)
        
    
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        
    ## commands on !회의시작
    @commands.command(name='회의시작', help='Start a meeting')
    async def start_meeting(self, ctx: Context):
        '''
        this command recognize whether the channel is for voice chat or not
        this command record the voice in the voice channel
        this command send a message to the user that the meeting has started
        '''

        ## check if the channel is for voice chat
        if ctx.author.voice is None:
            await ctx.send('You are not in a voice channel')
            return
        
        ## to count speakers
        self.monitoring_channel.update({ctx.channel.id: set()})

        await ctx.send('Starting a meeting')
        
        # ## get the voice channel
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()

        # ## start recording the voice
        self.recording[ctx.channel.id] = await voice_client.listen(discord.AudioSource)
        


    
    ## commands on !회의종료
    ## clear the text in the Text class
    ## send a message to the user that the meeting has ended
    ## transport the text in the Text class to the agent
    @commands.command(name='회의종료', help='End a meeting')
    async def end_meeting(self, ctx: Context):
        await ctx.send('End a meeting')


    #override on_voice_state_update method
    async def on_voice_state_update(self, member, before, after):

        if before.self_mute and not after.self_mute:
            if member.voice.channel.id in self.monitoring_channel:
                self.monitoring_channel[member.voice.channel.id].add(member)

        
        


    


    

    
        