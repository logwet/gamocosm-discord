from discord.ext import commands
import logging
import sys
import confuse
import os
from api import Server

def apiErrorHandler(err):
    if not err:
        return "Action succesfully triggered"
    else:
        return err

logging.basicConfig(handlers=[logging.FileHandler('app.log'), logging.StreamHandler(sys.stdout)], format='[%(asctime)s %(levelname)s] %(message)s', level=logging.INFO)
os.environ["CONFIGDIR"] = "./"
config = confuse.Configuration('config', 'config')

configtemplate = {
    'serverId': str,
    'apiKey': str,
    'discordKey': str,
    'discordChannel': int
}

validconfig = config.get(configtemplate)
logging.info(validconfig)
server_id = validconfig['serverId']
api_key = validconfig['apiKey']
discord_key = validconfig['discordKey']
discord_channel = validconfig['discordChannel']

server = Server(server_id, api_key)
logging.info(f"Starting status is: {server._status()}")

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    logging.info(f'Bot is ready. We have logged in as {client.user}')

@client.command()
async def ping(ctx):
    channel = client.get_channel(discord_channel)
    response = "Pong!"
    await channel.send(response)
    logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")

@client.command()
async def start(ctx):
    channel = client.get_channel(discord_channel)
    response = apiErrorHandler(server.start())
    await channel.send(response)
    logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")

@client.command()
async def stop(ctx):
    channel = client.get_channel(discord_channel)
    response = apiErrorHandler(server.stop())
    await channel.send(response)
    logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")

@client.command()
async def reboot(ctx):
    channel = client.get_channel(discord_channel)
    response = apiErrorHandler(server.reboot())
    await channel.send(response)
    logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")

@client.command()
async def pause(ctx):
    channel = client.get_channel(discord_channel)
    response = apiErrorHandler(server.pause())
    await channel.send(response)
    logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")

@client.command()
async def resume(ctx):
    channel = client.get_channel(discord_channel)
    response = apiErrorHandler(server.resume())
    await channel.send(response)
    logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")

@client.command()
async def backup(ctx):
    channel = client.get_channel(discord_channel)
    response = apiErrorHandler(server.backup())
    await channel.send(response)
    logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")

@client.command()
async def download(ctx):
    channel = client.get_channel(discord_channel)
    response = apiErrorHandler(server.download())
    await channel.send(response)
    logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")

@client.command()
async def status(ctx):
    channel = client.get_channel(discord_channel)
    raw_response = server._status()
    pserver = ['online' if raw_response['server'] else 'offline'][0]
    minecraft = ['online' if raw_response['minecraft'] else 'offline'][0]
    pending = raw_response['status']
    domain = raw_response['domain']
    ip = raw_response['ip']
    response = f"Physical server: {pserver}\nMinecraft: {minecraft}\nPending operations: {pending}\nServer hostname: {domain}\nServer ip: {ip}"
    await channel.send(response)
    logging.info(f"'{ctx.command}' command called by {ctx.author}. Response was '{response}'")

client.run(discord_key)