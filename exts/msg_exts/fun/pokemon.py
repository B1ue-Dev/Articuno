"""
This module is for Pokemon commands.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import json
import interactions
from interactions.ext import molter


class Pokemon(molter.MolterExtension):
    """Extension for /pokedex command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @molter.prefixed_command(name="pokedex")
    async def _pokedex(self, ctx: molter.MolterContext, pokemon_name: str):
        """Shows the information about a Pokemon."""

        name_lower = pokemon_name.lower()
        db = json.loads(open("./db/pokemon.json", "r", encoding="utf8").read())
        if name_lower in db:
            name = db[name_lower]["name"]
            id = db[name_lower]["num"]
            types = ", ".join(db[name_lower]["types"])
            desp = db[name_lower]["description"]
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
            abilities = ", ".join(list(db[name_lower]["abilities"].values()))
            egg_group = ", ".join(db[name_lower]["eggGroups"])
            height = db[name_lower]["heightm"]
            weight = db[name_lower]["weightkg"]

            if int(id) < int(10):
                id = "00" + str(id)
                id = int(id)
            elif int(id) < int(100):
                id = "0" + str(id)
                id = int(id)
            else:
                id = int(id)

            evs = db[name_lower]["evolutionLine"]
            if str(evs) != "[]":
                evs = "\n".join(evs)
            else:
                evs = None

            sprites_url_still = f"https://www.serebii.net/art/th/{id}.png"

            footer = interactions.EmbedFooter(
                text=f"First introduced in Generation {db[name_lower]['generation']}",
                icon_url="https://seeklogo.com/images/P/pokeball-logo-DC23868CA1-seeklogo.com.png",
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
                            f"**Weight:** {weight}\n",
                            f"**Abilities:** {abilities}",
                        ]
                    ),
                    inline=True,
                ),
                interactions.EmbedField(name="Stats", value=stats, inline=True),
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


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Pokemon(client)
    logging.debug("""[%s] Loaded Pokemon extension.""", log_time)
