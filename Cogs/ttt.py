from discord.ext import commands



class ttt(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.load_extension("Cogs.tictactoe.easy")
		self.bot.load_extension("Cogs.tictactoe.hard")


def setup(bot):
	bot.add_cog(ttt(bot))