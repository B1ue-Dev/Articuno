import discord
from discord.ext import commands
import random
from discord.ext.commands import Greedy
from discord import User
import asyncio
from typing import Union
import requests


blue = 0x236adf
red = 0xff0000
orange = 0xff8b00
purple = 0xac10eb
black = 0xffffff
white = 0x000000
green = 0x3bcc12
yellow = 0xfff900
gray = 0x6d6868

class Server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="About the channel")
    async def server(self, ctx):
        name = str(ctx.guild.name)
        id = str(ctx.guild.id)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        owner = str(ctx.guild.owner.id)
        region = str(ctx.guild.region)
        created = str(ctx.guild.created_at.strftime("%B %d, %Y"))

        embed = discord.Embed(title=name + " Information", color=blue)
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Member Count", value=memberCount + ":people_holding_hands:", inline=True)
        embed.add_field(name="Owner", value=f"<@{owner}>", inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Created on", value=created, inline=True)
        embed.set_footer(text=f"Owner: {ctx.guild.owner.name}")

        await ctx.send(embed=embed)



    @commands.command(description="Gets info about a specified user")
    async def info(self, ctx, member : discord.Member=None):
        if not member:
          member = ctx.author

        embed=discord.Embed(title="User info", colour=random.randint(0, 0xFFFFFF))
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Name", value=member.name, inline=True)
        embed.add_field(name="Nickname", value=member.nick, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Joined on", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="Top role", value=member.top_role.name, inline=True)
        embed.add_field(name="Created on", value=member.created_at.strftime("%B %d, %Y"), inline=True)
        embed.set_footer(icon_url=member.avatar_url, text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    

    @commands.command(description="DM yourself")
    async def dm(self, ctx, *, message):
      try:
        embed = discord.Embed(title=f"Here is the message:", description=f"{message}", color=green)
        await ctx.author.send(embed=embed)
        await ctx.message.add_reaction("✅")
        await ctx.channel.send(':white_check_mark: Message delivered successfully')
      except:
        await ctx.message.add_reaction("❌")
        await ctx.channel.send(f"{ctx.author.mention}, your DM is closed. I can't deliver the message to you")


    @commands.command(description="*For admin only*: DM a group of member")
    @commands.has_permissions(administrator = True)
    async def message(self, ctx, users: Greedy[User], *, message):
      try:
        for user in users:
            embed = discord.Embed(title=f"From {ctx.author.name}", description=f"**Here is the message:** {message}", color=green)
            await user.send(embed=embed)
            await ctx.message.add_reaction("✅")
            await ctx.channel.send(":white_check_mark: Message delivered sccessfully")
      except:
        await ctx.message.add_reaction("❌")
        await ctx.channel.send("❌ The user has DM closed. I can't deliver the message")
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, amount=5):
      if amount >= 101:
        await ctx.send("Uh, I only allow you to delete 100 messages a time")
      else:
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount, bulk=True)
        message0 = await ctx.send(f"{amount} messages have been deleted. This message will be deleted after 3 seconds.")
        await asyncio.sleep(3)
        await message0.delete()

    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    async def emojisteal(self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji], name=None):
        if not name:
          name = emoji.name
        await ctx.guild.create_custom_emoji(name=name, image=await emoji.url.read())
        await ctx.send(f"Successfully added the emoji {name}")

    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    async def emojiadd(self, ctx, url, name):
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, requests.exceptions.ConnectionError):
            return await ctx.send("The URL you have provided is invalid.")
        if response.status_code == 404:
            return await ctx.send("The URL you have provided leads to a 404.")
        try:
            await ctx.guild.create_custom_emoji(name=name, image=response.content)
        except discord.InvalidArgument:
            return await ctx.send("Invalid image type. Only PNG, JPEG and GIF are supported.")
        await ctx.send(f"Successfully added the emoji {name}")


    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    async def emojiremove(self, ctx, name):
        emotes = [x for x in ctx.guild.emojis if x.name == name]
        emote_length = len(emotes)
        if not emotes:
            return await ctx.send("No emotes with that name could be found on this server.")
        for emote in emotes:
            await emote.delete()
        if emote_length == 1:
            await ctx.send("Successfully removed the {} emoji!".format(name))
        else:
            await ctx.send("Successfully removed {} emoji with the name {}.".format(emote_length, name))

    @commands.command()
    async def emojiurl(self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji]):
        await ctx.send(f"<{emoji.url}>")
        
    @commands.command()
    async def addrole(self, ctx, member: discord.Member):
      guild = ctx.guild
      No = discord.utils.get(guild.roles, name="Articuno")
      await member.add_roles(No)
      await ctx.message.add_reaction("✅")



def setup(bot):
    bot.add_cog(Server(bot))
    
