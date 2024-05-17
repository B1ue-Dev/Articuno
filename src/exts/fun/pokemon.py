"""
Pokemon related commands.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import json
import re
from typing import List, Dict, Union
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)


data = json.loads(open("./src/db/pokemon.json", "r", encoding="utf8").read())
poketwo_list: List[str] = []
for mon in list(data.keys()):
    poketwo_list.append(data[mon]["name"])


class BaseStats:
    def __init__(self, hp, atk, defense, spa, spd, spe):
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.spa = spa
        self.spd = spd
        self.spe = spe


class Pokemon:
    """
    A class representing a Pokemon object.
    """

    __slots__ = [
        "num",
        "name",
        "description",
        "generation",
        "types",
        "baseStats",
        "abilities",
        "heightm",
        "weightkg",
        "color",
        "eggGroups",
        "evolutionLine",
    ]

    num: int
    """The index number of the Pokemon."""
    name: str
    """The name of the Pokemon."""
    description: str
    """A brief description of the Pokemon."""
    generation: int
    """The generation in which the Pokemon was introduced."""
    types: List[str]
    """A list of the Pokemon's types (e.g., ["Water", "Ice"])."""
    baseStats: BaseStats
    """A dictionary containing the Pokemon's base stats (e.g., {"hp": 45, "atk": 49, ...})."""
    abilities: dict[str, str]
    """A dictionary of the Pokemon's abilities (e.g., {0: "Blaze", "H": "Flash Fire"})."""
    heightm: float
    """The height of the Pokemon in meters."""
    weightkg: float
    """The weight of the Pokemon in kilograms."""
    color: str
    """The color of the Pokemon (e.g., "Blue")."""
    eggGroups: List[str]
    """A list of the Pokemon's egg groups."""
    evolutionLine: List[str]
    """A list representing the Pokemon's evolution line (e.g., ["Cyndaquil", "Quilava", "Typhlosion"])."""

    def __init__(self, **kwargs) -> None:
        self.num = kwargs.get("num", None)
        self.name = kwargs.get("name", None)
        self.description = kwargs.get("description", None)
        self.generation = kwargs.get("generation", None)
        self.types = kwargs.get("types", [])
        self.baseStats = BaseStats(
            hp=kwargs.get("baseStats", {}).get("hp"),
            atk=kwargs.get("baseStats", {}).get("atk"),
            defense=kwargs.get("baseStats", {}).get("defense"),
            spa=kwargs.get("baseStats", {}).get("spa"),
            spd=kwargs.get("baseStats", {}).get("spd"),
            spe=kwargs.get("baseStats", {}).get("spe"),
        )
        self.abilities = kwargs.get("abilities", {})
        self.heightm = kwargs.get("heightm", None)
        self.weightkg = kwargs.get("weightkg", None)
        self.color = kwargs.get("color", None)
        self.eggGroups = kwargs.get("eggGroups", [])
        self.evolutionLine = kwargs.get("evolutionLine", [])

    @classmethod
    def get_pokemon(cls, name: str) -> "Pokemon":
        """Get the information about a Pokemon."""

        def returnkey(text: str) -> str:
            # Remove non-alphabetic characters using regular expression
            r = re.sub(r"[^a-zA-Z]", "", text)
            return r.lower()

        name_key = data[returnkey(name)]
        return Pokemon(
            num=name_key.get("num"),
            name=name_key.get("name"),
            description=name_key.get("description"),
            generation=name_key.get("generation"),
            types=name_key.get("types", []),
            baseStats=name_key.get("baseStats", {}),
            abilities=name_key.get("abilities", {}),
            heightm=name_key.get("heightm"),
            weightkg=name_key.get("weightkg"),
            color=name_key.get("color"),
            eggGroups=name_key.get("eggGroups", []),
            evolutionLine=name_key.get("evolutionLine", []),
        )

    @property
    def url(self) -> str:
        """Returns the url of the Pokemon sprite."""

        return (
            f"https://www.serebii.net/art/th/{self.num}"
            + ("-h" if "Hisui" in self.name else "")
            + ".png"
        )

    @classmethod
    def db(cls):
        """Returns the full Pokemon db."""
        return data

    @classmethod
    def get_gen_list(cls, gen: int | None):
        if gen is not None:
            result = {
                name: info
                for name, info in cls.db().items()
                if info.get("generation") == int(gen)
            }
        else:
            result = data
        return result


class PKMCommand(interactions.Extension):
    """Extension for Pokemon-related commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @hybrid_slash_command(
        name="pokedex",
        description="Shows the information about a Pokemon.",
        integration_types=[
            interactions.IntegrationType.GUILD_INSTALL,
            interactions.IntegrationType.USER_INSTALL,
        ],
        silence_autocomplete_errors=True,
    )
    @interactions.slash_option(
        name="pokemon_name",
        description="Pokemon name",
        opt_type=interactions.OptionType.STRING,
        required=True,
        autocomplete=True,
    )
    async def pokedex(
        self, ctx: HybridContext, pokemon_name: interactions.ConsumeRest[str]
    ) -> None:
        """Shows the information about a Pokemon."""

        name_lower = pokemon_name.lower()
        pkm = Pokemon.get_pokemon(name_lower)
        name = data[name_lower]["name"] + (
            " (Hey, that's me!)"
            if data[name_lower]["name"] == "Articuno"
            else ""
        )
        id = pkm.num
        types = ", ".join(pkm.types)
        stats = "".join(
            [
                f"**HP:** {pkm.baseStats.hp}\n",
                f"**Attack:** {pkm.baseStats.atk}\n",
                f"**Defense:** {pkm.baseStats.defense}\n",
                f"**Special Attack:** {pkm.baseStats.spa}\n",
                f"**Special Defense:** {pkm.baseStats.spd}\n",
                f"**Speed:** {pkm.baseStats.spe}\n",
            ]
        )
        abilities = ", ".join(list(pkm.abilities.values()))
        egg_group = ", ".join(pkm.eggGroups)
        height = pkm.heightm
        weight = pkm.weightkg

        if int(id) < int(10):
            id = "00" + str(id)
            id = int(id)
        elif int(id) < int(100):
            id = "0" + str(id)
            id = int(id)
        else:
            id = int(id)

        evs = pkm.evolutionLine
        if str(evs) != "[]":
            evs = "\n".join(evs)
        else:
            evs = None

        footer = interactions.EmbedFooter(
            text=f"First introduced in Generation {data[name_lower]['generation']}",
            icon_url="https://seeklogo.com/images/P/pokeball-logo-DC23868CA1-seeklogo.com.png",
        )

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
            interactions.EmbedField(name="Stats", value=stats, inline=True),
        ]
        embed = interactions.Embed(
            title=f"{name}",
            description=pkm.description,
            footer=footer,
            images=interactions.EmbedAttachment(url=pkm.url),
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
                        "name": Pokemon.db[name]["name"],
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
                if (
                    focus.lower().strip()
                    in Pokemon.db[pkmn_name]["name"].lower()
                    and len(choices) < 20
                ):
                    choices.append(
                        {
                            "name": Pokemon.db[pkmn_name]["name"],
                            "value": pkmn_name,
                        }
                    )
            await ctx.send(choices)

    @hybrid_slash_command(
        name="poketwo",
        description="Search for Pokemon based on Poketwo hint.",
        integration_types=[
            interactions.IntegrationType.GUILD_INSTALL,
            interactions.IntegrationType.USER_INSTALL,
        ],
    )
    @interactions.slash_option(
        name="hint",
        description="The Poketwo hint.",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def poketwo(
        self, ctx: HybridContext, *, hint: interactions.ConsumeRest[str]
    ) -> None:
        """Search for Pokemon based on Poketwo hint."""

        result = []
        for i in poketwo_list:
            if len(i) == len(hint) and all(
                [
                    i[j] == hint[j]
                    or hint[j] == "_"
                    or (hint[j] == "-" and i[j] == "-")
                    for j in range(len(hint))
                ]
            ):
                result.append(i)
        if len(result) == 0:
            return await ctx.send("No result found.")

        cases: str = ""
        for case in result:
            cases += f"- {case}\n"
        await ctx.send(f"Here are all possible cases:\n{cases}")

    @interactions.listen()
    async def on_message_create(
        self, message: interactions.events.MessageCreate
    ) -> None:
        """Pokemon sprites related."""

        _msg: interactions.Message = message.message

        if _msg.content.startswith("$shiny"):
            ends = int(len(_msg.content) - 7)
            msg = str(_msg.content)[-ends:].lower()
            if msg in Pokemon.db():
                img = f"https://play.pokemonshowdown.com/sprites/ani-shiny/{msg}.gif"
                embed = interactions.Embed(
                    images=[interactions.EmbedAttachment(url=img)]
                )
                await _msg.channel.send(embeds=embed)

        elif _msg.content.startswith("$hisui"):
            ends = int(len(_msg.content) - 7)
            msg = str(_msg.content)[-ends:].lower()
            if f"{msg}hisui" in Pokemon.db():
                img = f"https://play.pokemonshowdown.com/sprites/ani/{msg}-hisui.gif"
                embed = interactions.Embed(
                    images=[interactions.EmbedAttachment(url=img)]
                )
                await _msg.channel.send(embeds=embed)

        elif _msg.content.startswith("$"):
            ends = int(len(_msg.content) - 1)
            msg = str(_msg.content)[-ends:].lower()
            if msg in Pokemon.db():
                img = f"https://play.pokemonshowdown.com/sprites/ani/{msg}.gif"
                embed = interactions.Embed(
                    images=[interactions.EmbedAttachment(url=img)]
                )
                await _msg.channel.send(embeds=embed)


def setup(client) -> None:
    """Setup the extension."""
    PKMCommand(client)
    logging.info("Loaded Pokemon extension.")
