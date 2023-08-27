"""
Pokemon related commands.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import json
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)


data: list[str] = json.loads(
    open("./src/db/pokemon.json", "r", encoding="utf8").read()
)


class Pokemon(interactions.Extension):
    """Extension for /pokedex command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @hybrid_slash_command(
        name="pokedex",
        description="Shows the information about a Pokemon.",
        silence_autocomplete_errors=True,
    )
    @interactions.slash_option(
        name="pokemon_name",
        description="Pokemon name",
        opt_type=interactions.OptionType.STRING,
        required=True,
        autocomplete=True,
    )
    async def pokedex(self, ctx: HybridContext, pokemon_name: str) -> None:
        """Shows the information about a Pokemon."""

        name_lower = pokemon_name.lower()
        if name_lower in data:
            name = data[name_lower]["name"] + (
                " (Hey, that's me!)"
                if data[name_lower]["name"] == "Articuno"
                else ""
            )
            id = data[name_lower]["num"]
            types = ", ".join(data[name_lower]["types"])
            stats = "".join(
                [
                    f"**HP:** {data[name_lower]['baseStats']['hp']}\n",
                    f"**Attack:** {data[name_lower]['baseStats']['atk']}\n",
                    f"**Defense:** {data[name_lower]['baseStats']['def']}\n",
                    f"**Special Attack:** {data[name_lower]['baseStats']['spa']}\n",
                    f"**Special Defense:** {data[name_lower]['baseStats']['spd']}\n",
                    f"**Speed:** {data[name_lower]['baseStats']['spe']}\n",
                ]
            )
            abilities = ", ".join(list(data[name_lower]["abilities"].values()))
            egg_group = ", ".join(data[name_lower]["eggGroups"])
            height = data[name_lower]["heightm"]
            weight = data[name_lower]["weightkg"]

            if int(id) < int(10):
                id = "00" + str(id)
                id = int(id)
            elif int(id) < int(100):
                id = "0" + str(id)
                id = int(id)
            else:
                id = int(id)

            evs = data[name_lower]["evolutionLine"]
            if str(evs) != "[]":
                evs = "\n".join(evs)
            else:
                evs = None

            sprites_url_still = f"https://www.serebii.net/art/th/{id}.png"

            footer = interactions.EmbedFooter(
                text=f"First introduced in Generation {data[name_lower]['generation']}",
                icon_url="https://seeklogo.com/images/P/pokeball-logo-DC23868CA1-seeklogo.com.png",
            )
            thumbnail = interactions.EmbedAttachment(url=sprites_url_still)
            fields = [
                interactions.EmbedField(
                    name="Information",
                    value="".join(
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
                interactions.EmbedField(
                    name="Stats", value=stats, inline=True
                ),
            ]
            embed = interactions.Embed(
                title=f"{name}",
                footer=footer,
                thumbnail=thumbnail,
                fields=fields,
            )
            if evs is not None:
                embed.add_field(name="Evolution Line", value=evs, inline=True)

            await ctx.send(embeds=embed)

    @pokedex.autocomplete(option_name="pokemon_name")
    async def pokedex_autocomplete(
        self, ctx: interactions.AutocompleteContext
    ) -> None:
        """Autocomplete for /pokedex."""

        pokemon_name: str = ctx.input_text
        if pokemon_name != "":
            letters: list = pokemon_name
        else:
            letters = []
        if len(pokemon_name) == 0:
            await ctx.send(
                [
                    {
                        "name": data[name]["name"],
                        "value": name,
                    }
                    for name in (
                        list(data.keys())[0:24]
                        if len(data) > 10
                        else list(data.keys())
                    )
                ]
            )
        else:
            choices: list = []
            for pkmn_name in data:
                focus: str = "".join(letters)
                if focus.lower() in pkmn_name and len(choices) < 20:
                    choices.append(
                        {
                            "name": data[pkmn_name]["name"],
                            "value": pkmn_name,
                        }
                    )
            await ctx.send(choices)

    @interactions.listen()
    async def on_message_create(
        self, message: interactions.events.MessageCreate
    ) -> None:
        """Pokemon sprites related."""

        _msg: interactions.Message = message.message

        if _msg.content.startswith("$shiny"):
            ends = int(len(_msg.content) - 7)
            msg = str(_msg.content)[-ends:].lower()
            if msg in data:
                img = f"https://play.pokemonshowdown.com/sprites/ani-shiny/{msg}.gif"
                embed = interactions.Embed(
                    images=[interactions.EmbedAttachment(url=img)]
                )
                await _msg.channel.send(embeds=embed)

        elif _msg.content.startswith("$"):
            ends = int(len(_msg.content) - 1)
            msg = str(_msg.content)[-ends:].lower()
            if msg in data:
                img = f"https://play.pokemonshowdown.com/sprites/ani/{msg}.gif"
                embed = interactions.Embed(
                    images=[interactions.EmbedAttachment(url=img)]
                )
                await _msg.channel.send(embeds=embed)


def setup(client) -> None:
    """Setup the extension."""
    Pokemon(client)
    logging.info("Loaded Pokemon extension.")
