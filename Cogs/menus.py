import interactions as i
from interactions import SelectMenu, SelectOption, Embed
from interactions import extension_user_command as user_command
from interactions import extension_message_command as message_command
from interactions.ext import wait_for
from googletrans import Translator
import os
from dotenv import load_dotenv
load_dotenv()
scope = int(os.getenv("SCOPE"))






class Menus(i.Extension):
	def __init__(self, bot):
		self.bot = bot
		wait_for.setup(bot, add_method=True)

	
	@message_command(
		name="Translate",
		scope=scope
	)
	async def translate(self, ctx: i.CommandContext):
		translator = Translator()
		message = ctx.target
		content = message.content
		lang = translator.detect(content).lang
		translation = translator.translate(content)
		message1 = translation.text
		# Format the embed
		footer = i.EmbedFooter(text="Powered by Google Translate", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png")
		embed = i.Embed(title=f"Detected language: {lang}", description=f"```{message1}```", footer=footer)
		# Select menu
		select_menu = i.SelectMenu(
				options = [
					SelectOption(
						label = "English",
						value = "en",
					),
					SelectOption(
						label = "French",
						value = "fr",
					),
					SelectOption(
						label = "Spanish",
						value = "es",
					),
					SelectOption(
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
				embed = Embed(title=f"Detected language: {lang}", description=f"```{message1}```")
				embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png", text="Google Translate")
				await res.send(embeds=embed, components=select_menu, ephemeral=True)
			elif selects == "fr":
				translation = translator.translate(content, dest='fr')
				message1 = translation.text
				embed = Embed(title=f"Detected language: {lang}", description=f"```{message1}```")
				embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png", text="Google Translate")
				await res.send(embeds=embed, components=select_menu, ephemeral=True)
			elif selects == "es":
				translation = translator.translate(content, dest='es')
				message1 = translation.text
				embed = Embed(title=f"Detected language: {lang}", description=f"```{message1}```")
				embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png", text="Google Translate")
				await res.send(embeds=embed, components=select_menu, ephemeral=True)
			elif selects == "zh-CN":
				translation = translator.translate(content, dest='zh-CN')
				message1 = translation.text
				embed = Embed(title=f"Detected language: {lang}", description=f"```{message1}```")
				embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png", text="Google Translate")
				await res.send(embeds=embed, components=select_menu, ephemeral=True)


		




def setup(bot):
	Menus(bot)