"""
This module is for Pokedex command.

(C) 2022 - Jimmy-Blue
"""

import json
import interactions


class Pokemon(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="pokedex",
        description="Show the information about a Pokemon",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="pokemon_name",
                description="Pokemon name",
                required=True,
                autocomplete=True
            )
        ]
    )
    async def _pokemon(self, ctx: interactions.CommandContext, pokemon_name: str):
        name_lower = pokemon_name.lower()

        data = json.loads(open("./db/pokemon.json", "r", encoding="utf8").read())
        if name_lower in data:
            name = data[name_lower]['name']
            id = data[name_lower]['num']	
            types = str(data[name_lower]['types'])
            types = types.replace("'","")
            types = types.replace("[","")
            types = types.replace("]","")
            hp = data[name_lower]['baseStats']['hp']
            atk = data[name_lower]['baseStats']['atk']
            defe = data[name_lower]['baseStats']['def']
            spa = data[name_lower]['baseStats']['spa']
            spd = data[name_lower]['baseStats']['spd']
            spe = data[name_lower]['baseStats']['spe']
            stats = "**HP:** {}\n**Attack:** {}\n**Defense:** {}\n**Special Attack:** {}\n**Special Defense:** {}\n**Speed:** {}".format(hp, atk, defe, spa, spd, spe)
            egg_group = str(data[name_lower]['eggGroups'])
            egg_group = egg_group.replace("'","")
            egg_group = egg_group.replace("[","")
            egg_group = egg_group.replace("]","")
            height = data[name_lower]['heightm']
            weight = data[name_lower]['weightkg']
            if int(id) < int(10):
                id = "00" + str(id)
                id = int(id)
            elif int(id) < int(100):
                id = "0" + str(id)
                id = int(id)
            else:
                id = int(id)
            sprites_url_still = f"https://www.serebii.net/art/th/{id}.png"

            thumbnail = interactions.EmbedImageStruct(url=sprites_url_still)
            fields = [
                interactions.EmbedField(name="Information", value=f"**Entry:** {id}\n**Type(s):** {types}\n**Egg Groups:** {egg_group}\n**Height:** {height}\n**Weight:** {weight}", inline=True),
                interactions.EmbedField(name="Stats", value=stats, inline=True)
            ]
            embed = interactions.Embed(
                title=f"{name}",
                thumbnail=thumbnail,
                fields=fields,
            )
            await ctx.send(embeds=embed)


    @interactions.extension_autocomplete(
        command="pokedex",
        name="pokemon_name"
    )
    async def auto_complete(self, ctx:interactions.CommandContext, pokemon_name: str = ""):
        if pokemon_name != "":
            letters: list = pokemon_name
        else:
            letters = []
        data = json.loads(open("./db/pokemon.json", "r", encoding="utf8").read())
        if len(pokemon_name) == 0:
            await ctx.populate(
                [
                    interactions.Choice(
                        name=name[0].capitalize(), value=name[0].capitalize()) for name in (
                            list(data.items())[0:9] if len(data) > 10 else list(data.items()
                        )
                    )
                ]
            )
        else:
            choices: list = []
            for pkmn_name in data:
                focus: str = "".join(letters)
                if focus.lower() in pkmn_name and len(choices) < 20:
                    choices.append(interactions.Choice(name=pkmn_name.capitalize(), value=pkmn_name.capitalize()))
            await ctx.populate(choices)


def setup(client):
    Pokemon(client)
