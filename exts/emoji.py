import interactions
from interactions import extension_command as command
import io, aiohttp, re
from utils.permission import Permissions, has_permission


class Emoji(interactions.Extension):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot = bot


	@command(
		name="emoji",
		description="Emoji commands",
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
			),
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="add",
				description="Add an emoji from an url to the current server",
				options=[
					interactions.Option(
						type=interactions.OptionType.STRING,
						name="url",
						description="Url to the emoji",
						required=True
					),
					interactions.Option(
						type=interactions.OptionType.STRING,
						name="name",
						description="Name for the added emoji",
						required=True
					)
				]
			),
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="remove",
				description="Remove an emoji from the current server",
				options=[
					interactions.Option(
						type=interactions.OptionType.STRING,
						name="emoji",
						description="Targeted emoji",
						required=True
					)
				]
			)
		]
	)
	async def _emoji(self, ctx: interactions.CommandContext,
		sub_command: str,
		emoji: str = None,
		url: str = None,
		name: str = None
	):
		if sub_command == "info":
			await self._emoji_info(ctx, emoji)
		elif sub_command == "steal":
			await self._emoji_steal(ctx, emoji, name)
		elif sub_command == "add":
			await self._emoji_add(ctx, url, name)
		elif sub_command == "remove":
			await self._emoji_remove(ctx, emoji)


	async def _emoji_info(self, ctx: interactions.CommandContext, emoji: str):
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
		
		elif emoji.isnumeric() and len(emoji) > 0:
			emoji_id = int(emoji)
			_emoji = interactions.Emoji(**await self.bot._http.get_guild_emoji(int(ctx.guild_id), int(emoji_id)),  _client=self.bot._http)
			if _emoji.name is not None:
				image = interactions.EmbedImageStruct(url=_emoji.url)
				title = f"``<:{_emoji.name}:{_emoji.id}>``" if _emoji.url.endswith(".png") else f"``<a:{_emoji.name}:{_emoji.id}>``"
				embed = interactions.Embed(
					title=title,
					description=f"[Emoji link]({_emoji.url})",
					color=0x788cdc,
					image=image
				)
				await ctx.send(content=f"<{_emoji.url}>", embeds=embed)
			else:
				await ctx.send("Invalid emoji. Please try again and make sure that it is **from** this server.\nError code: 404", ephemeral=True)

		else:
			await ctx.send("Invalid emoji. Please try again.\nError code: 400", ephemeral=True)


	async def _emoji_steal(self, ctx: interactions.CommandContext, emoji: str, name: str = None):
		if not (
			has_permission(int(ctx.author.permissions), Permissions.MANAGE_EMOJIS_AND_STICKERS) or
			has_permission(int(ctx.author.permissions), Permissions.ADMINISTRATOR)
		):
			await ctx.send(content="You do not have manage emojis and stickers permission.", ephemeral=True)
			return
		else:
			if emoji.startswith("<") and not emoji.startswith("<a") and emoji.endswith(">"):
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
								image = interactions.Image(fp=_io, file="unknown.png")
								await guild.create_emoji(image=image, name=emoji_name)
								await ctx.send(f"Emoji uploaded!")
							else:
								await ctx.send(content="Invalid url. Please try again.\nError code: 404", ephemeral=True)
				else:
					await ctx.send(content="Invalid emoji. Please try again.\nError code: 400", ephemeral=True)

			elif emoji.startswith("<a") and emoji.endswith(">"):
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
								image = interactions.Image(fp=_io, file="unknown.gif")
								await guild.create_emoji(image=image, name=emoji_name)
								await ctx.send(content="Emoji uploaded!")
							else:
								await ctx.send(content="Invalid url. Please try again.\nError code: 404", ephemeral=True)
				else:
					await ctx.send(content="Invalid emoji. Please try again.", ephemeral=True)

			else:
				await ctx.send("Invalid emoji. Please try again.", ephemeral=True)


	async def _emoji_add(self, ctx: interactions.CommandContext, url: str, name: str):
		if not (
			has_permission(int(ctx.author.permissions), Permissions.MANAGE_EMOJIS_AND_STICKERS) or
			has_permission(int(ctx.author.permissions), Permissions.ADMINISTRATOR)
		):
			await ctx.send(content="You do not have manage emojis and stickers permission.", ephemeral=True)
			return
		else:
			async with aiohttp.ClientSession() as session:
				async with session.get(url) as resp:
					if resp.status == 200:
						if resp.content_type in {"image/png", "image/jpeg", "imgage/jpg, image/webp"}:
							_io = (io.BytesIO(await resp.read())).read()
							image = interactions.Image(fp=_io, file="unknown.png")
							guild = await ctx.get_guild()
							await guild.create_emoji(image=image, name=name)
							await ctx.send(content="Emoji uploaded!")
						elif resp.content_type in {"image/gif"}:
							_io = (io.BytesIO(await resp.read())).read()
							image = interactions.Image(fp=_io, file="unknown.gif")
							guild = await ctx.get_guild()
							await guild.create_emoji(image=image, name=name)
							await ctx.send(content="Emoji uploaded!")
						else:
							await ctx.send(content="Invalid url. Please try again.\nSupported format: png, jpeg, jpg, webp, gif", ephemeral=True)
					else:
						await ctx.send(content="Invalid url. Please try again.", ephemeral=True)
	

	async def _emoji_remove(self, ctx: interactions.CommandContext, emoji: str):
		if not (
			has_permission(int(ctx.author.permissions), Permissions.MANAGE_EMOJIS_AND_STICKERS) or
			has_permission(int(ctx.author.permissions), Permissions.ADMINISTRATOR)
		):
			await ctx.send(content="You do not have manage emojis and stickers permission.", ephemeral=True)
			return
		else:
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
						guild = await ctx.get_guild()
						await guild.delete_emoji(_emoji)
						await ctx.send(content="Emoji deleted!", ephemeral=True)
					else:
						await ctx.send(content="Invalid emoji. Please try again and make sure that it is **from** this server.\nError code: 404", ephemeral=True)

			elif emoji.startswith("<a") and emoji.endswith(">"):
				s = [pos for pos, char in enumerate(emoji) if char == ':']
				if len(s) == 2:
					for i in s:
						if i != 2:
							_emoji = emoji[i:]
							break
					emoji_id = int(_emoji[1:-1])
					_emoji = interactions.Emoji(**await self.bot._http.get_guild_emoji(int(ctx.guild_id), int(emoji_id)),  _client=self.bot._http)
					if _emoji.name is not None:
						guild = await ctx.get_guild()
						await guild.delete_emoji(_emoji)
						await ctx.send(content="Emoji deleted!", ephemeral=True)
					else:
						await ctx.send(content="Invalid emoji. Please try again and make sure that it is **from** this server.\nError code: 404", ephemeral=True)
		
			elif emoji.isnumeric() and len(emoji) > 0:
				emoji_id = int(emoji)
				_emoji = interactions.Emoji(**await self.bot._http.get_guild_emoji(int(ctx.guild_id), int(emoji_id)),  _client=self.bot._http)
				if _emoji.name is not None:
					guild = await ctx.get_guild()
					await guild.delete_emoji(_emoji)
					await ctx.send(content="Emoji deleted!", ephemeral=True)
				else:
					await ctx.send(content="Invalid emoji. Please try again and make sure that it is **from** this server.\nError code: 404", ephemeral=True)
		
			else:
				await ctx.send("Invalid emoji. Please try again.", ephemeral=True)

	









def setup(bot):
	Emoji(bot)
