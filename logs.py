import discord
from discord.ext import commands
import random

blue = 0x236adf
red = 0xff0000
orange = 0xff8b00
purple = 0xac10eb
black = 0xffffff
white = 0x000000
green = 0x3bcc12
yellow = 0xfff900
gray = 0x6d6868

snipe_message_author = {}
snipe_message_content = {}


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild = message.guild
        channel = discord.utils.get(guild.channels, name="📝║logs")
        embed = discord.Embed(timestamp=message.created_at, colour=red) 
        embed.set_author(name=f'{message.author.name}#{message.author.discriminator}', icon_url=message.author.avatar_url)
        embed.set_footer(text=f"Author ID:{message.author.id} • Message ID: {message.id}")
        embed.add_field(name="**Member**", value=f"<@{message.author.id}>", inline=True)
        embed.add_field(name="**Channel**", value=f"<#{message.channel.id}>", inline=True)
        embed.add_field(name="**Deleted message content**", value=message.content, inline=False)
        await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_message_edit(self,before,after):
        guild = before.guild
        channel = discord.utils.get(guild.channels, name="📝║logs")
        embed = discord.Embed(timestamp=before.created_at, colour=red) 
        embed.set_author(name=f'{before.author.name}#{before.author.discriminator}', icon_url=before.author.avatar_url)
        embed.set_footer(text=f"Author ID:{before.author.id} • Message ID: {before.id}")
        embed.add_field(name="**Member**", value=f"<@{before.author.id}>", inline=True)
        embed.add_field(name="**Channel**", value=f"<#{before.channel.id}>", inline=True)
        embed.add_field(name="**Message content before edited**", value=before.content, inline=False)
        embed.add_field(name="**Message content after edited**", value=after.content, inline=False)
        await channel.send(embed=embed)



    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        welcome1 = discord.utils.get(guild.channels, name="👋║welcome")
        welcome2 = discord.utils.get(guild.channels, name="greets")

        log = discord.utils.get(guild.channels, name="📝║logs")

        memberRole1 = discord.utils.get(guild.roles, name="👤║Member")
        memberRole2 = discord.utils.get(guild.roles, name="Simp")

        join = discord.Embed(color=random.randint(0, 0xFFFFFF))
        join.set_thumbnail(url=member.avatar_url)
        join.set_footer(text=f"Member ID: {member.id}")
        join.add_field(name=f"Welcome :partying_face:", value=f"Welcome to {guild.name}, **{member.name}**", inline=False)

        logger = discord.Embed(color=random.randint(0, 0xFFFFFF))
        logger.set_thumbnail(url=member.avatar_url)
        logger.set_footer(text=f"Member ID: {member.id}")
        logger.add_field(name="Member's name", value=str(member.name), inline=True)
        logger.add_field(name="Member's ID", value=member.id, inline=True)
        logger.add_field(name="Joined on", value=member.joined_at.strftime("%B %d, %Y"), inline=False)
        logger.add_field(name="Created on", value=member.created_at.strftime("%B %d, %Y"), inline=False)

        try:
            await member.add_roles(memberRole1)
        except:
            await member.add_roles(memberRole2)
        try:
            await welcome1.send(embed=join)
        except:
            await welcome2.send(embed=join)
        await log.send(embed=logger)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        bye1 = discord.utils.get(guild.channels, name="👋║welcome")
        bye2 = discord.utils.get(guild.channels, name="greets")

        embed = discord.Embed(color=random.randint(0, 0xFFFFFF))
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Member ID: {member.id}")
        embed.add_field(name=f"Goodbye :cry:", value=f"Goodbye, **{member.name}**. Thanks for joining {guild.name}", inline=False)

        try:
            await bye1.send(embed=embed)
        except:
            await bye2.send(embed=embed)
        


def setup(bot):
    bot.add_cog(Logs(bot))
