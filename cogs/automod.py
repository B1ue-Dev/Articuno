import discord
from discord.ext import commands




class AutoMod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if "@everyone" in message.content or "@here" in message.content:
            if message.author.guild_permissions.administrator:
            # If the user has administrator role (admin or owner), it will not be blocked
                return
            else:
            # If the user doesn't have enough role and try to ping everyone, it will
            # be blocked
                await message.delete()
                await message.channel.send(
                    f"<@{message.author.id}>, don't try to ping everyone.")





def setup(bot):
    bot.add_cog(AutoMod(bot))