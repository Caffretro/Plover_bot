import discord
from discord.ext import commands
import json
import os, random

with open('setting.json','r', encoding='utf8') as codes:
    jsonData = json.load(codes)
bot = commands.Bot(command_prefix = '##') # creating bot var

@bot.event
async def on_ready():
    print(">> Bot is online <<")

@bot.event
async def on_member_join(member):
    print(f"{member} join!")
    channel = bot.get_channel(int(jsonData['welcome_channel'])) # the id of welcome channel
    await channel.send(f'{member} 通过了检票口')

@bot.event
async def on_member_remove(member):
    print(f"{member} leave!")
    channel = bot.get_channel(int(jsonData['welcome_channel'])) # the id of welcome channel
    await channel.send(f'{member} 离开了车站')

@bot.command()
async def load(ctx, extension):
    try:
        bot.load_extension(f'cmds.{extension}')
        await ctx.send(f'Loaded {extension.lower()}.')
    except:
        await ctx.send(f'{extension} is not a valid extension.')

@bot.command()
async def unload(ctx, extension):
    try:
        bot.unload_extension(f'cmds.{extension}')
        await ctx.send(f'Unloaded {extension.lower()}.')
    except:
        await ctx.send(f'{extension} is not a valid extension.')

@bot.command()
async def reload(ctx, extension):
    try:
        bot.reload_extension(f'cmds.{extension}')
        await ctx.send(f'Reloaded {extension.lower()}.')
    except:
        await ctx.send(f'{extension} is not a valid extension.')

for Filename in os.listdir('C:\Caffretro\Ca2+\Discord Bot\cmds'):
    if Filename.endswith('.py'):
        bot.load_extension(f'cmds.{Filename[:-3]}')

if __name__ == "__main__":
    # below is the token for Plover_bot
    bot.run(jsonData['TOKEN'])