import discord
from discord.ext import commands

class DiscordBot(commands.Bot):
    def __init__(self, command_prefix):
        intents = discord.Intents.default()
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.add_command(self.hello)

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    @commands.command()
    async def hello(self, ctx):
        """!hello 입력 시 응답하는 명령어"""
        await ctx.send("Hello, world!")

