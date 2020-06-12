import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '##') # creating bot var

@bot.event
async def on_ready():
    print(">> Bot is online <<")

@bot.event
async def on_member_join(member):
    print(f"{member} join!")
    channel = bot.get_channel(721122350895988807) # the id of welcome channel
    await channel.send(f'{member} 通过了检票口')

@bot.event
async def on_member_remove(member):
    print(f"{member} leave!")
    channel = bot.get_channel(721122350895988807) # the id of welcome channel
    await channel.send(f'{member} 离开了车站')

# below is the token for Plover_bot
bot.run('NzIxMTA2MzgyMDgxNzUzMDk5.XuPsvg.TA5v2Sp2rc2Fw4VQy-Ao0WAz9bg')