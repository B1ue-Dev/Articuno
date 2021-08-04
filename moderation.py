import discord
from discord.ext import commands
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

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="Ban a specified member")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason = None,):

        log_channel = discord.utils.get(ctx.guild.channels, name="📝║logs")

        channel_message = discord.Embed(title=f"{member.name} has been banned by {ctx.author.name}.", description=f"Reason: {reason}", color=red)

        user = discord.Embed(title=f"You have been banned by {ctx.author.name} in {ctx.guild.name}.", description=f"Reason: {reason}", color=red)

        log=discord.Embed(title="Banned successfully!", colour=red)
        log.set_thumbnail(url=member.avatar_url)
        log.add_field(name="**Moderator**", value=ctx.author.mention + str(ctx.author), inline=True)
        log.add_field(name="**Member**", value=member.mention + str(member), inline=False)
        log.add_field(name="**ID**", value=member.id, inline=False)
        log.add_field(name="**Reason**", value=f"{reason}", inline=False)
        if member == ctx.author:
          await ctx.send("You cannot ban yourself.")
        else:
          try:
              await log_channel.send(embed=log)
          except:
              await ctx.send("I could not find the logs channel.")
          try:
              await member.send(embed=user)
          except:
              await ctx.send("I could not DM the User. I will still ban.")
          await member.ban(reason = reason, delete_message_days=0)
          await ctx.message.add_reaction("✅")
          await ctx.send(embed=channel_message)
        


    @commands.command(name='unban')
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, id: int):
        user = await self.bot.fetch_user(id)
        await ctx.message.add_reaction("✅")
        await ctx.guild.unban(user)
        embed1 = discord.Embed(description=f"Member has been unbanned successfully", color=yellow)
        await ctx.send(embed=embed1)
        


    @commands.command(description="Kick a specified member")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member, *, reason = None):
        log_channel = discord.utils.get(ctx.guild.channels, name="📝║logs")
        
        channel_message = discord.Embed(title=f"{member.name} has been kicked by {ctx.author.name}.", description=f"Reason: {reason}", color=red)

        user = discord.Embed(title=f"You have been kicked by {ctx.author.name} in {ctx.guild.name}.", description=f"Reason: {reason}", color=red)

        log=discord.Embed(title="Kicked successfully!", colour=red)
        log.set_thumbnail(url=member.avatar_url)
        log.add_field(name="**Moderator**", value=ctx.author.mention + str(ctx.author), inline=True)
        log.add_field(name="**Member**", value=member.mention + str(member), inline=False)
        log.add_field(name="**ID**", value=member.id, inline=False)
        log.add_field(name="**Reason**", value=f"{reason}", inline=False)
        if member == ctx.author:
          await ctx.send("You cannot kick yourself.")
        else:
          try:
              await log_channel.send(embed=log)
          except:
              await ctx.send("I could not find the logs channel.")
          try:
              await member.send(embed=user)
          except:
              await ctx.send("I could not DM the User. I will still kick.")
          await member.kick(reason = reason)    
          await ctx.message.add_reaction("✅")
          await ctx.send(embed=channel_message)
        
        


    @commands.command(description="Mute a specified user.")
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        log_channel = discord.utils.get(ctx.guild.channels, name="📝║logs")
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="🔇║Muted")

        channel_message = discord.Embed(title=f"{member.name} has been muted.", description=f"Reason: {reason}", colour=red)

        user = discord.Embed(title=f"You have been muted by {ctx.author.name} in {ctx.guild.name}.", description=f"Reason: {reason}", color=red)

        log=discord.Embed(title="Muted successfully!", colour=red)
        log.set_thumbnail(url=member.avatar_url)
        log.add_field(name="**Moderator**", value=ctx.author.mention + str(ctx.author), inline=True)
        log.add_field(name="**Member**", value=member.mention + str(member), inline=False)
        log.add_field(name="**ID**", value=member.id, inline=False)
        log.add_field(name="**Reason**", value=f"{reason}", inline=False)

        try:
            await log_channel.send(embed=log)
        except:
            await ctx.send("I could not find the logs channel")
        try:
            await member.send(embed=user)
        except:
            await ctx.send("I could not DM the User. I will still mute")
        try:
            await member.add_roles(mutedRole, reason=reason)
            await ctx.message.add_reaction("✅")
            await ctx.send(embed=channel_message)
        except: 
            await ctx.send("There is no mute role, so I could not mute the user")
            await ctx.message.add_reaction("❌") 


        



    @commands.command(description="Unmute a specified user.")
    @commands.has_permissions(manage_messages = True)
    async def unmute(self, ctx, member: discord.Member):
        log_channel = discord.utils.get(ctx.guild.channels, name="📝║logs")

        log=discord.Embed(title="Unmuted successfully!", colour=green)
        log.set_thumbnail(url=member.avatar_url)
        log.add_field(name="**Moderator**", value=ctx.author.mention, inline=True)
        log.add_field(name="**Member**", value=member.mention + str(member), inline=False)
        log.add_field(name="**ID**", value=member.id, inline=False)

        mutedRole = discord.utils.get(ctx.guild.roles, name="🔇║Muted")

        try:
            # Ignore this. Thank you!
            await log_channel.send(embed=log)
        except:
            await ctx.send("I could not find the logs channel")
        # Still buggy like :woozy_face:
        try:
            await member.remove_roles(mutedRole)
            await ctx.message.add_reaction("✅")
            await ctx.send(f"{member.name} is unmuted.")
        except:
            await ctx.send("The user is not muted")
            await ctx.message.add_reaction("❌") 

    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        global snipe_message_content
        global snipe_message_author
        global snipe_message_id
        global snipe_message_author_id

        snipe_message_content = message.content
        snipe_message_author = message.author.name
        snipe_message_id = message.id
        snipe_message_author_id = message.author.id
        await asyncio.sleep(60)

        if message.id == snipe_message_id:
            snipe_message_author = None
            snipe_message_content = None
            snipe_message_id = None
            snipe_message_author_id = None

    @commands.command()
    async def snipe(self, message):
        # Experimental, may have a lot of bugs
        if snipe_message_content==None:
            await message.channel.send("Theres nothing to snipe.")
        else:
            embed = discord.Embed(description=f"<@!{snipe_message_author_id}> said: {snipe_message_content}")
            embed.set_footer(text=f"Asked by {message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
            embed.set_author(name= f"{snipe_message_author}")
            await message.channel.send(embed=embed)
            return

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel : discord.TextChannel=None):
      channel = channel or ctx.channel
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.send_messages = False
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      await ctx.message.add_reaction('🔒')
      await ctx.send(f'``{channel}`` is locked.')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel : discord.TextChannel=None):
      channel = channel or ctx.channel
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.send_messages = True
      message = await ctx.send(f'``{channel}`` is being unlocked.')
      await asyncio.sleep(2)
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      await ctx.message.add_reaction('🔓')
      await message.edit(content=f"``{channel}`` is unlocked.")

        

def setup(bot):
  bot.add_cog(Moderation(bot))
