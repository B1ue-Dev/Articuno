import discord
from discord.ext import commands


blue = 0x236adf
red = 0xff0000
orange = 0xff8b00
purple = 0xac10eb
black = 0xffffff
white = 0x000000
green = 0x3bcc12
yellow = 0xfff900
gray = 0x6d6868


class Error(commands.Cog):
    def __init__(self,bot):
          self.bot = bot
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error): #exceptions, will add more
      if isinstance(error,commands.MissingPermissions):
        embed=discord.Embed(title=f"{ctx.author.name}, you made an error <:angery:859696959337529345>",description=f"Error: Missing Permission",color=red)
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("❌")

      elif isinstance(error,commands.BotMissingPermissions):
        error = str(error)
        error = error.replace('Bot requires', '')
        error = error.replace('permission(s) to run this command.', '')
        embed=discord.Embed(title=f"{ctx.author.name}, you made an error <:angery:859696959337529345>",description=f"Error: Bot Missing Permission",color=red)
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("❌")

      elif isinstance(error, commands.BotMissingPermissions):
        embed=discord.Embed(title=f"{ctx.author.name}, you made an error <:angery:859696959337529345>",description=f"Error: Missing Permission",color=red)
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("❌")

      elif isinstance(error,commands.MissingRequiredArgument):
        embed=discord.Embed(title=f"{ctx.author.name}, you made an error <:angery:859696959337529345>",description=f"Error: Missing Required Argument",color=red)
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("❌")

      elif isinstance(error,commands.BadArgument):
        embed=discord.Embed(title=f"{ctx.author.name}, you made an error <:angery:859696959337529345>",description=f"Error: Bad Argument", color=red)
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("❌")

      elif isinstance(error, commands.errors.MissingRequiredArgument):
        embed=discord.Embed(title=f"{ctx.author.name}, you made an error <:angery:859696959337529345>",description=f"Error: Missing Required Argument",color=red)
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("❌")

      elif isinstance(error, commands.errors.CommandNotFound):
        embed=discord.Embed(title=f"{ctx.author.name}, you made an error <:angery:859696959337529345>", description=f"Error: Command not found",color=red)
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("❌")

      elif isinstance(error, commands.errors.CommandInvokeError):
        embed=discord.Embed(title=f"Oh god!", description=f"Uh oh, this command has a problem. Ping <@738937306224001157> so he can solve this",color=red)
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("❌")
        await self.bot.get_channel(867039086387789874).send(content=discord.utils.escape_mentions("Something wrong"))
      if isinstance(error, commands.CommandOnCooldown):
        embed=discord.Embed(title=f"{ctx.author.name}, you made an error <:angery:859696959337529345>",description=f"Command On Cool Down. Try again in {error.retry_after:.2f}s.", color=red)
        await ctx.message.add_reaction("❌")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Error(bot))
