from discord.ext import commands
import re
import logging
from Library.NdN_roll import ndn_roll


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

        if rolls > 999999:
            await ctx.send('Fuck you. Calculate that yourself by hand.')
            return
        result, result_sum = ndn_roll(rolls, limit)
        logging.info(result)
        # result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        add_str = ''
        if args:
            regex = r'(\w*\+)(\d+)'
            match = re.search(regex, args[0])
            if match:
                result, result_sum = ndn_roll(rolls, limit, match.group(1), int(match.group(2)))
                add_str = '{}'.format(match.group(0))
            else:
                result, result_sum = ndn_roll(rolls, limit)
        else:
            result, result_sum = ndn_roll(rolls, limit)

        for i in range(len(result_sum)):
            print(result[i][1:-1])
            print(result_sum[i])
            await ctx.send('`({}) {}\n={}`'.format(result[i][1:-1], add_str, result_sum[i]))
        logging.info('`{}`'.format(args))


def setup(bot):
    bot.add_cog(RollCommands(bot))
