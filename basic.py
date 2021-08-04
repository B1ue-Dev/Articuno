import discord
from discord.ext import commands
import random
import aiohttp
import requests
import asyncio



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

    @commands.command(description="Hello")
    async def hi(self, ctx):
        await ctx.send(f"Hello there, {ctx.author.name}")
    @commands.command(description="Hello")
    async def hello(self, ctx):
        await ctx.send(f"Hello there, {ctx.author.name}")
    @commands.command(description="Hello")
    async def henlo(self, ctx):
        await ctx.send(f"Henlo <:Henlo:859316764159770645>")

    @commands.command(description="Developers/Contributors to this project")
    async def credits(self, ctx):
        embed = discord.Embed(title=f'Credits', description=f"Developers and contributors in this project:", color=blue)
        embed.add_field(name="JimmyBlue#4773", value=f"**Leader** The owner and creator of this project and mostly handle with stuffs")
        embed.add_field(name="terabyte.#4258", value=f"**Developer** Debugger and helper for me in this project")
        embed.add_field(name="matteodev#1109", value=f"**Suggestor** Idea maker for this")
        embed.add_field(name="Manana#3313", value="**Tester** Insider for this project")
        embed.add_field(name="pokemon hangout", value=f"**Inspirational** If it wasn't because of this server, this project would be abandoned\n[Join this amazing server](https://discord.gg/TWtrRS7uVp)")
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
        
    @commands.command()
    async def status(self, ctx):
      await ctx.channel.send(f"<a:WindowsHello:854724546061402146> {ctx.author.mention}, everything is working perfectly fine.")
    
    @commands.command()
    async def invite(self, ctx):
      embed = discord.Embed(title=f"Invite me to your server :)", description=f"[Invite](https://discord.com/api/oauth2/authorize?client_id=851064798333501480&permissions=8&scope=bot)", color=blue)
      await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def stats(self, ctx):
      async with aiohttp.ClientSession():
        response = requests.get('https://api.statcord.com/v3/851064798333501480')
        data = response.json()
        pdata = data['data']
        for d in pdata:
            usercount = (d['users'])
            cpu = (d['cpuload'])
            memload = (d['memload'])
        python = "3.8.10"
        discordpy = "1.7.6"
        latency=f"{round(self.bot.latency * 1000)}ms"

        embed=discord.Embed(title="Articuno Stats",color=blue)
        embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/782628076503957524/10ca66e0b32229c171a26d35e53f342b.png?size=256')        
        embed.add_field(name="Server Count :family_mmbb:",value=len(self.bot.guilds))
        embed.add_field(name="User Count :bust_in_silhouette:",value=f"{usercount}")
        embed.add_field(name="CPU Load <:CPU:870908659897610250>",value=f"{cpu}%")
        embed.add_field(name="MEM Load <:RAM:870907903513612299>",value=f"{memload}MB")
        embed.add_field(name="Python <:Python:860913381850480650>", value=python)
        embed.add_field(name="Discord.py <:Discord:860913504361644032>", value=discordpy)
        embed.add_field(name="Latency :ping_pong:", value=latency)
        embed.add_field(name="Operating System <:Tux:859316661248720918>", value="Linux")
        embed.set_footer(icon_url='https://cdn.statcord.com/logo.png',text=f"Powered by Statcord")
        await ctx.send(embed=embed)
      

    @commands.command()
    @commands.is_owner()
    async def update(self, ctx):
      await ctx.message.delete()
      message = await ctx.send(f"<a:WindowsLoading:859101948397092924> Articuno is being updated to the latest version. Please be patient\nEstimate time left: unknown")
      await asyncio.sleep(30)
      await message.delete()
      embed = discord.Embed(title="An update to Articuno", description="``Changelog v2.2.5``",color=blue)
      embed.add_field(name="What's new in this update?",value="In this update, Articuno has 3 new fun commands. ``hornycard`` ``simpcard`` and ``ai``. We have worked hard (at least, compared to before) to make this. The AI command was a real pain, but luckily, we managed to solved the problem. Thank you for your trust in Articuno and have a great day, everyone. Love you all :love_you_gesture:")
      await ctx.send(embed=embed)









def setup(bot):
  bot.add_cog(Basic(bot))
