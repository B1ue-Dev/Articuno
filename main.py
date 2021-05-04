import discord
from discord.ext.commands import bot
from discord.ext import commands
import asyncio
import random
import time
import json
import multiprocessing

client = commands.Bot(command_prefix="$")
blue = 0x236adf
red = 0xff0000
orange = 0xff8b00
purple = 0xac10eb
black = 0xffffff
white = 0x000000
green = 0x3bcc12



@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='as a BOT'))
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))


@client.command()
async def hello(ctx):
    await ctx.send('Hello!')

@client.command()
async def credits(ctx):
    embed = discord.Embed(title=f'Credits', description=f"Articuno was originally created by <@738937306224001157>", color=blue)
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
     embed = discord.Embed(description=f":ping_pong:Pong! Took about {round(client.latency * 1000)}ms", color=orange)
     await ctx.send(embed=embed)

@client.command()
async def avatar(ctx, avamember : discord.Member=None, *, member = discord.Member):
    embed = discord.Embed(color=white)
    avatar = avamember.avatar_url
    embed.set_image(url=avatar)
    await ctx.send(embed=embed)
    
@client.command()
async def server(ctx):
    name = str(ctx.guild.name)
    id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=blue
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)

	
@client.command()
async def about(ctx):
    embed = discord.Embed(title=f"About Articuno", color=blue)
    python = "3.9.1"
    discordpy = "1.5.1"
    latency=f"{round(client.latency * 1000)}ms"
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/782628076503957524/10ca66e0b32229c171a26d35e53f342b.webp?size=1024')
    embed.add_field(name="Python <:python:800396434905366528>", value=python, inline=False)
    embed.add_field(name="Discord.py <:discord:762341762017787935>", value=discordpy, inline=True)
    embed.add_field(name="Latency :ping_pong:", value=latency, inline=False)
    await ctx.send(embed=embed)
	
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    message = discord.Embed(title=f"Banned {member.name} by {ctx.author.name}", description=f"Reason: {reason}", color=blue)
    message.set_image(url='https://tenor.com/view/blob-banned-ban-hammer-blob-ban-emoji-gif-16021044')
    await ctx.channel.send(embed=message)
    try:
        await member.send(embed=message)
    except:
        await ctx.channel.send("I couldn't DM the User. I'll still ban")

    await member.ban(reason = reason)

@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    message = discord.Embed(title=f"{member.name} has been kicked by {ctx.author.name}", description=f"Reason: {reason}", color=blue)
    try:
        await member.send(embed=message)
    except:
        await ctx.channel.send("I couldn't DM the User. I'll still kick")
    await ctx.channel.send(embed=message)
    await member.kick(reason = reason)

client.run('Sheesh')
