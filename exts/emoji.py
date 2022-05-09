import interactions
from interactions import extension_command as command
import os, io, aiohttp, re
from dotenv import load_dotenv
load_dotenv()
scope = int(os.getenv("SCOPE"))


class Emoji(interactions.Extension):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot = bot


	@command(
		name="emoji",
		description="Emoji commands",
		scope=scope,
		options=[
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="info",
				description="Get the information about an emoji",
				options=[
					interactions.Option(
						type=interactions.OptionType.STRING,
						name="emoji",
						description="Targeted emoji",
						required=True
					)
				]
			),
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="steal",
				description="Steal an emoji from another server and add it to the current server",
				options=[
					interactions.Option(
						type=interactions.OptionType.STRING,
						name="emoji",
						description="Targeted emoji",
						required=True
					),
					interactions.Option(
						type=interactions.OptionType.STRING,
						name="name",
						description="Name for the stolen emoji",
						required=False
					)
				]
			)
		]
	)
	async def _emoji(self, ctx: interactions.CommandContext,
		sub_command: str,
		emoji: str,
		name: str = None
	):
		if sub_command == "info":
			if emoji.startswith("<") and not emoji.startswith("<a") and emoji.endswith(">"):
				s = [pos for pos, char in enumerate(emoji) if char == ':']
				if len(s) == 2:
					for i in s:
						if i != 1:
							emoji = emoji[i:]
							break
					emoji_id = int(emoji[1:-1])
					_emoji = interactions.Emoji(**await self.bot._http.get_guild_emoji(int(ctx.guild_id), int(emoji_id)),  _client=self.bot._http)
					if _emoji.name is not None:
						image = interactions.EmbedImageStruct(url=_emoji.url)
						embed = interactions.Embed(
							title=f"``<:{_emoji.name}:{_emoji.id}>``",
							description=f"[Emoji link]({_emoji.url})",
							color=0x788cdc,
							image=image
						)
						await ctx.send(content=f"<{_emoji.url}>", embeds=embed)
					else:
						await ctx.send("Invalid emoji. Please try again and make sure that it is **from** this server.\nError code: 404", ephemeral=True)
				else:
					await ctx.send("Invalid emoji. Please try again.\nError code: 400", ephemeral=True)

			elif emoji.startswith("<a") and emoji.endswith(">"):
				s = [pos for pos, char in enumerate(emoji) if char == ':']
				if len(s) == 2:
					for i in s:
						if i != 2:
							emoji = emoji[i:]
							break
					emoji_id = int(emoji[1:-1])
					_emoji = interactions.Emoji(**await self.bot._http.get_guild_emoji(int(ctx.guild_id), int(emoji_id)),  _client=self.bot._http)
					if _emoji.name is not None:
						image = interactions.EmbedImageStruct(url=_emoji.url)
						embed = interactions.Embed(
							title=f"``<a:{_emoji.name}:{_emoji.id}>``",
							description=f"[Emoji link]({_emoji.url})",
							color=0x788cdc,
							image=image
						)
						await ctx.send(content=f"<{_emoji.url}>", embeds=embed)
					else:
						await ctx.send("Invalid emoji. Please try again and make sure that it is **from** this server.\nError code: 404", ephemeral=True)
				else:
					await ctx.send("Invalid emoji. Please try again.\nError code: 400", ephemeral=True)

			else:
				await ctx.send("Invalid emoji. Please try again.\nError code: 400", ephemeral=True)

		elif sub_command == "steal":
			if emoji.startswith("<") and not emoji.startswith("<a") and emoji.endswith(">"):
				msg = await ctx.send("Getting emoji...")
				s = [pos for pos, char in enumerate(emoji) if char == ':']
				if len(s) == 2:
					for i in s:
						if i != 1:
							_emoji = emoji[i:]
							break
					emoji_id = int(_emoji[1:-1])
					if name is None:
						emoji_name = re.findall(r"(?<=:)(.*)(?=:)", emoji)[0]
					else:
						emoji_name = name
					_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.png"
					guild = await ctx.get_guild()
					async with aiohttp.ClientSession() as session:
						async with session.get(_url) as resp:
							if resp.status == 200:
								_io = (io.BytesIO(await resp.read())).read()
								await msg.edit(content="Uploading emoji...")
								image = interactions.Image(fp=_io, file="unknown.png")
								await guild.create_emoji(image=image, name=emoji_name)
								await msg.edit(content="Emoji uploaded!")
							else:
								await msg.edit(content="Invalid url. Please try again.")
				else:
					await msg.edit(content="Invalid emoji. Please try again.")
			elif emoji.startswith("<a") and emoji.endswith(">"):
				msg = await ctx.send("Getting emoji...")
				s = [pos for pos, char in enumerate(emoji) if char == ':']
				if len(s) == 2:
					for i in s:
						if i != 2:
							_emoji = emoji[i:]
							break
					emoji_id = int(_emoji[1:-1])
					if name is None:
						emoji_name = re.findall(r"(?<=:)(.*)(?=:)", emoji)[0]
					else:
						emoji_name = name
					_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.gif"
					guild = await ctx.get_guild()
					async with aiohttp.ClientSession() as session:
						async with session.get(_url) as resp:
							if resp.status == 200:
								_io = (io.BytesIO(await resp.read())).read()
								await msg.edit(content="Uploading emoji...")
								image = interactions.Image(fp=_io, file="unknown.gif")
								await guild.create_emoji(image=image, name=emoji_name)
								await msg.edit(content="Emoji uploaded!")
							else:
								await msg.edit(content="Invalid url. Please try again.")
				else:
					await msg.edit(content="Invalid emoji. Please try again.")






def setup(bot):
	Emoji(bot)
