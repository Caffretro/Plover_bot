import discord
from discord.ext import commands
import json
from core.classes import Cog_Extension

with open('setting.json','r', encoding='utf8') as codes:
    jsonData = json.load(codes)

class Event(Cog_Extension):
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} join!")
        channel = self.bot.get_channel(int(jsonData['welcome_channel'])) # the id of welcome channel
        await channel.send(f'{member} 通过了检票口')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} leave!")
        channel = self.bot.get_channel(int(jsonData['welcome_channel'])) # the id of welcome channel
        await channel.send(f'{member} 离开了车站')

    # Activate with keywords
    @commands.Cog.listener()
    async def on_message(self, msg):
        keywords = ['apple']
        if msg.content in keywords and msg.author != self.bot.user:
            # note that msg.channel is required that is different from ctx
            await msg.channel.send('hi')


# registering bot
def setup(bot):
    bot.add_cog(Event(bot))