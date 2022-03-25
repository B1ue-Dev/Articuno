import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
import jishaku
from jishaku.features.baseclass import Feature as jsk
import json
from slash_help import SlashHelp
from dotenv import load_dotenv
import status
import io, traceback, inspect, textwrap, contextlib
load_dotenv()


# Token
bot_token = os.getenv('TOKEN')



intents = discord.Intents.default()
intents.members = True
activity = discord.Activity(type=discord.ActivityType.watching,
							name="for a new era.")
bot = commands.Bot(command_prefix="$",
					intents=intents,
					activity=activity,
					help_command=None,
					enable_debug_events=True,
					owner_id = 892080548342820925)
slash = SlashCommand(bot, sync_commands = True, override_type = True, delete_from_unused_guilds = True)
SlashHelp(bot, slash, bot_token, dpy_command=True)





# Extensions
bot.load_extension('jishaku') #must for debug
# Others
bot.load_extension('Cogs.admin') # Done
bot.load_extension('Cogs.automod') # Done
#bot.load_extension('Cogs.arty')
bot.load_extension('Cogs.basic')
bot.load_extension('Cogs.error')
bot.load_extension('Cogs.fun')
bot.load_extension('Cogs.hacktool')
bot.load_extension('Cogs.logs')
bot.load_extension('Cogs.menus')
bot.load_extension('Cogs.server')
bot.load_extension('Cogs.ttt')




# Send message in the channel, which indicate that the bot is ready
@bot.event
async def on_ready():
	#channel = bot.get_channel(867039086387789874)
	##message = f"{bot.user.name} is now online again\nTime: <t:{jsk.load_time.timestamp():.0f}:R>"
	#embed = discord.Embed(description=message, color=0x000000)
	websocket = f"{bot.latency * 1000:.0f}"
	print('Connected to: {}'.format(bot.user.name))
	print('Bot ID: {}'.format(bot.user.id))
	print(f'Latency: {websocket}ms')
	#buttons = [
	#	create_button(style=ButtonStyle.URL, label="GitHub", url="https://github.com/Jimmy-Blue/Articuno")
	#]
	#action_row = create_actionrow(*buttons)
	#await channel.send(embed=embed, components=[action_row])


# List all servers the bot is connected to
@bot.command()
@commands.is_owner()
async def servers(ctx):
	for guild in bot.guilds:
		await ctx.send(guild.name)
# No!
@bot.command(name='eval')
@commands.is_owner()
async def _eval(ctx, *, body):
	"""Evaluates python code"""
	blocked_words = ['.delete()', 'os', 'subprocess', 'history()', '("token")', "('token')",
					 'aW1wb3J0IG9zCnJldHVybiBvcy5lbnZpcm9uLmdldCgndG9rZW4nKQ==', 'aW1wb3J0IG9zCnByaW50KG9zLmVudmlyb24uZ2V0KCd0b2tlbicpKQ==']
	if ctx.author.id != bot.owner_id:
		for x in blocked_words:
			if x in body:
				return await ctx.send('Your code contains certain blocked words.')
	env = {
		'ctx': ctx,
		'channel': ctx.channel,
		'author': ctx.author,
		'guild': ctx.guild,
		'message': ctx.message,
		'source': inspect.getsource,
	}

	env.update(globals())

	body = cleanup_code(body)
	stdout = io.StringIO()
	err = out = None

	to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

	def paginate(text: str):
		'''Simple generator that paginates text.'''
		last = 0
		pages = []
		for curr in range(0, len(text)):
			if curr % 1980 == 0:
				pages.append(text[last:curr])
				last = curr
				appd_index = curr
		if appd_index != len(text)-1:
			pages.append(text[last:curr])
		return list(filter(lambda a: a != '', pages))
	
	try:
		exec(to_compile, env)
	except Exception as e:
		err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
		return await ctx.message.add_reaction('\u2049')

	func = env['func']
	try:
		with contextlib.redirect_stdout(stdout):
			ret = await func()
	except Exception as e:
		value = stdout.getvalue()
		err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
	else:
		value = stdout.getvalue()
		if ret is None:
			if value:
				try:
					
					out = await ctx.send(f'```py\n{value}\n```')
				except:
					paginated_text = paginate(value)
					for page in paginated_text:
						if page == paginated_text[-1]:
							out = await ctx.send(f'```py\n{page}\n```')
							break
						await ctx.send(f'```py\n{page}\n```')
		else:
			bot._last_result = ret
			try:
				out = await ctx.send(f'```py\n{value}{ret}\n```')
			except:
				paginated_text = paginate(f"{value}{ret}")
				for page in paginated_text:
					if page == paginated_text[-1]:
						out = await ctx.send(f'```py\n{page}\n```')
						break
					await ctx.send(f'```py\n{page}\n```')

	if out:
		await ctx.message.add_reaction('\u2705')  # tick
	elif err:
		await ctx.message.add_reaction('\u2049')  # x
	else:
		await ctx.message.add_reaction('\u2705')

def cleanup_code(content):
	"""Automatically removes code blocks from the code."""
	# remove ```py\n```
	if content.startswith('```') and content.endswith('```'):
		return '\n'.join(content.split('\n')[1:-1])

	# remove `foo`
	return content.strip('` \n')

def get_syntax_error(e):
	if e.text is None:
		return f'```py\n{e.__class__.__name__}: {e}\n```'
	return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'







bot.run(bot_token)