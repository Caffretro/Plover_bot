import discord
from discord.ext import commands
import json
import os, random

with open('setting.json','r', encoding='utf8') as codes:
    jsonData = json.load(codes)
bot = commands.Bot(command_prefix = '##') # creating bot var

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type=3, name='singyesterday.com'))
    print(">> Bot is online <<")

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

for Filename in os.listdir('./cmds'):
    if Filename.endswith('.py'):
        bot.load_extension(f'cmds.{Filename[:-3]}')

if __name__ == "__main__":
    # below is the token for Plover_bot
    bot.run(jsonData['TOKEN'])