"""
This module is for Pokemon commands.

(C) 2022 - Jimmy-Blue
"""

import io
import random
import asyncio
import json
import interactions
from interactions import extension_command as command
from interactions.ext.wait_for import wait_for
import requests
from PIL import Image
from utils.utils import get_response


def _pokemon_image(url: str):
    _resp = requests.get(url)
    if _resp.status_code == 200:
        _pokemon = Image.open(io.BytesIO(_resp.content)).resize((720, 720)).convert('RGBA')

        return _pokemon


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
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="difficulty",
                description="Difficulty of the game",
                choices=[
                    interactions.Choice(name="Easy", value="easy"),
                    interactions.Choice(name="Hard", value="hard"),
                ],
                required=True,
            ),
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="generation",
                description="Generation of the Pokemon",
                choices=[interactions.Choice(name=f"Gen {i}", value=f"{i}") for i in range(1, 9)],
                required=False,
            )
        ]
    )
    async def whos_that_pokemon(self, ctx: interactions.CommandContext, difficulty: str, generation: str = None):
        await ctx.defer()

        _pokemon_list = {}
        db = json.loads(open("./db/pokemon.json", "r", encoding="utf8").read())

        if generation is None:
            generation = [1, 905]
        else:
            if generation == "1":
                generation = [1, 151]
            elif generation == "2":
                generation = [152, 251]
            elif generation == "3":
                generation = [252, 386]
            elif generation == "4":
                generation = [387, 493]
            elif generation == "5":
                generation = [494, 649]
            elif generation == "6":
                generation = [650, 721]
            elif generation == "7":
                generation = [722, 809]
            elif generation == "8":
                generation = [810, 905]

        for i in range(4):
            _num = random.randint(generation[0], generation[1])
            _val = list(db.values())[_num]

            _pokemon_list[i] = _val

        _lists = {}
        for i in range(4):
            _lists[i] = {"num": _pokemon_list[i]['num'], "name": _pokemon_list[i]['name']}

        _correct_pokemon = _lists[random.randint(0, 3)]
        _correct_pokemon_hard = _lists[0]

        _image = _pokemon_image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{_correct_pokemon['num']}.png")

        _image = _pokemon_image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{_correct_pokemon['num']}.png")
        _black_image = Image.new('RGBA', _image.size, (0, 0, 0))

        bg = Image.open("whos_that_pokemon.png")

        _num = (235, 180)
        text_img = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        text_img.paste(bg, (0, 0))
        text_img.paste(_black_image, _num, _image)

        with io.BytesIO() as out:
            text_img.save(out, format="PNG")
            file = interactions.File(filename="image.png", fp=out.getvalue())

        _text_img = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        _text_img.paste(bg, (0, 0))
        _text_img.paste(_image, _num, _image)

        with io.BytesIO() as out:
            _text_img.save(out, format="PNG")
            _file = interactions.File(filename="_image.png", fp=out.getvalue())

        if difficulty == "easy":

            _button_list = []
            for i in range(4):
                _button_list.append(
                    interactions.Button(
                        style=interactions.ButtonStyle.SECONDARY,
                        label=f"{_lists[i]['name']}",
                        custom_id=f"{_lists[i]['num']}"
                    )
                )

            msg = await ctx.send(content="**Who's that Pokemon?**", components=_button_list, files=file)

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

                            await res.edit(
                                content=f"**Who's that Pokemon?**\n\nIt's **{_correct_pokemon['name']}**! {ctx.user.mention} had the right answer.",
                                components=_button_disabled,
                                files=_file
                            )
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

                            await res.edit(
                                content=f"**Who's that Pokemon?**\n\nIt's **{_correct_pokemon['name']}**! {ctx.user.mention} had the wrong answer.",
                                components=_button_disabled,
                                files=_file
                            )
                            break

                except asyncio.TimeoutError:

                    _button_disabled = []
                    for i in range(4):
                        _button_disabled.append(
                            interactions.Button(
                                style=interactions.ButtonStyle.SECONDARY,
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

                    await msg.edit(
                        content=f"**Who's that Pokemon?**\n\nTimeout! It's **{_correct_pokemon['name']}**!",
                        components=_action_rows,
                        files=_file
                    )
                    break
        
        elif difficulty == "hard":

            button = interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="Answer",
                custom_id="answer"
            )
            msg = await ctx.send(content="**Who's that Pokemon?**", components=[button], files=file)

            while True:
                try:
                    res = await self.bot.wait_for_component(components=[button], messages=int(msg.id), timeout = 15)
                    if int(res.user.id) == int(ctx.user.id):
                        
                        modal = interactions.Modal(
                            title="Who's that Pokemon?",
                            custom_id="_wtp",
                            components=[
                                interactions.TextInput(
                                    style=interactions.TextStyleType.SHORT,
                                    label="Your answer",
                                    placeholder="Ex: Pikachu ⚠ (Do not hit Cancel)",
                                    custom_id="_answer",
                                    max_length=100,
                                ),
                            ]
                        )

                        await res.popup(modal)
                    
                        def check(_ctx: interactions.CommandContext):
                             return _ctx.data.custom_id == "_wtp" and _ctx.user.id == ctx.user.id

                        _res: interactions.ComponentContext = await wait_for(self.bot, "on_modal", check=check, timeout=15)
                        _answer = _res.data._json['components'][0].get('components')[0]['value']

                        if _answer.lower().rstrip() == _correct_pokemon_hard['name'].lower():

                            _button_disabled = interactions.Button(
                                style=interactions.ButtonStyle.SECONDARY,
                                label="Answer",
                                custom_id="answer",
                                disabled=True
                            )

                            await _res.send()
                            await msg.edit(
                                content=f"**Who's that Pokemon?**\n\nIt's **{_correct_pokemon_hard['name']}**! {ctx.user.mention} had the right answer.",
                                components=[_button_disabled],
                                files=_file
                            ) 
                            break

                        else:

                            _action_rows = [
                                interactions.ActionRow(
                                    components=[
                                        interactions.Button(
                                            style=interactions.ButtonStyle.SECONDARY,
                                            label="Answer",
                                            custom_id="answer",
                                            disabled=True
                                        )
                                    ]
                                ),
                                interactions.ActionRow(
                                    components=[
                                        interactions.Button(
                                            style=interactions.ButtonStyle.LINK,
                                            label=f"{_correct_pokemon['name']} (Bulbapedia)",
                                            url=f"https://bulbapedia.bulbagarden.net/wiki/{_correct_pokemon_hard['name']}_(Pokémon)",
                                        )
                                    ]
                                )
                            ]

                            await _res.send()
                            await msg.edit(
                                content=f"**Who's that Pokemon?**\n\nIt's **{_correct_pokemon_hard['name']}**! {ctx.user.mention} had the wrong answer.",
                                components=_action_rows,
                                files=_file
                            )
                            break

                except asyncio.TimeoutError:

                    _action_rows = [
                        interactions.ActionRow(
                            components=[
                                interactions.Button(
                                    style=interactions.ButtonStyle.SECONDARY,
                                    label="Answer",
                                    custom_id="answer",
                                    disabled=True
                                )
                            ]
                        ),
                        interactions.ActionRow(
                            components=[
                                interactions.Button(
                                    style=interactions.ButtonStyle.LINK,
                                    label=f"{_correct_pokemon_hard['name']} (Bulbapedia)",
                                    url=f"https://bulbapedia.bulbagarden.net/wiki/{_correct_pokemon_hard['name']}_(Pokémon)",
                                )
                            ]
                        )
                    ]

                    await msg.edit(
                        content=f"**Who's that Pokemon?**\n\nTimeout! It's **{_correct_pokemon_hard['name']}**!",
                        components=_action_rows,
                        files=_file
                    )
                    break



def setup(bot):
    Pokemon(bot)
