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


class RollCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll', aliases=['r'], brief='Rolls a dice in NdN format. Supports addition.',
                      description='Rolls a dice in NdN format. Supports addition per roll or on sum.')
    async def roll(self, ctx, dice: str, *args):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except ValueError:
            await ctx.send('Format has to be in NdN!')
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

        await ctx.send('`{}\n={}`'.format(str(result.tolist())[1:-1], result_sum))
        logging.info('`{}`'.format(args))


def setup(bot):
    bot.add_cog(RollCommands(bot))
