import logging
import os
import sys

import confuse
from discord.ext import commands

import commands as cmds
from api import Server

logging.basicConfig(handlers=[logging.FileHandler('app.log'), logging.StreamHandler(sys.stdout)],
                    format='[%(asctime)s %(levelname)s] %(message)s', level=logging.INFO)
logging.info("------ APP STARTED ------")

os.environ["CONFIGDIR"] = "./"
config = confuse.Configuration('config', 'config')

configtemplate = {
    'serverId': str,
    'apiKey': str,
    'discordKey': str,
    'discordChannel': int
}

validconfig = config.get(configtemplate)
logging.info(f"Config: {validconfig}")
server_id = validconfig['serverId']
api_key = validconfig['apiKey']
discord_key = validconfig['discordKey']
discord_channel = validconfig['discordChannel']

server = Server(server_id, api_key)
logging.info(f"Starting status is: {server._status()}")

client = commands.Bot(command_prefix=".")


@client.event
async def on_ready():
    logging.info(f'Bot is ready. We have logged in as {client.user}')


def find_commands(module, clazz):
    """Searches commands.py to find suitable commands to register"""
    for name in dir(module):
        o = getattr(module, name)
        try:
            if (o != clazz) and issubclass(o, clazz):
                yield name, o
        except TypeError:
            pass


for category in find_commands(cmds, cmds.Category):
    logging.info(f"Configuring command category {category[1]}")
    client.add_cog(category[1](client, discord_channel, server))

client.run(discord_key)
