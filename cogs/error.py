'''

This is a cog for error handler.
This will define ``on_command_error`` and ``on_slash_command_error``.
If there is an error during the execution of a command, it will send a traceback.

'''






import discord
from discord.ext import commands
import discord_slash
from discord_slash.context import InteractionContext
from datetime import datetime, timezone
import traceback



class Error(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		# No idea what I am doing here
		error_time: datetime = datetime.utcnow().replace(tzinfo=timezone.utc)
		traceb2 = traceback.format_exception(type(error), error, error.__traceback__)
		traceb = ''.join(traceb2)
		traceb = traceb.replace('`','')
		traceb = traceb.replace('\\n','\n')
		traceb = traceb.replace('\\t','\t')
		traceb = traceb.replace('\\r','\r')
		traceb = traceb.replace("\\","/")
		# Format the messaege
		embed = discord.Embed(title="An error occured", description=f"Command **{ctx.command}** triggered an error during execution")
		embed.add_field(name="Error",value=f'```py\n{type(error).__name__}: {error}\n```')
		await ctx.send(embed=embed)





def setup(bot):
	bot.add_cog(Error(bot))