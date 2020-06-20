import discord
from discord.ext import commands
from discord.utils import get
import json
import os
import youtube_dl
import array
from core.classes import Cog_Extension

with open('setting.json', 'r', encoding='utf8') as codes:
    jsonData = json.load(codes)


class Voice(Cog_Extension):
    global Voice
    selections = []
    localSongs = []
    queue = []
    currentSong = None

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
                # check if bot is being used in another channel
                if channel and channel != ctx.voice_client.channel:
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

    # TODO: catch Extractor Error and DownloadError
    # Go watch error episode. Assume it always gets correct url right now
    @commands.command(pass_context=True, aliases=['po'])
    async def playonline(self, ctx, url: str):

        # bugs with youtube-dl playing, currently offlining play command
        await ctx.send("Youtube music streaming is currently offline, sorry for any inconvenience.")
        return

        # check if bot is idle
        channel = ctx.message.author.voice.channel  # join where join command sender is
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            # check if bot is being used in another channel
            if channel and channel != ctx.voice_client.channel:
                await ctx.send('I\'m currently being used in another channel')
                return
        else:
            voice = await channel.connect()
            await ctx.send(f'Joined {channel}')

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
        await ctx.send("Loading...(sorry for the waiting but I\'m just a Raspberry Pi)")
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        # quality set to 320, could result in errors. Default is 192
        # toggle 'quiet' to get cleanner console
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

    @commands.command(pass_context=True, aliases=['c'])
    async def circle(self, ctx):
        channel = ctx.message.author.voice.channel  # join where join command sender is
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        # scan local music files
        if not self.localSongs:
            for file in os.listdir(jsonData['musicStorage']):
                if file.endswith('.mp3') or file.endswith('.flac') or file.endswith('.wma'):
                    self.localSongs.append(file)

    @commands.command(pass_context=True, aliases=['p'])
    async def play(self, ctx, *, name=None):

        channel = ctx.message.author.voice.channel  # join where join command sender is
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        def check_queue(selection=False):
            # make check_queue a one time function, so the program can await a text message to discord channel
            # if the song just added to queue is a secondary command, need to reset selection
            if selection:
                self.selections.clear()
            if self.queue:
                nextSong = self.queue.pop(0)
                self.currentSong = nextSong
                voice.play(discord.FFmpegPCMAudio(f'/home/pi/Music/{nextSong}'),
                           after=lambda e: print(f'{nextSong} has finished playing'))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

        if name is None:
            print("User entered invalid song name")
            await ctx.send("Usage: playlocal <songname>")
            return

        if voice and voice.is_connected():
            # check if bot is being used in another channel
            if channel and channel != ctx.voice_client.channel:
                await ctx.send('I\'m currently being used in another channel')
                return
        else:
            voice = await channel.connect()
            await ctx.send(f'Joined {channel}')

        # check if this request is a follow up request
        if self.selections:
            self.queue.append(self.selections[int(name) - 1])
            check_queue(True)
            # TODO: check if queue is empty and choose what to display in text channel
            await ctx.send(f'Now playing: {self.currentSong}')
            return

        # get to music storage
        await ctx.send("Loading...(sorry for the waiting but I\'m just a Raspberry Pi)")

        # scan local music files
        if not self.localSongs:
            for file in os.listdir(jsonData['musicStorage']):
                if file.endswith('.mp3') or file.endswith('.flac') or file.endswith('.wma'):
                    self.localSongs.append(file)
        # search keywords
        matching = [s for s in self.localSongs if name.lower() in s.lower()]
        if not matching:
            print(f"{name} not found in local disk")
            await ctx.send(f"{name} not found in local disk")
        elif len(matching) > 1:
            await ctx.send("Below are matchings. Specify which one you want to play:")
            for candidate, i in zip(matching, range(len(matching))):
                await ctx.send(f'|     {i+1}. {candidate}')
                self.selections.append(candidate)
        else:
            self.queue.append(matching[0])
            check_queue()
            # TODO: check if queue is empty and choose what to display in text channel
            await ctx.send(f'Now playing: {self.currentSong}')

    # TODO: implement skip function

    @commands.command(pass_context=True, aliases=['pa', 'pau'])
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Music paused")
            voice.pause()
            await ctx.send("Music paused")
        else:
            print("There aren't any musics playing")
            await ctx.send("There aren't any musics playing")

    @commands.command(pass_context=True, aliases=['r', 're'])
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print("Music resumed")
            voice.resume()
            await ctx.send("Music resumed")
        else:
            print("Music isn't paused")
            await ctx.send("Music isn't paused")

    @commands.command(pass_context=True, aliases=['s', 'st'])
    async def stop(self, ctx):
        self.queue.clear()
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Music stopped")
            voice.stop()
            await ctx.send("Music stopped")
        else:
            print("There aren't any musics playing")
            await ctx.send("There aren't any musics playing")

# registering bot


def setup(bot):
    bot.add_cog(Voice(bot))
