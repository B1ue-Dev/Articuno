import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, SlashCommand, ComponentContext
from discord_slash.utils.manage_components import (
	create_button,
	create_actionrow,
	create_select,
	create_select_option,
	wait_for_component,
)
from discord_slash.model import ButtonStyle, ContextMenuType
from discord_slash.context import InteractionContext, MenuContext
from discord_slash.utils.manage_commands import create_option, create_choice
import base64 as b64


# As always, lazy
subcommand = cog_ext.cog_subcommand



'''

Excuse me, but no!

'''



class Hacktool(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	guild_ids = [833886728259239968, 859030372783751168, 738938246574374913]


	@subcommand(base="base64",
				name="encode",
				description="Encode a string (base64)"
				)
	async def encode(self, ctx: commands.Context, message: str):
		string_message = message
		string_bytes = string_message.encode("utf-8")
		base64_bytes = b64.b64encode(string_bytes)
		base64_string = base64_bytes.decode("utf-8")
		await ctx.send(f"```{base64_string}```")


	@subcommand(base="base64",
				name="decode",
				description="Decode a string (base64)"
				)
	async def decode(self, ctx: commands.Context, message: str):
		string_message = message
		string_bytes = string_message.encode("utf-8")
		try:
			base64_bytes = b64.b64decode(string_bytes)
			base64_string = base64_bytes.decode("utf-8")
			await ctx.send(f"```{base64_string}```")
		except:
			await ctx.send("```Invalid string. Please try again!```", hidden=True)





def setup(bot: commands.Bot):
	bot.add_cog(Hacktool(bot))
