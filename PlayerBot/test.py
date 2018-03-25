import discord
from discord.ext import commands
import asyncio
import numpy as np
import pandas as pd
import random
import re
import logging
import yaml


with open("../Config/PlayerBot_config.yaml", 'r') as stream:
    config = yaml.load(stream)


logging.basicConfig(level=logging.INFO)

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix=config['command_prefix'], description=description)


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


@bot.command(name='roll', aliases=['r'], brief='Rolls a dice in NdN format. Supports addition.',
             description='Rolls a dice in NdN format. Supports addition per roll or on sum.')
async def roll(dice : str, *args):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except ValueError:
        await bot.say('Format has to be in NdN!')
        return

    result = np.random.randint(1, limit + 1, size=rolls)
    result_sum = np.sum(result)
    logging.info(result)
    # result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    if args:
        regex = r'(\w*\+)(\d+)'
        match = re.search(regex, args[0])
        if match:
            if match.group(1) == '+':
                result_sum += int(match.group(2))
            elif match.group(1) == 'r+':
                result += int(match.group(2))
                result_sum = np.sum(result)

    await bot.say('`{}\n={}`'.format(str(result.tolist())[1:-1], result_sum))
    logging.info('`{}`'.format(args))


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
