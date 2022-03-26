from http.client import HTTPException
import discord
from discord.ext import commands
import discord_slash
from discord_slash.context import InteractionContext
from datetime import datetime, timezone
import traceback


# Excuse me but I am lazy
listener = commands.Cog.listener


class Error(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@listener()
	async def on_slash_command_error(self, ctx: InteractionContext, error):
		error_time: datetime = datetime.utcnow().replace(tzinfo=timezone.utc)

		traceb2 = traceback.format_exception(type(error), error, error.__traceback__)
		traceb = ''.join(traceb2)
		traceb = traceb.replace('`','')
		traceb = traceb.replace('\\n','\n')
		traceb = traceb.replace('\\t','\t')
		traceb = traceb.replace('\\r','\r')
		traceb = traceb.replace("\\","/")
		er = ""
		for i in traceb:
			er = er + f"{i}"
		embed=discord.Embed(title="**Uh oh...**",description="An error occurred. The developer team is dealing with the problem now.\nJoin the [**Support Server**](https://discord.gg/rQHRQ8JjSY) for more help.",color=discord.Color.red())
		embed.add_field(name="Error",value=f'```py\n{type(error).__name__}: {error}\n```')
		await ctx.send(embed=embed, hidden=True)

		errorc2 = await self.bot.fetch_channel(862636687226044436)
		try:
			error=discord.Embed(title="An error occurred.",
					description=f"Caused by **{ctx.command}**\n__Author:__ {ctx.author} `{ctx.author.id}`\n__Guild:__ {ctx.guild.name} `{ctx.guild.id}`\n__Occured:__ <t:{error_time.timestamp():.0f}:R>",color=discord.Color.red())
		except:
			error=discord.Embed(title="An error occurred.",
					description=f"Caused by **{ctx.command}**\n__Author ID:__ {ctx.author} `{ctx.author.id}`\n__Occured:__ <t:{error_time.timestamp():.0f}:R>",color=discord.Color.red())
		try:
			error.add_field(name="Error",value=f"```py\n{traceb}\n```")
			await errorc2.send(embed=error)
		except Exception as e:
			try:
				error1=discord.Embed(title="An error occurred.",
								description=f"Caused by **{ctx.command}**\n__Author:__ {ctx.author} `{ctx.author.id}`\n__Guild:__ {ctx.guild.name} `{ctx.guild.id}`\n__Occured:__ <t:{error_time.timestamp():.0f}:R>",color=discord.Color.red())
			except:
				error1=discord.Embed(title="An error occurred.",
								description=f"Caused by **{ctx.command}**\n__Author ID:__ {ctx.author} `{ctx.author.id}`\n__Occured:__ <t:{error_time.timestamp():.0f}:R>",color=discord.Color.red())
			error1.add_field(name="Error",value=f"```py\n...{er[-1000:]}\n```")
			await errorc2.send(embed=error1)





	@listener()
	async def on_component_callback_error(self, ctx: InteractionContext, error):
		error_time: datetime = datetime.utcnow().replace(tzinfo=timezone.utc)

		traceb2 = traceback.format_exception(type(error), error, error.__traceback__)
		traceb = ''.join(traceb2)
		traceb = traceb.replace('`','')
		traceb = traceb.replace('\\n','\n')
		traceb = traceb.replace('\\t','\t')
		traceb = traceb.replace('\\r','\r')
		traceb = traceb.replace("\\","/")
		er = ""
		for i in traceb:
			er = er + f"{i}"
		embed=discord.Embed(title="**Uh oh...**",description="An error occurred. The developer team is dealing with the problem now.\nJoin the [**Support Server**](https://discord.gg/rQHRQ8JjSY) for more help.",color=discord.Color.red())
		embed.add_field(name="Error",value=f'```py\n{type(error).__name__}: {error}\n```')
		try:
			await ctx.send(embed=embed, hidden=True)
		except:
			pass

		errorc2 = await self.bot.fetch_channel(862636687226044436)
		try:
			error=discord.Embed(title="An error occurred.",
					description=f"Caused by **{ctx.command}**\n__Author:__ {ctx.author} `{ctx.author.id}`\n__Guild:__ {ctx.guild.name} `{ctx.guild.id}`\n__Occured:__ <t:{error_time.timestamp():.0f}:R>",color=discord.Color.red())
		except:
			error=discord.Embed(title="An error occurred.",
					description=f"Caused by **{ctx.command}**\n__Author ID:__ {ctx.author} `{ctx.author.id}`\n__Occured:__ <t:{error_time.timestamp():.0f}:R>",color=discord.Color.red())
		try:
			error.add_field(name="Error",value=f"```py\n{traceb}\n```")
			await errorc2.send(embed=error)
		except Exception as e:
			try:
				error1=discord.Embed(title="An error occurred.",
								description=f"Caused by **{ctx.command}**\n__Author:__ {ctx.author} `{ctx.author.id}`\n__Guild:__ {ctx.guild.name} `{ctx.guild.id}`\n__Occured:__ <t:{error_time.timestamp():.0f}:R>",color=discord.Color.red())
			except:
				error1=discord.Embed(title="An error occurred.",
								description=f"Caused by **{ctx.command}**\n__Author ID:__ {ctx.author} `{ctx.author.id}`\n__Occured:__ <t:{error_time.timestamp():.0f}:R>",color=discord.Color.red())
			error1.add_field(name="Error",value=f"```py\n...{er[-1000:]}\n```")
			await errorc2.send(embed=error1)





	@listener()
	async def on_command_error(self, ctx, error):

		# CommandNotFound
		if isinstance(error, commands.errors.CommandNotFound):
			return None

		# CommandInvokeError
		elif isinstance(error,commands.CommandInvokeError):
			error_time: datetime = datetime.utcnow().replace(tzinfo=timezone.utc)

			traceb2 = traceback.format_exception(type(error), error, error.__traceback__)
			traceb = ''.join(traceb2)
			traceb = traceb.replace('`','')
			traceb = traceb.replace('\\n','\n')
			traceb = traceb.replace('\\t','\t')
			traceb = traceb.replace('\\r','\r')
			traceb = traceb.replace("\\","/")
			er = ""
			for i in traceb:
				er = er + f"{i}"
			embed=discord.Embed(title="**Uh oh...**",description="An error occurred. The developer team is dealing with the problem now.\nJoin the [**Support Server**](https://discord.gg/rQHRQ8JjSY) for more help.",color=discord.Color.red())
			embed.add_field(name="Error",value=f'```py\n{type(error).__name__}: {error}\n```')
			await ctx.send(embed=embed, hidden=True)

			errorc2 = await self.bot.fetch_channel(862636687226044436)
			try:
				error=discord.Embed(title="An error occurred.",
						description=f"Caused by **{ctx.command}**\n__Author:__ {ctx.author} `{ctx.author.id}`\n__Guild:__ {ctx.guild.name} `{ctx.guild.id}`\n__Occured:__ <t:{error_time.timestamp():.0f}:R>",color=discord.Color.red())
			except:
				error=discord.Embed(title="An error occurred.",
						description=f"Caused by **{ctx.command}**\n__Author ID:__ {ctx.author} `{ctx.author.id}`\n__Occured:__ <t:{error_time.timestamp():.0f}:R>",color=discord.Color.red())
			try:
				error.add_field(name="Error",value=f"```py\n{traceb}\n```")
				await errorc2.send(embed=error)
			except Exception as e:
				try:
					error1=discord.Embed(title="An error occurred.",
									description=f"Caused by **{ctx.command}**\n__Author:__ {ctx.author} `{ctx.author.id}`\n__Guild:__ {ctx.guild.name} `{ctx.guild.id}`\n__Occured:__ <t:{error_time.timestamp():.0f}:R>",color=discord.Color.red())
				except:
					error1=discord.Embed(title="An error occurred.",
									description=f"Caused by **{ctx.command}**\n__Author ID:__ {ctx.author} `{ctx.author.id}`\n__Occured:__ <t:{error_time.timestamp():.0f}:R>",color=discord.Color.red())
				error1.add_field(name="Error",value=f"```py\n...{er[-1000:]}\n```")
				await errorc2.send(embed=error1)

		# MissingRequiredArgument
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send(f"{error}")

		# BadUnionArgument
		elif isinstance(error, commands.errors.BadUnionArgument):
			await ctx.send(f"{error}")

		# BadArgument
		elif isinstance(error,commands.BadArgument):
			await ctx.send(f"{error}")

		# EmojiNotFound
		elif isinstance(error, commands.EmojiNotFound):
			await ctx.send(f"{error}")
		
		# NotOwner
		elif isinstance(error, commands.NotOwner):
			await ctx.send(f"No!")







def setup(bot):
	bot.add_cog(Error(bot))
