import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, SlashCommand
import random



class Fun(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@cog_ext.cog_slash(name="ship", description="Ship two users together")
	async def _ship(self, ctx: SlashContext, name1 = None, name2 = None):
		shipnumber = int(random.randint(0, 100))
		if not name1:
			name1 = ctx.author.name
			name_2 = random.choice(ctx.guild.members)
			name2 = name_2.name
		if not name2:
			name_1 = name1
			name2 = name_1
			name1 = ctx.author.name
		# Choose a random comment and heart emoji
		if 0 <= shipnumber <= 30:
			comment = "Really low! {}".format(random.choice(
				["Friendzone.", 
				'Just "friends".', 
				"There's barely any love."]))
			heart = ":broken_heart:"
		elif 31 <= shipnumber <= 70:
			comment = "Moderate! {}".format(random.choice(
				["Fair enough!",
				"A small bit of love is in the air...",
				"I feel like there's some romance progressing!"]))
			heart = ":mending_heart:"
		elif 71 <= shipnumber <= 90:
			comment = "Almost perfect! {}".format(random.choice(
				["I definitely can see that love is in the air",
				"I feel the love! There's a sign of a match!",
				"A few things can be imporved to make this a match made in heaven!"]))
			heart = random.choice(
				[":revolving_hearts:",
				":heart_exclamation:",
				":heart_on_fire",
				":heartbeat:"])
		elif 90 < shipnumber <= 100:
			comment = "True love! {}".format(random.choice(
				["It's a match!", 
				"There's a match made in heaven!", 
				"It's definitely a match!"]))
			heart = random.choice(
				[":sparkling_heart:",
				":heart_decoration",
				":hearts:",
				":two_hearts:",
				":heartpulse:"])
		# Choose color
		if shipnumber <= 40:
			shipColor = 0xE80303
		elif 41 < shipnumber < 80:
			shipColor = 0xff6600
		else:
			shipColor = 0x3be801
		# embed message
		embed = discord.Embed(description=f"**{name1}** {heart} **{name2}**" ,color=shipColor)
		embed.add_field(name="Results:", value=f"{shipnumber}%  {comment}", inline=True)
		await ctx.send(embed=embed)


def setup(bot: commands.Bot):
	bot.add_cog(Fun(bot))