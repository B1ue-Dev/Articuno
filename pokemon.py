import discord
from discord.ext import commands
import requests
import random
import aiohttp


class Pokemon(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @commands.command()
    async def pokemon(self,ctx,*,pokemon):
      async with aiohttp.ClientSession() as session:
        response = await session.get(f'https://some-random-api.ml/pokedex?pokemon={pokemon}')
        if str(response.status) == "404":
            await ctx.send("I couldn't find that pokemon. Please try again.")
        else:
                        rj = await response.json()
                        name = (rj['name']).capitalize()
                        pid = (rj['id'])
                        ptype = (rj['type'])
                        desc = (rj['description'])
                        species = (rj['species'])
                        stats = (rj['stats'])
                        evolfam = (rj['family'])
                        evs = (evolfam['evolutionLine'])
                        evs=str(evs)
                        evs=evs.replace("'","")
                        evs=evs.replace("]","")
                        evs=evs.replace("[","")
                        hp = (stats['hp'])
                        attack = (stats['attack'])
                        defense = (stats['defense'])
                        speed = (stats['speed'])
                        spattack = (stats['sp_atk'])
                        spdef = (stats['sp_def'])
                        abilities = (rj['abilities'])
                        abilities = str(abilities)
                        abilities=abilities.replace("'","")
                        abilities=abilities.replace("[","")
                        abilities=abilities.replace("]","")
                        weight = (rj['weight'])
                        height = (rj['height'])
                        weight = weight.replace(u'\xa0', u' ')
                        height = height.replace(u'\xa0', u' ')
                        species = str(species)
                        species=species.replace("'","")
                        species=species.replace("[","")
                        species=species.replace("]","")
                        species=species.replace(",","")
                        ptype = str(ptype)
                        ptype=ptype.replace("'","")
                        ptype=ptype.replace("[","")
                        ptype=ptype.replace("]","")
                        imgs=(rj['sprites'])
                        if int(rj['generation']) < 6:
                            img=(imgs['animated'])
                        else:
                            img=(imgs['normal'])
                        url = (imgs['normal'])
                        try:
                            idx = await session.get(url)
                            idx = await idx.read()
                            #await url.save(f'{pokemon}av.png',seek_begin = True)
                            embed=discord.Embed(title=name,description=desc,color=random.randint(0, 0xFFFFFF))
                        except:
                            embed=discord.Embed(title=name,description=desc)
                        embed.set_thumbnail(url=img)
                        embed.add_field(name="Information",value=f"Pokedex Entry: {pid}\nFirst introduced in generation {(rj['generation'])}\nType(s): {ptype}\nAbilities: {abilities}",inline=True)
                        embed.add_field(name="Base Stats",value=f"HP: {hp}\nDefense: {defense}\nSpeed: {speed}\nAttack: {attack}\nSpecial Attack: {spattack}\nSpecial Defense: {spdef}",inline=True)
                        if len(evs) != 0:
                            embed.add_field(name="Evolution Line",value=evs,inline=True)
                        await ctx.channel.trigger_typing()
                        await ctx.send(embed=embed)

    @commands.command()
    async def pikachu(self, ctx):
      response = requests.get('https://some-random-api.ml/img/pikachu')
      data = response.json()
      embed = discord.Embed(
        title = 'Pikachu <:PikaFacePalm:865060210991955968>',
        description = 'Here is a gif of Pikachu',
        color = 0xfff900
      )
      embed.set_image(url=data['link'])
      embed.set_footer(text="")
      await ctx.channel.trigger_typing()
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Pokemon(bot))
