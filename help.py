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

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.group(description="List of available comamnds", invoke_without_command=True)
    async def help(self, ctx):
      embed = discord.Embed(title="Available commands for Articuno", description=f"If you encounter any error, DM to <@738937306224001157>JimmyBlue#4773\nTo see how to use a command, type ``$help [command]``",color=blue)
      # BASIC
      embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/782628076503957524/10ca66e0b32229c171a26d35e53f342b.png?size=256')
      embed.add_field(name="**Basic**", value="``avatar`` ``credits`` ``invite`` ``ping`` ``stats``", inline=False)
      # MODERATION
      embed.add_field(name="**Moderation**", value="``kick`` ``ban`` ``unban`` ``mute`` ``unmute`` ``snipe`` ``lock`` ``unlock``", inline=False)
      # FUN
      embed.add_field(name="**Fun**", value="``ball`` ``coffee`` ``meme`` ``duck`` ``cat`` ``dog`` ``pokemon`` ``pikachu`` ``bread`` ``ship`` ``roll`` ``say`` ``joke`` ``hornycard`` ``simpcard`` ``ai``", inline=False)
      # SERVER
      embed.add_field(name="**Server**", value="``server`` ``info`` ``dm`` ``message`` ``emojisteal``  ``emojiadd`` ``emojiremove`` ``emojiurl``")
      await ctx.message.add_reaction("✅")
      await ctx.send(embed=embed)

    # BASIC Commands help menu:
    @help.command()
    async def avatar(self, ctx):
      embed = discord.Embed(title="Avatar", description="Show the avatar of a specific user",color=blue)
      embed.add_field(name="**How to use:**", value="``$avatar [member]``")
      await ctx.send(embed=embed)
    @help.command()
    async def credits(self, ctx):
      embed = discord.Embed(title="Credits", description="Developers in this project",color=blue)
      embed.add_field(name="**How to use:**", value="``$credits``")
      await ctx.send(embed=embed)
    @help.command()
    async def invite(self, ctx):
      embed = discord.Embed(title="Invite", description="Invite me to your server",color=blue)
      embed.add_field(name="**:)**", value=f"[Invite link](https://discord.com/api/oauth2/authorize?client_id=851064798333501480&permissions=8&scope=bot)")
      await ctx.send(embed=embed)
    @help.command()
    async def ping(self, ctx):
      embed = discord.Embed(title="Ping", description="Ping the BOT",color=blue)
      embed.add_field(name="**How to use:**", value=f"``$ping``")
      await ctx.send(embed=embed)
    @help.command()
    async def stats(self, ctx):
      embed = discord.Embed(title="Stats", description="See the stats of Articuno",color=blue)
      embed.add_field(name="**How to use:**", value=f"``$stats``")
      await ctx.send(embed=embed)


    # MODERATION Commands help menu:
    @help.command()
    async def kick(self, ctx):
      embed = discord.Embed(title="Kick", description="Kick a specific user",color=blue)
      embed.add_field(name="**How to use:**", value="``$kick <member> [reason]``")
      await ctx.send(embed=embed)
    @help.command()
    async def ban(self, ctx):
      embed = discord.Embed(title="Ban", description="Ban a specific user",color=blue)
      embed.add_field(name="**How to use:**", value="``$ban <member> [reason]``")
      await ctx.send(embed=embed)
    @help.command()
    async def unban(self, ctx):
      embed = discord.Embed(title="Unban", description="Unban a specific user",color=blue)
      embed.add_field(name="**How to use:**", value="``$unban <member.id>``")
      await ctx.send(embed=embed)
    @help.command()
    async def mute(self, ctx):
      embed = discord.Embed(title="Mute", description="Mute a specific user",color=blue)
      embed.add_field(name="**How to use:**", value="``$mute <member> [reason]``")
      await ctx.send(embed=embed)
    @help.command()
    async def unmute(self, ctx):
      embed = discord.Embed(title="Unmute", description="Unmute a specific user",color=blue)
      embed.add_field(name="**How to use:**", value="``$unmute <member>``")
      await ctx.send(embed=embed)
    @help.command()
    async def snipe(self, ctx):
      embed = discord.Embed(title="Snipe", description="Snipe the most recent deleted message",color=blue)
      embed.add_field(name="**How to use:**", value="``$snipe``")
      await ctx.send(embed=embed)
    @help.command()
    async def lock(self, ctx):
      embed = discord.Embed(title="Lock", description="Lock down a specific channel",color=blue)
      embed.add_field(name="**How to use:**", value="``$lock [channel]``")
      await ctx.send(embed=embed)
    @help.command()
    async def unlock(self, ctx):
      embed = discord.Embed(title="Unlock", description="Unlock a specific channel",color=blue)
      embed.add_field(name="**How to use:**", value="``$unlock [channel]``")
      await ctx.send(embed=embed)    

    
    # FUN Commands help menu:
    @help.command()
    async def ball(self, ctx):
      embed = discord.Embed(title="Ball", description="Random answer",color=blue)
      embed.add_field(name="**How to use:**", value="``$ball <argument>``")
      await ctx.send(embed=embed)      
    @help.command()
    async def coffee(self, ctx):
      embed = discord.Embed(title="Coffee", description="Send a random image of coffee",color=blue)
      embed.add_field(name="**How to use:**", value="``$coffee``")
      await ctx.send(embed=embed)
    @help.command()
    async def meme(self, ctx):
      embed = discord.Embed(title="Meme", description="Send a meme",color=blue)
      embed.add_field(name="**How to use:**", value="``$meme``")
      await ctx.send(embed=embed)
    @help.command()
    async def duck(self, ctx):
      embed = discord.Embed(title="Duck", description="Send a random image of duck",color=blue)
      embed.add_field(name="**How to use:**", value="``$duck``")
      await ctx.send(embed=embed)
    @help.command()
    async def cat(self, ctx):
      embed = discord.Embed(title="Cat", description="Send a random image of cat",color=blue)
      embed.add_field(name="**How to use:**", value="``$cat``")
      await ctx.send(embed=embed)
    @help.command()
    async def dog(self, ctx):
      embed = discord.Embed(title="Dog", description="Send a random image of dog",color=blue)
      embed.add_field(name="**How to use:**", value="``$dog``")
      await ctx.send(embed=embed)
    @help.command()
    async def pokemon(self, ctx):
      embed = discord.Embed(title="Pokemon", description="Information about a Pokemon",color=blue)
      embed.add_field(name="**How to use:**", value="``$pokemon <pokemon name>``")
      await ctx.send(embed=embed)
    @help.command()
    async def pikachu(self, ctx):
      embed = discord.Embed(title="Pikachu", description="Send a random gif of Pikachu",color=blue)
      embed.add_field(name="**How to use:**", value="``$pikachu``")
      await ctx.send(embed=embed)
    @help.command()
    async def bread(self, ctx):
      embed = discord.Embed(title="Bread", description="Send a random image of bread",color=blue)
      embed.add_field(name="**How to use:**", value="``$bread``")
      await ctx.send(embed=embed)
    @help.command()
    async def ship(self, ctx):
      embed = discord.Embed(title="Ship", description="Ship 2 users or anything",color=blue)
      embed.add_field(name="**How to use:**", value="``$ship [argument 1] [argument 2]``")
      await ctx.send(embed=embed)
    @help.command()
    async def roll(self, ctx):
      embed = discord.Embed(title="Roll", description="Roll a dice from 1 to 6",color=blue)
      embed.add_field(name="**How to use:**", value="``$roll``")
      await ctx.send(embed=embed)
    @help.command()
    async def say(self, ctx):
      embed = discord.Embed(title="Say", description="Let Articuno say something that the user want",color=blue)
      embed.add_field(name="**How to use:**", value="``$say <argument>``")
      await ctx.send(embed=embed)
    @help.command()
    async def joke(self, ctx):
      embed = discord.Embed(title="Joke", description="Send a random joke",color=blue)
      embed.add_field(name=f"**How to use**", value=f"``$joke``")
      await ctx.send(embed=embed)
    @help.command()
    async def hornycard(self, ctx):
      embed = discord.Embed(title="Hornycard", description="Make a hornycard based on the user's profile picture", color=blue)
      embed.add_field(name=f"**How to use**", value=f"``$hornycard [user]``")
      await ctx.send(embed=embed)
    @help.command()
    async def simpcard(self, ctx):
      embed = discord.Embed(title="Simpcard", description="Make a simpcard based on the user's profile picture", color=blue)
      embed.add_field(name=f"**How to use**", value=f"``$simpcard [user]``")
      await ctx.send(embed=embed)
    @help.command()
    async def ai(self, ctx):
      embed = discord.Embed(title="AI", description="Talk with an AI chatbot", color=blue)
      embed.add_field(name=f"**How to use**", value=f"``$ai <argument>``")
      await ctx.send(embed=embed)

    # SERVER Commands help menu:
    @help.command()
    async def server(self, ctx):
      embed = discord.Embed(title="Server", description="Information about server",color=blue)
      embed.add_field(name="**How to use:**", value="``$server``")
      await ctx.send(embed=embed)
    @help.command()
    async def info(self, ctx):
      embed = discord.Embed(title="Info", description="Information about a member",color=blue)
      embed.add_field(name="**How to use:**", value="``$info [member]``")
      await ctx.send(embed=embed)
    @help.command()
    async def dm(self, ctx):
      embed = discord.Embed(title="DM", description="Direct Message yourself",color=blue)
      embed.add_field(name="**How to use:**", value="``$dm <argument>``")
      await ctx.send(embed=embed)
    @help.command()
    async def message(self, ctx):
      embed = discord.Embed(title="Message", description="DM a member (Only administrators can use this command)",color=blue)
      embed.add_field(name="**How to use:**", value="``$message <member> <argument>``")
      await ctx.send(embed=embed)
    @help.command()
    async def emojisteal(self, ctx):
      embed = discord.Embed(title="Emojisteal", description="Add a custom enoji from another server to your own server",color=blue)
      embed.add_field(name="**How to use:**", value="``$emojisteal <emoji> [name]``")
      await ctx.send(embed=embed)
    @help.command()
    async def emojiadd(self, ctx):
      embed = discord.Embed(title="Emojiadd", description="Add an emoji from an image link to your own server",color=blue)
      embed.add_field(name="**How to use:**", value="``$emojiadd <link> <name>``")
      await ctx.send(embed=embed)
    @help.command()
    async def emojiremove(self, ctx):
      embed = discord.Embed(title="Emojiremove", description="Remove an emoji from the server",color=blue)
      embed.add_field(name="**How to use:**", value="``$emojiremove <name of the emoji>``")
      embed.add_field(name="**Example**", value="``$emojiremove bruh``, do not use ``$emojiremove :bruh:``")
      await ctx.send(embed=embed)
    @help.command()
    async def emojiurl(self, ctx):
      embed = discord.Embed(title="Emojiurl", description="Get the link of an emoji",color=blue)
      embed.add_field(name="**How to use:**", value="``$demojiurl <emoji>``")
      await ctx.send(embed=embed)

      #DONE! I need a sleep now. 


def setup(bot):
    bot.add_cog(Help(bot))
