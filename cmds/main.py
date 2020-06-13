import discord
from discord.ext import commands
import json
from core.classes import Cog_Extension

with open('setting.json','r', encoding='utf8') as codes:
    jsonData = json.load(codes)

class Main(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency * 1000)} ms') ## converting to ms

# registering bot
def setup(bot):
    bot.add_cog(Main(bot))