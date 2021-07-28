import discord
from discord.ext import commands
import requests
import random
import asyncio


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def duck(self, ctx):
      response = requests.get('https://random-d.uk/api/v1/random')
      data = response.json()
      embed = discord.Embed(
          title = 'Duck 🦆',
          description = 'This is a duck',
          color=random.randint(0, 0xFFFFFF)
          )
      embed.set_image(url=data['url'])            
      embed.set_footer(text="")
      await ctx.channel.trigger_typing()
      await ctx.send(embed=embed)

    @commands.command()
    async def ball(self, ctx, *, question):
      ballresponse = [
  "Yes", "No", "Take a wild guess...", "Very doubtful",
  "Sure", "Without a doubt", "Most likely", "Might be possible",
  "You'll be judged", "no... (╯°□°）╯︵ ┻━┻", "no... baka",
  "Please, Please no ;-;", "Who know?", "I don't care", "This tbh", "You too", 
  "Bruh", "(☞ﾟヮﾟ)☞", "ㄟ( ▔, ▔ )ㄏ", "¯\_(ツ)_/¯", "LOL", "lmao", "f*ck you"
]
      answer = random.choice(ballresponse)
      await ctx.channel.trigger_typing()
      await ctx.reply(f"🎱**Answer:** {answer}")

    @commands.command()
    async def coffee(self, ctx):
      response = requests.get('https://coffee.alexflipnote.dev/random.json')
      data = response.json()
      embed = discord.Embed(
          title = 'Coffee ☕',
          description = 'A random image of coffee',
          color=random.randint(0, 0xFFFFFF)
          )
      embed.set_image(url=data['file'])            
      embed.set_footer(text="")
      await ctx.channel.trigger_typing()
      await ctx.send(embed=embed)

    @commands.command()
    async def meme(self, ctx):
      response1 = requests.get('https://some-random-api.ml/meme')
      data1 = response1.json()
      embed = discord.Embed(
          title = 'Meme 🤣',
          description = 'Here is a random meme I found',
          color = random.randint(0, 0xFFFFFF)
      )
      embed.set_image(url=data1['image'])
      embed.set_footer(text="")
      await ctx.channel.trigger_typing()
      await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
      response1 = requests.get('https://aws.random.cat/meow')
      response2 = requests.get('https://some-random-api.ml/facts/cat')
      data1 = response1.json()
      data2 = response2.json()
      embed = discord.Embed(
          title = 'Cat 🐈',
          description = 'This is a cat',
          color=random.randint(0, 0xFFFFFF)
          )
      embed.set_image(url=data1['file'])            
      embed.set_footer(text=data2['fact'])
      await ctx.channel.trigger_typing()
      await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx):
      response1 = requests.get('https://some-random-api.ml/img/dog')
      response2 = requests.get('https://some-random-api.ml/facts/dog')
      data1 = response1.json()
      data2 = response2.json()
      embed = discord.Embed(
          title = 'Dog 🐕',
          description = 'This is a dog',
          color=random.randint(0, 0xFFFFFF)
      )
      embed.set_image(url=data1['link'])
      embed.set_footer(text=data2['fact'])
      await ctx.channel.trigger_typing()
      await ctx.send(embed=embed)

    @commands.command()
    async def chat(self, ctx):
      await ctx.channel.trigger_typing()
      await ctx.send('Ur mom')

    @commands.command()
    async def bread(self, ctx):
      bread_image = [
        "https://miro.medium.com/max/7710/0*aj2NrmkQ69jMxpY0",
        "https://api.time.com/wp-content/uploads/2015/07/bread.jpeg?w=824&quality=70",
        "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/homemade-bread-horizontal-1547759080.jpg?crop=0.671xw:1.00xh;0.0801xw,0&resize=640:*",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5z13gFPAYP-kMG9Ysp0EC7xqh65a7JsCd2g&usqp=CAU"
        "https://media.istockphoto.com/photos/heap-of-bread-picture-id995038782?k=6&m=995038782&s=612x612&w=0&h=ukIfA0cMtdUrwp0sIYzW1rpKNon6iI-fPW8rkxmMNnk="
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Korb_mit_Br%C3%B6tchen.JPG/1200px-Korb_mit_Br%C3%B6tchen.JPG"
        "https://static01.nyt.com/images/2014/04/23/dining/23WHITE2/23WHITE2-articleLarge.jpg"
        "https://www.superhealthykids.com/wp-content/uploads/2019/11/Rosemary-Bread-2.jpg"
        "https://static01.nyt.com/images/2014/04/23/dining/23WHITE2/23WHITE2-articleLarge.jpg"
        "https://i.pinimg.com/originals/88/82/bc/8882bcf327896ab79fb97e85ae63a002.gif"
      ]
      bread = random.choice(bread_image)
      await ctx.channel.trigger_typing()
      await ctx.reply(f"{bread}")

    @commands.command()
    async def ship(self, ctx, name1=None, name2=None):
        shipnumber = int(random.randint(0, 100))
      
        if not name1:
          name1 = ctx.author.name
          name2 = random.choice(ctx.guild.members)
          name2 == name2.name
        if not name2:
          name2 = ctx.author.name
          name1 = name1

        if 0 <= shipnumber <= 30:
          comment = "Really low! {}".format(random.choice(["Friendzone ;(", 
                                                            'Just "friends"', 
                                                            "There's barely any love ;(",
                                                            "I sense a small bit of love!",
                                                            "Still in that friendzone ;(",
                                                            "No, just no!",
                                                            "But there's a small sense of romance from one person!"]))
        elif 31 <= shipnumber <= 70:
          comment = "Moderate! {}".format(random.choice(["Fair enough!",
                                                          "A small bit of love is in the air...",
                                                          "I feel like there's some romance progressing!",
                                                          "I'm starting to feel some love!",
                                                          "At least this is acceptable",
                                                          "...",
                                                          "I sense a bit of potential!",
                                                          "But it's very one-sided OwO"]))
        elif 71 <= shipnumber <= 90:
          comment = "Almost perfect! {}".format(random.choice(["I definitely can see that love is in the air",
                                                              "I feel the love! There's a sign of a match!",
                                                              "A few things can be imporved to make this a match made in heaven!",
                                                              "I can definitely feel the love",
                                                              "This has a big potential",
                                                              "I can see the love is there! Somewhere..."]))
        elif 90 < shipnumber <= 100:
          comment = "True love! {}".format(random.choice(["It's a match!", 
                                                           "There's a match made in heaven!", 
                                                           "It's definitely a match!", 
                                                           "Love is truely in the air!", 
                                                           "Love is most definitely in the air!"]))
        

        if shipnumber <= 40:
            shipColor = 0xE80303
        elif 41 < shipnumber < 80:
            shipColor = 0xff6600
        else:
            shipColor = 0x3be801

        emb = (discord.Embed(color=shipColor, \
                             title="Love test for:", \
                             description="**{0}** and **{1}** {2}".format(name1, name2, random.choice([
                                                                                                        ":sparkling_heart:", 
                                                                                                        ":heart_decoration:", 
                                                                                                        ":heart_exclamation:", 
                                                                                                        ":heartbeat:"]))))
        emb.add_field(name="Results:", value=f"{shipnumber}%  {comment}", inline=True)
        emb.set_author(name="Shipping", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)

    @commands.command()
    async def roll(self, message):
      dice = ["1","2","3","4","5","6"]
      number = random.choice(dice)
      await message.channel.trigger_typing()
      message0 = await message.reply("I am rolling the dice now")
      await asyncio.sleep(3)
      await message0.edit(content=f"The number is {number}")

    @commands.command()
    async def say(self, message, *, content):
      fp  = open('banned.txt')
      bad_list = [word.strip() for line in fp.readlines() for word in line.split(',') if word.strip()]
      content=content.lower()
      if any(word in content for word in bad_list):
          await message.reply("Don't you dare!")
      else:
          await message.channel.trigger_typing()
          await message.reply(f"```{content}```")    


def setup(bot):
    bot.add_cog(Fun(bot))
