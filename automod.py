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


class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        guild = message.guild
        channel = discord.utils.get(guild.channels, name="📝║logs")

        if "@everyone" in message.content or "@here" in message.content:
            if message.author.guild_permissions.administrator:
                return
            else:
                await message.delete()
                await message.channel.send(
                    f"<@{message.author.id}>, nice try. Mods have been noticed and will have a suitable punishment for you"
                )

        embed2 = discord.Embed(title="Muted successfully", colour=red)
        embed2.set_thumbnail(url=message.author.avatar_url)
        embed2.add_field(name="Member",
                         value=message.author.mention + str(message.author),
                         inline=False)
        embed2.add_field(name="ID", value=message.author.id, inline=False)
        embed2.add_field(name="Reason", value="Sent invite link", inline=False)

        if "https://discord.gg" in message.content or "http://discord.gg" in message.content:
            await message.delete()
            await message.channel.send(
                f"<@{message.author.id}>, invite links aren't allowed here. Please read the rules again"
            )
            await channel.send(embed=embed2)

        if "<@!851064798333501480>" in message.content or "@Articuno#5180" in message.content:
            embed = discord.Embed(
                title="It seems like you mentioned me",
                description=
                "I couldn't help but notice you mentioned me. My prefix is ``$``. You can use ``$help`` to see a list of available commands that I have <:seemsDerp:859104289637269555>",
                color=blue)
            await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(AutoMod(bot))
