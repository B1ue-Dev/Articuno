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
from googletrans import Translator


context_menu = cog_ext.cog_context_menu


class ContextMenuMessage(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@context_menu(target=ContextMenuType.USER,
                name="Information",
                )
	async def _user_menu(self, ctx: MenuContext):
		member = ctx.target_author
		# Check if bot
		if not member.bot:
			bot = "No"
		else:
			bot = "Yes"
		# Highest role's color
		color = member.top_role.color
		# Joined date
		joined = f"<t:{member.joined_at.timestamp():.0f}:R>"
		# Account creation date
		created = f"<t:{member.created_at.timestamp():.0f}:R>"
		embed=discord.Embed(colour=color)
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_author(name=f"{member.name}'s information", icon_url=member.avatar_url)
		embed.add_field(name="Name", value=member, inline=True)
		if member.nick is True:
			embed.add_field(name="Nickname", value=member.nick, inline=True)
		else:
			pass
		embed.add_field(name="ID", value=member.id, inline=True)
		embed.add_field(name="Joined", value=joined, inline=False)
		embed.add_field(name="Created", value=created, inline=False)
		embed.add_field(name="Bot?", value=bot)
		await ctx.send(embed=embed, hidden=True)


	@context_menu(target=ContextMenuType.MESSAGE,
				name="Translate",
                )
	async def Translate(self, ctx: MenuContext):
		translator = Translator()
		message = ctx.target_message.content
		lang = translator.detect(message).lang
		translation = translator.translate(message)
		message1 = translation.text
		# Selection
		select = create_select(
			options = [
				create_select_option('English', '1', '🇬🇧', 'English'),
				create_select_option('French', '2', '🇫🇷', 'French'),
				create_select_option('Spanish', '3', '🇪🇸', 'Spanish'),
				create_select_option('Chinese', '4', '🇨🇳', 'Chinese'),
				create_select_option('Vietnamese', '5', '🇻🇳', 'Vietnamese'),
			],
			placeholder = 'Select a language',
			min_values = 1,
			max_values = 1,
		)
		selection = create_actionrow(select)
		embed = discord.Embed(title=f"Detected language: {lang}", description=f"```{message1}```", color=discord.Color.dark_theme())
		embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png", text="Google Translate")
		msg = await ctx.send(embed=embed, components=[selection], hidden=True)
		while True:
			cmp1: ComponentContext = await wait_for_component(self.bot, components=[selection])
			selects = int(cmp1.selected_options[0])
			if selects == 1:
				translation = translator.translate(message, dest='en')
				message1 = translation.text
				embed = discord.Embed(title=f"Detected language: {lang}", description=f"```{message1}```", color=discord.Color.dark_theme())
				embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png", text="Google Translate")
				await cmp1.send(embed=embed, components=[selection], hidden=True)
			elif selects == 2:
				translation = translator.translate(message, dest='fr')
				message1 = translation.text
				embed = discord.Embed(title=f"Detected language: {lang}", description=f"```{message1}```", color=discord.Color.dark_theme())
				embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png", text="Google Translate")
				await cmp1.send(embed=embed, components=[selection], hidden=True)
			elif selects == 3:
				translation = translator.translate(message, dest='es')
				message1 = translation.text
				embed = discord.Embed(title=f"Detected language: {lang}", description=f"```{message1}```", color=discord.Color.dark_theme())
				embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png", text="Google Translate")
				await cmp1.send(embed=embed, components=[selection], hidden=True)
			elif selects == 4:
				translation = translator.translate(message, dest='zh-CN')
				message1 = translation.text
				embed = discord.Embed(title=f"Detected language: {lang}", description=f"```{message1}```", color=discord.Color.dark_theme())
				embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png", text="Google Translate")
				await cmp1.send(embed=embed, components=[selection], hidden=True)
			elif selects == 5:
				translation = translator.translate(message, dest='vi')
				message1 = translation.text
				embed = discord.Embed(title=f"Detected language: {lang}", description=f"```{message1}```", color=discord.Color.dark_theme())
				embed.set_footer(icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png", text="Google Translate")
				await cmp1.send(embed=embed, components=[selection], hidden=True)




def setup(bot: commands.Bot):
	bot.add_cog(ContextMenuMessage(bot))
