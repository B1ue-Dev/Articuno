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


class Swear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        fp  = open('banned_word.txt')
        bad_list = [word.strip() for line in fp.readlines() for word in line.split(',') if word.strip()]
        guild = message.guild
        channel = discord.utils.get(guild.channels, name="📝║logs")
        mutedRole = discord.utils.get(message.guild.roles, name="🔇║Muted")

        embed1=discord.Embed(title="Muted successfully", colour=red)
        embed1.set_thumbnail(url=message.author.avatar_url)
        embed1.add_field(name="Member", value=message.author.mention + str(message.author), inline=False)
        embed1.add_field(name="ID", value=message.author.id, inline=False)
        embed1.add_field(name="Reason", value="Bad word contained in message content", inline=False)
        message.content=message.content.lower()
        if any(word in message.content for word in bad_list):
            await message.delete()
            await message.channel.send(f"<@{message.author.id}>, bad words aren't allowed here. Please read the rules again")
            await message.author.add_roles(mutedRole)
            await channel.send(embed=embed1)

def setup(bot):
    bot.add_cog(Swear(bot))
