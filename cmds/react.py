import discord
from discord.ext import commands
import json
import os, random
from core.classes import Cog_Extension

with open('setting.json','r', encoding='utf8') as codes:
    jsonData = json.load(codes)

class React(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gallery(self, ctx):
        selected = random.choice(os.listdir(jsonData['singyesterday']))
        pic = discord.File(f'C:\\Caffretro\\Ca2+\\Discord Bot\\SingYesterday\\{selected}')
        await ctx.send(file=pic)

# registering bot
def setup(bot):
    bot.add_cog(React(bot))