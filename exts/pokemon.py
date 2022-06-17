"""
This module is for Pokemon commands.

(C) 2022 - Jimmy-Blue
"""

import random
import asyncio
import json
import interactions
from interactions import extension_command as command
from utils.utils import get_response


class Pokemon(interactions.Extension):
    def __init__(self, bot):
        self.bot = bot

    @command(
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
        url = "https://some-random-api.ml/pokedex"
        params = {
            "pokemon": pokemon_name
        }
        resp = await get_response(url, params)
        try:
            desp = resp['description']
            gen = resp['generation']
            id = resp['id']
            abilities = str(resp['abilities'])
            abilities = abilities.replace("'", "")
            abilities = abilities.replace("[", "")
            abilities = abilities.replace("]", "")
            evs = int(resp['family']['evolutionStage'])
            if evs != 0:
                evs = str(resp['family']['evolutionLine'])
                evs = evs.replace("'", "")
                evs = evs.replace("[", "")
                evs = evs.replace("]", "")
            else:
                evs = None
            if int(id) < int(10):
                id = "00" + str(id)
                id = int(id)
            elif int(id) < int(100):
                id = "0" + str(id)
                id = int(id)
            else:
                id = int(id)
            sprites_url_still = f"https://www.serebii.net/art/th/{id}.png"
            data = json.loads(open("./db/pokemon.json", "r", encoding="utf8").read())
            if name_lower in data:
                name = data[name_lower]['name']
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

                footer = interactions.EmbedFooter(
                    text=f"First introduced in Generation {gen}",
                    icon_url="https://seeklogo.com/images/P/pokeball-logo-DC23868CA1-seeklogo.com.png"
                )
                thumbnail = interactions.EmbedImageStruct(url=sprites_url_still)
                fields = [
                    interactions.EmbedField(
                        name="Information",
                        value=f"**Entry:** {id}\n**Type(s):** {types}\n**Abilities:** {abilities}\n**Egg Groups:** {egg_group}\n**Height:** {height}\n**Weight:** {weight}", inline=True
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
            else:
                await ctx.send("Pokemon not found.")
        except TypeError:
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


    @interactions.extension_command(
        name="who_is_that_pokemon",
        description="Who's that Pokemon game",
    )
    async def whos_that_pokemon(self, ctx: interactions.CommandContext):
        await ctx.defer()

        _pokemon_list = {}
        db = json.loads(open("./db/pokemon.json", "r", encoding="utf8").read())

        for i in range(4):
            _num = random.randint(1, 905)
            _val = list(db.values())[_num]

            _pokemon_list[i] = _val

        _lists = {}
        for i in range(4):
            _lists[i] = {"num": _pokemon_list[i]['num'], "name": _pokemon_list[i]['name']}

        _correct_pokemon = _lists[random.randint(0, 3)]

        _button_list = []
        for i in range(4):
            _button_list.append(
                interactions.Button(
                    style=interactions.ButtonStyle.SECONDARY,
                    label=f"{_lists[i]['name']}",
                    custom_id=f"{_lists[i]['num']}"
                )
            )

        embed = interactions.Embed(
            title="Who's that Pokemon?",
            image=interactions.EmbedImageStruct(url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{_correct_pokemon['num']}.png"),
        )

        msg = await ctx.send(embeds=embed, components=_button_list)

        while True:
            try:
                res = await self.bot.wait_for_component(components=_button_list, messages=int(msg.id), timeout = 15)
                if int(res.user.id) == int(ctx.user.id):
                    if str(res.custom_id) == str(_correct_pokemon['num']):
                        _button_disabled = []
                        for i in range(4):
                            _button_disabled.append(
                                interactions.Button(
                                    style=interactions.ButtonStyle.SECONDARY if str(_lists[i]['num']) != str(_correct_pokemon['num']) else interactions.ButtonStyle.SUCCESS,
                                    label=f"{_lists[i]['name']}",
                                    custom_id=f"{_lists[i]['num']}",
                                    disabled=True
                                )
                            )

                        embed = interactions.Embed(
                            title="Who's that Pokemon?",
                            image=interactions.EmbedImageStruct(url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{_correct_pokemon['num']}.png"),
                            description=f"It's **{_correct_pokemon['name']}**! {ctx.user.mention} had the right answer.",
                        )

                        await res.edit(embeds=embed, components=_button_disabled)
                        break
                    else:
                        _button_disabled = []
                        for i in range(4):
                            _button_disabled.append(
                                interactions.Button(
                                    style=(
                                        interactions.ButtonStyle.SECONDARY if str(_lists[i]['num']) != str(_correct_pokemon['num']) and str(_lists[i]['num']) != str(res.custom_id)
                                        else (interactions.ButtonStyle.DANGER if str(_lists[i]['num']) == str(res.custom_id) else interactions.ButtonStyle.SUCCESS)
                                    ),
                                    label=f"{_lists[i]['name']}",
                                    custom_id=f"{_lists[i]['num']}",
                                    disabled=True
                                )
                            )
                        _action_rows = [
                            interactions.ActionRow(
                                components=_button_disabled
                            ),
                            interactions.ActionRow(
                                components=[
                                    interactions.Button(
                                        style=interactions.ButtonStyle.LINK,
                                        label=f"{_correct_pokemon['name']} (Bulbapedia)",
                                        url=f"https://bulbapedia.bulbagarden.net/wiki/{_correct_pokemon['name']}_(Pokémon)",
                                    )
                                ]
                            )
                        ]

                        embed = interactions.Embed(
                            title="Who's that Pokemon?",
                            image=interactions.EmbedImageStruct(url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{_correct_pokemon['num']}.png"),
                            description=f"It's **{_correct_pokemon['name']}**! {ctx.user.mention} had the wrong answer.",
                        )

                        await res.edit(embeds=embed, components=_action_rows)
                        break

            except asyncio.TimeoutError:
                await msg.edit("Time out!")
                break


def setup(bot):
    Pokemon(bot)
