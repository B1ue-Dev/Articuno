"""
This module is for Pokemon commands.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import io
import json
import interactions
from utils.utils import get_response


class Pokemon(interactions.Extension):
    """Extension for /pokedex command."""

    def __init__(self, client: interactions.Client) -> None:
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
                autocomplete=True,
            ),
        ],
    )
    async def _pokedex(
        self, ctx: interactions.CommandContext, pokemon_name: str
    ):
        name_lower = pokemon_name.lower()
        db = json.loads(open("./db/pokemon.json", "r", encoding="utf8").read())
        if name_lower in db:
            name = db[name_lower]['name']

            if name == "MissingNo.":
                _resp = requests.get("https://upload.wikimedia.org/wikipedia/commons/6/62/MissingNo.png")
                file = interactions.File("null.png", fp=io.BytesIO(_resp.content))
                embed = interactions.Embed(title="??????", description="".join("\n??????" for i in range(0, 3)))
                embed.set_thumbnail(url="attachment://null.png")
                return await ctx.send(embeds=embed, files=file)

            id = db[name_lower]['num']
            types = ", ".join(db[name_lower]['types'])
            desp = db[name_lower]['description']
            stats = "".join(
                [
                    f"**HP:** {db[name_lower]['baseStats']['hp']}\n",
                    f"**Attack:** {db[name_lower]['baseStats']['atk']}\n",
                    f"**Defense:** {db[name_lower]['baseStats']['def']}\n",
                    f"**Special Attack:** {db[name_lower]['baseStats']['spa']}\n",
                    f"**Special Defense:** {db[name_lower]['baseStats']['spd']}\n",
                    f"**Speed:** {db[name_lower]['baseStats']['spe']}\n",
                ]
            )
            abilities = ", ".join(list(db['bulbasaur']['abilities'].values()))
            egg_group = ", ".join(db[name_lower]['eggGroups'])
            height = db[name_lower]['heightm']
            weight = db[name_lower]['weightkg']

            if int(id) < int(10):
                id = "00" + str(id)
                id = int(id)
            elif int(id) < int(100):
                id = "0" + str(id)
                id = int(id)
            else:
                id = int(id)

            evs = db[name_lower]['evolutionLine']
            if str(evs) != "[]":
                evs = "\n".join(evs)
            else:
                evs = None

            sprites_url_still = f"https://www.serebii.net/art/th/{id}.png"

            footer = interactions.EmbedFooter(
                text=f"First introduced in Generation {db[name_lower]['generation']}",
                icon_url="https://seeklogo.com/images/P/pokeball-logo-DC23868CA1-seeklogo.com.png"
            )
            thumbnail = interactions.EmbedImageStruct(url=sprites_url_still)
            fields = [
                interactions.EmbedField(
                    name="Information",
                    value=f"".join(
                        [
                            f"**Entry:** {id}\n",
                            f"**Type(s):** {types}\n",
                            f"**Egg Groups:** {egg_group}\n",
                            f"**Height:** {height}\n",
                            f"**Weight:** {weight}",
                        ]
                    ),
                    inline=True
                ),
                interactions.EmbedField(name="Stats", value=stats, inline=True)
            ]
            embed = interactions.Embed(
                title=f"{name}",
                description=f"{desp}",
                footer=footer,
                thumbnail=thumbnail,
                fields=fields,
            )
            if evs is not None:
                embed.add_field(name="Evolution Line", value=evs, inline=True)

            await ctx.send(embeds=embed)


    @interactions.extension_autocomplete(
        command="pokedex",
        name="pokemon_name"
    )
    async def auto_complete(self, ctx: interactions.CommandContext, pokemon_name: str = ""):
        if pokemon_name != "":
            letters: list = pokemon_name
        else:
            letters = []
        data = json.loads(open("./db/pokemon.json", "r", encoding="utf8").read())
        if len(pokemon_name) == 0:
            await ctx.populate(
                [
                    interactions.Choice(
                        name=name[0].capitalize(),
                        value=name[0].capitalize()
                    ) for name in (
                        list(data.items())[0:9]
                        if len(data) > 10
                        else list(data.items())
                    )
                ]
            )
        else:
            choices: list = []
            for pkmn_name in data:
                focus: str = "".join(letters)
                if focus.lower() in pkmn_name and len(choices) < 20:
                    choices.append(
                    interactions.Choice(
                        name=pkmn_name.capitalize(),
                        value=pkmn_name.capitalize())
                    )
            await ctx.populate(choices)


    @interactions.extension_listener(name="on_message_create")
    async def message_create(self, message: interactions.Message):
        channel = await message.get_channel()
        if message.content.startswith("$shiny"):
            ends = int(len(message.content) - 7)
            msg = str(message.content)[-ends:].lower()
            data = json.loads(open("./db/pokemon.json", "r").read())
            if msg in data:
                img = f"https://play.pokemonshowdown.com/sprites/ani-shiny/{msg}.gif"
                embed = interactions.Embed(
                    image=interactions.EmbedImageStruct(url=img)
                )
                await channel.send(embeds=embed)

        elif message.content.startswith("$"):
            ends = int(len(message.content) - 1)
            msg = str(message.content)[-ends:].lower()
            data = json.loads(open("./db/pokemon.json", "r").read())
            if msg in data:
                img = f"https://play.pokemonshowdown.com/sprites/ani/{msg}.gif"
                embed = interactions.Embed(
                    image=interactions.EmbedImageStruct(url=img)
                )
                await channel.send(embeds=embed)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (
        datetime.datetime.now() + datetime.timedelta(hours=7)
    ).strftime("%d/%m/%Y %H:%M:%S")
    Pokemon(client)
    logging.debug("""[%s] Loaded Pokemon extension.""", log_time)
    print(f"[{log_time}] Loaded Pokemon extension.")
