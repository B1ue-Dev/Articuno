import discord
from discord import Client, Intents, Embed
from discord.ext import commands
from discord_slash import SlashCommand
import jishaku
import json



# Token
with open('./data/config.json') as bot_data:
	data = json.load(bot_data)




# 3 dots here
intents = discord.Intents.default()
intents.members = True
activity = discord.Activity(type=discord.ActivityType.watching,
							name="for v3.0 /help")
bot = commands.Bot(command_prefix="$",
					intents=intents,
					activity=activity,
					enable_debug_events=True)
slash = SlashCommand(bot, sync_commands = True, override_type = True, delete_from_unused_guilds = True)




# Extensions
bot.load_extension('jishaku') # Jishaku is for debug
bot.load_extension('cogs.admin')
bot.load_extension('cogs.automod')
bot.load_extension('cogs.basic')
bot.load_extension('cogs.error')
bot.load_extension('cogs.fun')
bot.load_extension('cogs.hacktool')
bot.load_extension('cogs.menus')
bot.load_extension('cogs.server')




# Notify when bot is connected
@bot.event
async def on_ready():
	websocket = f"{bot.latency * 1000:.0f}"
	print('Connected to: {}'.format(bot.user.name))
	print('Bot ID: {}'.format(bot.user.id))
	print(f'Latency: {websocket}ms')





#bot.run
bot.run(data["TOKEN"])
