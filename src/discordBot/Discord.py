import discord
from discord.ext import commands
from discord.ext.commands import Context

class DiscordBot:
    def __init__(self, token: str):
        self.token = token
        self.recording = {}
        self.monitoring_channel = {}

        intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix='!', intents=intents)

        # 명령어 등록
        self.bot.add_command(self.start_meeting)
        self.bot.add_command(self.end_meeting)

        # 이벤트 핸들러 등록
        self.bot.event(self.on_ready)
        self.bot.event(self.on_voice_state_update)

    async def on_ready(self):
        print(f"Logged in as {self.bot.user}")

    @commands.command(name='회의시작', help='Start a meeting')
    async def start_meeting(self, ctx: Context):
        if ctx.author.voice is None:
            await ctx.send('You are not in a voice channel')
            return

        self.monitoring_channel.update({ctx.channel.id: set()})
        await ctx.send('Starting a meeting')

        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()
        self.recording[ctx.channel.id] = await voice_client.listen(discord.AudioSource)

    @commands.command(name='회의종료', help='End a meeting')
    async def end_meeting(self, ctx: Context):
        await ctx.send('End a meeting')

    async def on_voice_state_update(self, member, before, after):
        if before.self_mute and not after.self_mute:
            if member.voice.channel.id in self.monitoring_channel:
                self.monitoring_channel[member.voice.channel.id].add(member)

    def run(self):
        self.bot.run(self.token)
