import discord
from discord.ext import commands
import asyncio
import numpy as np
import pandas as pd
import random
import re
import logging
import yaml


with open("Config/my_PlayerBot_config.yaml", 'r') as stream:
    config = yaml.load(stream)


logging.basicConfig(level=logging.INFO)

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix=config['command_prefix'], description=description, owner_id=106566006637338624)
# this specifies what extensions to load when the bot starts up
startup_extensions = ["PlayerBot.Rolls"]


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('discord.py v{}'.format(discord.__version__))
    print('------')


@bot.command()
@commands.is_owner()
async def load(ctx, extension_name: str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))


@bot.command()
@commands.is_owner()
async def unload(ctx, extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await ctx.send("{} unloaded.".format(extension_name))


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(config['token'])
