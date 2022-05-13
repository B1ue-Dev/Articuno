import interactions
from interactions import extension_user_command as user_command
from interactions import extension_message_command as message_command
from interactions.ext import wait_for
from googletrans import Translator






class Menus(interactions.Extension):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot = bot
		wait_for.setup(bot, add_method=True)

	
	@message_command(
		name="Translate"
	)
	async def _translate(self, ctx: interactions.CommandContext):
		translator = Translator()
		message = ctx.target
		content = message.content
		lang = translator.detect(content).lang
		translation = translator.translate(content)
		message1 = translation.text

		footer = interactions.EmbedFooter(text="Powered by Google Translate", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png")
		embed = interactions.Embed(
			title=f"Detected language: {lang}",
			description=f"```{message1}```",
			footer=footer
		)

		select_menu = interactions.SelectMenu(
			options = [
				interactions.SelectOption(
					label = "English",
					value = "en",
				),
				interactions.SelectOption(
					label = "French",
					value = "fr",
				),
				interactions.SelectOption(
					label = "Spanish",
					value = "es",
				),
				interactions.SelectOption(
					label = "Chinese",
					value = "zh-CN",
				)
			],
			placeholder = "Select a language",
			custom_id = "select_menu",
		)
		await ctx.send(embeds=embed, components=select_menu, ephemeral=True)

		while True:
			res = await self.bot.wait_for_component(components=select_menu)
			selects = res.data.values[0]
			if selects == "en":
				translation = translator.translate(content, dest='en')
				message1 = translation.text
				embed = interactions.Embed(title=f"Detected language: {lang}", description=f"```{message1}```")
				embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png", text="Google Translate")
				await res.send(embeds=embed, components=select_menu, ephemeral=True)
			elif selects == "fr":
				translation = translator.translate(content, dest='fr')
				message1 = translation.text
				embed = interactions.Embed(title=f"Detected language: {lang}", description=f"```{message1}```")
				embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png", text="Google Translate")
				await res.send(embeds=embed, components=select_menu, ephemeral=True)
			elif selects == "es":
				translation = translator.translate(content, dest='es')
				message1 = translation.text
				embed = interactions.Embed(title=f"Detected language: {lang}", description=f"```{message1}```")
				embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png", text="Google Translate")
				await res.send(embeds=embed, components=select_menu, ephemeral=True)
			elif selects == "zh-CN":
				translation = translator.translate(content, dest='zh-CN')
				message1 = translation.text
				embed = interactions.Embed(title=f"Detected language: {lang}", description=f"```{message1}```")
				embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png", text="Google Translate")
				await res.send(embeds=embed, components=select_menu, ephemeral=True)
	


	@user_command(
		name="User Information"
	)
	async def _user_information(self, ctx: interactions.CommandContext):
		name = ctx.target.user.username
		discriminator = int(ctx.target.user.discriminator)
		id = int(ctx.target.user.id)
		joined_at = round(ctx.target.joined_at.timestamp())
		created_at = ctx.target.user.id.epoch
		avatar = ctx.target.user.avatar_url
		bot = ctx.target.user.bot
		if bot is True:
			bot = "Yes"
		else:
			bot = "No"

		thumbnail = interactions.EmbedImageStruct(url=avatar)
		fields = [
			interactions.EmbedField(name="Name", value=f"{name}#{discriminator}", inline=True),
			interactions.EmbedField(name="ID", value=id, inline=True),
			interactions.EmbedField(name="Joined at", value=f"<t:{joined_at}>", inline=False),
			interactions.EmbedField(name="Created on", value=f"<t:{created_at}>", inline=False),
			interactions.EmbedField(name="Bot?", value=bot, inline=True),
		]
		embed = interactions.Embed(
			title=f"User Information",
			thumbnail=thumbnail,
			fields=fields
		)

		await ctx.send(embeds=embed, ephemeral=True)






def setup(bot):
	Menus(bot)
