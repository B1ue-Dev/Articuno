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
        db = json.loads(open("./db/pokemon.json", "r", encoding="utf8").read())
        if name_lower in db:
            name = db[name_lower]["name"] + (
                " (Hey, that's me!)"
                if db[name_lower]["name"] == "Articuno"
                else ""
            )
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
                description=f"{desp}",
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
        data: list[str] = json.loads(
            open("./db/pokemon.json", "r", encoding="utf8").read()
        )
        if len(pokemon_name) == 0:
            await ctx.send(
                [
                    {
                        "name": name[0].capitalize(),
                        "value": name[0].capitalize(),
                    }
                    for name in (
                        list(data.items())[0:24]
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
                        {
                            "name": pkmn_name.capitalize(),
                            "value": pkmn_name.capitalize(),
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
            data = json.loads(
                open("./db/pokemon.json", "r", encoding="utf8").read()
            )
            if msg in data:
                img = f"https://play.pokemonshowdown.com/sprites/ani-shiny/{msg}.gif"
                embed = interactions.Embed(
                    images=[interactions.EmbedAttachment(url=img)]
                )
                await _msg.channel.send(embeds=embed)

        elif _msg.content.startswith("$"):
            ends = int(len(_msg.content) - 1)
            msg = str(_msg.content)[-ends:].lower()
            data = json.loads(
                open("./db/pokemon.json", "r", encoding="utf8").read()
            )
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
