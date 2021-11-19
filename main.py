import discord
from discord import Client, Intents, Embed
from discord.ext import commands
from discord_slash import SlashCommand
import jishaku
import json


intents = discord.Intents.default()
intents.members = True
# Activity for bot
activity = discord.Activity(type=discord.ActivityType.watching, name="for /")
# ...
bot = commands.Bot(command_prefix="!",
		intents=intents,
		activity=activity)
slash = SlashCommand(bot, sync_commands = True, override_type = True, delete_from_unused_guilds = True)



# Token
with open('./data/config.json') as bot_data:
    data = json.load(bot_data)



# Extensions
bot.load_extension('jishaku') # Jishaku is for debug
bot.load_extension('cogs.admin')
bot.load_extension('cogs.automod')
bot.load_extension('cogs.basic')
'''
bot.load_extension('cogs.fun')
bot.load_extension('cogs.logs')
bot.load_extension('cogs.server')
'''



# Notify when bot is connected
@bot.event
async def on_ready():
	websocket = f"{bot.latency * 1000:.0f}"
	print('Connected to: {}'.format(bot.user.name))
	print('Bot ID: {}'.format(bot.user.id))
	print(f'Latency: {websocket}ms')


#bot.run
bot.run(data["TOKEN"])
