import discord
from discord.ext import commands
import asyncio
import numpy as np
import pandas as pd
import logging
import yaml


with open("../Config/PlayerBot_config.yaml", 'r') as stream:
    try:
        print(yaml.load(stream))
    except yaml.YAMLError as exc:
        print(exc)


logging.basicConfig(level=logging.INFO)

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='/', description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)


@bot.command(name='roll', aliases=['r'], brief='Rolls a dice in NdN format.')
async def roll(dice : str, *args):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = np.random.randint(1, limit, size=rolls).tolist()
    logging.info(result)
    # result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say('`{}\n={}`'.format(str(result)[1:-1], np.sum(result)))
    await bot.say('`{}`'.format(args))


@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))


@bot.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)


@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))


@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))


@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')


@bot.command()
async def test():
    await bot.say('`test`')


async def list_servers():
    await bot.wait_until_ready()
    while not bot.is_closed:
        print('Current servers:')
        for server in bot.servers:
            print(server.name)
        await asyncio.sleep(6)


bot.run('NDI1NDE0MDc3MjEzNTczMTIx.DZIofw.Ej2h-rzPaNuGzaDzme_w04Q-SKg')
