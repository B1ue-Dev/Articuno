import discord
from discord.ext import commands
import random
import aiohttp
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

class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(description="List of available comamnds")
    async def help(self, ctx):
      embed = discord.Embed(title="Available commands for Articuno", description=f"If you encounter any error, DM to <@738937306224001157>JimmyBlue#4773", color=blue)
      embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/782628076503957524/10ca66e0b32229c171a26d35e53f342b.png?size=256')
      embed.add_field(name="**Basic**", value="``about`` ``avatar`` ``credits`` ``hello`` ``hi`` ``henlo`` ``invite`` ``ping`` ``status`` ``stats``", inline=False)
      embed.add_field(name="**Fun**", value="``ball`` ``coffee`` ``meme`` ``duck`` ``cat`` ``dog`` ``pokemon`` ``pikachu`` ``bread`` ``ship`` ``roll`` ``say``", inline=False)
      embed.add_field(name="**Moderation**", value="``kick`` ``ban`` ``unban`` ``mute`` ``unmute`` ``snipe``", inline=False)
      embed.add_field(name="**Server**", value="``server`` ``info`` ``dm`` ``message`` ``emoji`` ``emojicopy`` ``emojiadd`` ``emojiremove`` ``emojiurl``")
      await ctx.message.add_reaction("✅")
      await ctx.send(embed=embed)

    @commands.command(description="Hello")
    async def hi(self, ctx):
        await ctx.send(f"Hello there, {ctx.author.name}")
    @commands.command(description="Hello")
    async def hello(self, ctx):
        await ctx.send(f"Hello there, {ctx.author.name}")
    @commands.command(description="Hello")
    async def henlo(self, ctx):
        await ctx.send(f"Henlo <:Henlo:859316764159770645>")

    @commands.command(description="The owner of Articuno")
    async def credits(self, ctx):
        embed = discord.Embed(title=f'Credits', description=f"Articuno was originally created by <@738937306224001157>", color=blue)
        await ctx.send(embed=embed)

    @commands.command(description="Ping the commands")
    async def ping(self, ctx):
        embed = discord.Embed(description=f":ping_pong:Pong! Took about {round(self.bot.latency * 1000)}ms", color=orange)
        await ctx.send(embed=embed)


    @commands.command(description="Avatar of a spetified user")
    async def avatar(self, ctx, *,  avamember : discord.Member=None):
        if not avamember:
          avamember = ctx.author
        avatar = avamember.avatar_url
        member = avamember.name
        embed = discord.Embed(description=f"**Avatar**", color=random.randint(0, 0xFFFFFF))
        embed.set_author(name=member, icon_url=avatar)
        embed.set_image(url=avatar)
        await ctx.send(embed=embed)

        
    @commands.command(description="About Articuno")
    async def about(self, ctx):
        embed = discord.Embed(title=f"About Articuno", color=blue)
        python = "3.8.10"
        discordpy = "1.7.6"
        latency=f"{round(self.bot.latency * 1000)}ms"
        embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/782628076503957524/10ca66e0b32229c171a26d35e53f342b.png?size=256')
        embed.add_field(name="Python <:Python:860913381850480650>", value=python, inline=False)
        embed.add_field(name="Discord.py <:Discord:860913504361644032>", value=discordpy, inline=True)
        embed.add_field(name="Latency :ping_pong:", value=latency, inline=False)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def status(self, ctx):
      await ctx.channel.send(f"<a:WindowsHello:854724546061402146> {ctx.author.mention}, everything is working perfectly fine")
    
    @commands.command()
    async def invite(self, ctx):
      embed = discord.Embed(title=f"Invite me to your server", description=f"https://discord.com/api/oauth2/authorize?client_id=851064798333501480&permissions=8&scope=bot", color=blue)
      await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
      async with aiohttp.ClientSession():
        response = requests.get('https://api.statcord.com/v3/851064798333501480')
        data = response.json()
        pdata = data['data']
        for d in pdata:
            usercount = (d['users'])
            cpu = (d['cpuload'])
            memload = (d['memload'])
            memactive = (d['memactive'])
        embed=discord.Embed(title="Articuno Stats",description="My official stats!",color=blue)
        embed.add_field(name="Server Count",value=len(self.bot.guilds))
        embed.add_field(name="User Count",value=f"{usercount}")
        embed.add_field(name="CPU Load",value=f"{cpu}%")
        embed.add_field(name="MEM Load",value=f"{memload}MB")
        embed.add_field(name="MEM Active",value=f"{memactive}KB")
        embed.set_footer(icon_url='https://cdn.statcord.com/logo.png',text=f"Powered by Statcord")
        await ctx.send(embed=embed)
      


    
def setup(bot):
  bot.add_cog(Basic(bot))
