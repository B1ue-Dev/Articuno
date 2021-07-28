import discord
from discord.ext import commands
from itertools import cycle
import asyncio
import os
import jishaku
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)
status = cycle(["status1", "status2"])
blue = 0x236adf
red = 0xff0000
orange = 0xff8b00
purple = 0xac10eb
black = 0xffffff
white = 0x000000
green = 0x3bcc12
yellow = 0xfff900
gray = 0x6d6868

bot.load_extension('jishaku')
bot.load_extension("basic")
bot.load_extension('moderation')
bot.load_extension('automod')
bot.load_extension('logs')
bot.load_extension('error')
bot.load_extension('fun')
bot.load_extension('pokemon')
bot.load_extension('stats')
bot.load_extension('swear')
bot.load_extension('emoji')
bot.load_extension('server')




@bot.event
async def on_ready():
	print('Connected to bot: {}'.format(bot.user.name))
	print('Bot ID: {}'.format(bot.user.id))
	bot.loop.create_task(status_task())


async def status_task():
	while True:
		await bot.change_presence(status=discord.Status.online,
		                          activity=discord.Activity(
		                              type=discord.ActivityType.watching,
		                              name="for chat"))
		await asyncio.sleep(80)

		await bot.change_presence(status=discord.Status.do_not_disturb,
		                          activity=discord.Activity(
		                              type=discord.ActivityType.playing,
		                              name="with drug"))
		await asyncio.sleep(25)

		await bot.change_presence(status=discord.Status.online,
		                          activity=discord.Activity(
		                              type=discord.ActivityType.streaming,
		                              name="on YouTube"))
		await asyncio.sleep(45)

		await bot.change_presence(status=discord.Status.idle,
		                          activity=discord.Activity(
		                              type=discord.ActivityType.playing,
		                              name="with sleep..."))
		await asyncio.sleep(150)



@bot.command(description="*For owner only*: Change Articuno's status")
@commands.is_owner()
async def change(ctx, type, *, status):
	if type.startswith("play"):
		await bot.change_presence(activity=discord.Game(name=status))
	if type.startswith("watch"):
		await bot.change_presence(activity=discord.Activity(
		    type=discord.ActivityType.watching, name=status))
	if type.startswith("stream"):
		await bot.change_presence(activity=discord.Activity(
		    type=discord.ActivityType.streaming, name=status))
	if type.startswith("listen"):
		await bot.change_presence(activity=discord.Activity(
		    type=discord.ActivityType.listening, name=status))
	await ctx.send("BOT's status changed successfully")





bot.run("ODUxMDY0Nzk4MzMzNTAxNDgw.YLy12w.EtzCjFGNf2xaeoKePJY3uhH3kxY")
