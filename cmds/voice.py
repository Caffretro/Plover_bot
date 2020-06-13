import discord
from discord.ext import commands
from discord.utils import get
import json
from core.classes import Cog_Extension

with open('setting.json','r', encoding='utf8') as codes:
    jsonData = json.load(codes)

class Voice(Cog_Extension):

    @commands.command(pass_context=True, aliases=['j'])
    async def join(self, ctx):
        global Voice
        channel = ctx.message.author.voice.channel # join where join command sender is
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await voice.disconnect()

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await ctx.send(f'Joined {channel}')

    @commands.command(pass_context=True, aliases=['l'])
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f'Bot has left {channel}')
            await ctx.send(f'Bot has left {channel}')
        else:
            print(f'Bot is not in a channel')
            await ctx.send(f'Bot is not in a channel')

# registering bot
def setup(bot):
    bot.add_cog(Voice(bot))