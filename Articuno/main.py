import discord
from discord.ext import commands
import asyncio
import random
import time
import json
import multiprocessing
import os
from discord.ext.commands import Bot, Greedy
from discord import User

bot = commands.Bot(command_prefix="$")
blue = 0x236adf
red = 0xff0000
orange = 0xff8b00
purple = 0xac10eb
black = 0xffffff
white = 0x000000
green = 0x3bcc12


@bot.event
async def on_ready():
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='as a BOT'))
@bot.command(description="Changes bots activity")
@commands.has_permissions(administrator=True)
async def activity(ctx, *, activity):
    await bot.change_presence(activity=discord.Game(name=activity))
    await ctx.send(f"Bot's activity changed to {activity}")


@bot.command()
async def hi(ctx):
    await ctx.send(f"Hello there, {ctx.author.name}")

@bot.command()
async def credits(ctx):
    embed = discord.Embed(title=f'Credits', description=f"Articuno was originally created by <@738937306224001157>", color=blue)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
     embed = discord.Embed(description=f":ping_pong:Pong! Took about {round(bot.latency * 1000)}ms", color=orange)
     await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, avamember : discord.Member=None, *, member = discord.Member):
    embed = discord.Embed(color=white)
    avatar = avamember.avatar_url
    embed.set_image(url=avatar)
    await ctx.send(embed=embed)
    
@bot.command()
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

	
@bot.command()
async def about(ctx):
    embed = discord.Embed(title=f"About Articuno", color=blue)
    python = "3.9.1"
    discordpy = "1.5.1"
    latency=f"{round(bot.latency * 1000)}ms"
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/782628076503957524/10ca66e0b32229c171a26d35e53f342b.webp?size=1024')
    embed.add_field(name="Python <:python:800396434905366528>", value=python, inline=False)
    embed.add_field(name="Discord.py <:discord:762341762017787935>", value=discordpy, inline=True)
    embed.add_field(name="Latency :ping_pong:", value=latency, inline=False)
    await ctx.send(embed=embed)
	
@bot.command()
async def dm(ctx, *, message):
    await ctx.author.send(message)

@bot.command()
@commands.has_permissions(administrator = True)
async def notice(ctx, users: Greedy[User], *, message):
    for user in users:
        await user.send(message)

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    message = discord.Embed(title=f"Banned {member.name} by {ctx.author.name}", description=f"Reason: {reason}", color=blue)
    try:
        await member.send(embed=message)
    except:
        await ctx.channel.send("I couldn't DM the User. I'll still ban")

    await ctx.channel.send(embed=message)
    await member.ban(reason = reason)

@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    message = discord.Embed(title=f"{member.name} has been kicked by {ctx.author.name}", description=f"Reason: {reason}", color=blue)
    try:
        await member.send(embed=message)
    except:
        await ctx.channel.send("I couldn't DM the User. I'll still kick")
    await ctx.channel.send(embed=message)
    await member.kick(reason = reason)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        error1 = discord.Embed(title=f"{ctx.author.name}, you made an error <:angery:795706290135498762>", description=f"Error: Command not found", color=red)
        await ctx.send(embed=error1)
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        error2 = discord.Embed(title=f"{ctx.author.name}, you made an error <:angery:795706290135498762>", description=f"Error: Missing Required Argument", color=red)
        await ctx.send(embed=error2)

bot.run('NzgyNjI4MDc2NTAzOTU3NTI0.X8O9MQ.x51JafJtk71sirIWH40yZhAgiZ0')