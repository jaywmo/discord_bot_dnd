import discord
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = '`Hello {0.author.mention}`'.format(message)
        await client.send_message(message.channel, msg)
        logging.info(msg)

    if message.content.startswith('!test'):
        df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        await client.send_message(message.channel, df)
        logging.info(df)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run('NDI1NDE0MDc3MjEzNTczMTIx.DZIofw.Ej2h-rzPaNuGzaDzme_w04Q-SKg')