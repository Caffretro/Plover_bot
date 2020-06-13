import discord
from discord.ext import commands
from discord.utils import get
import json
import os
import youtube_dl
from core.classes import Cog_Extension

with open('setting.json', 'r', encoding='utf8') as codes:
    jsonData = json.load(codes)


class Voice(Cog_Extension):
    global Voice

    @commands.command(pass_context=True, aliases=['j'])
    async def join(self, ctx, mode=None):

        channel = ctx.message.author.voice.channel  # join where join command sender is
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        # force the bot to join current ctx's channel
        if mode == 'strong':
            await voice.disconnect()

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
        else:
            if voice and voice.is_connected():
                await ctx.send('I\'m currently being used in another channel')
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

    @commands.command(pass_context=True, aliases=['p'])
    async def play(self, ctx, url: str):
        # check if bot is idle
        # channel = ctx.message.author.voice.channel # join where join command sender is
        # voice = get(self.bot.voice_clients, guild=ctx.guild)

        # if voice and voice.is_connected():
        #     if :
        #         await ctx.send('I\'m currently being used in another channel')
        # else:
        #     voice = await channel.connect()
        # if voice and voice.is_connected and ctx.voice_client.channel != channel:
        #     # remind user that bot it being used, do nothing
        #     await ctx.send('I\'m currently being used in another channel')
        #     return
        # elif ctx.voice_client.channel == channel:
        #     print('Play command from same channel\n')
        # else:
        #     voice = await channel.connect()

        self.join(self, ctx, None)

        # check local file
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed current dir's song.mp3")
        except PermissionError:
            print("Can't delete song.mp3 since it's being played")
            await ctx.send("Music is being played")
            return

        # using youtube-dl module
        await ctx.send("Loading...")

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        # quality set to 320, could result in errors. Default is 192
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Extracting audio and downloading now")
            ydl.download([url])

        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                name = file
                print(f'Renamed file: {file}')
                os.rename(file, 'song.mp3')

        voice.play(discord.FFmpegPCMAudio("song.mp3"),
                   after=lambda e: print(f'{name} has finished playing'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        newName = name.rsplit('-', 2)
        await ctx.send(f'Playing: {newName[0]}')
        print("Playing...")

# registering bot


def setup(bot):
    bot.add_cog(Voice(bot))
