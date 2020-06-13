import discord
from discord.ext import commands

# Cog connector for classes
class Cog_Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot