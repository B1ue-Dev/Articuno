"""
Who's that Pokemon command.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import io
import random
import asyncio
import json
from typing import Any
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
import requests
from PIL import Image


def extract_pokemon_image(url: str) -> Image.Image:
    """
    Format the Pokemon image from the URL.

    :param url: The URL of the image.
    :type url: str
    :return: The formatted image.
    :rtype: Image
    """

    _resp = requests.get(url)
    if _resp.status_code == 200:
        img = Image.open(io.BytesIO(_resp.content)).convert("RGBA")
        if img.size[0] > 120 and img.size[1] > 240:
            img = img.resize((int(img.width * 2.2), int(img.height * 2.2)))
        else:
            img = img.resize((int(img.width * 3), int(img.height * 3)))

        return img


def get_pokemon(generation: int = None) -> list:
    """
    Get a random Pokemon from the database.

    :param generation: The generation of the Pokemon.
    :type generation: int
    :return: The Pokemon list.
    :rtype: list
    """

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
        elif generation == "9":
            generation = [906, 1010]

    for i in range(4):
        _num = random.randint(generation[0] - 1, generation[1] - 1)
        _val = list(db.values())[_num]

        _pokemon_list[i] = _val

    _lists = {}
    _list_number = []
    for i in range(4):
        if len(_list_number) < 5:
            if i not in _list_number:
                _lists[i] = {
                    "num": _pokemon_list[i]["num"],
                    "name": _pokemon_list[i]["name"],
                }
                _list_number.append(i)
            else:
                continue

    return _lists


class WTP(interactions.Extension):
    """Extension for /whos_that_pokemon command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @hybrid_slash_command(
        name="whos_that_pokemon",
        description="Who's that Pokemon game.",
        aliases=["wtp"],
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="difficulty",
                description="Difficulty of the game",
                choices=[
                    interactions.SlashCommandChoice(name="easy", value="easy"),
                    interactions.SlashCommandChoice(name="hard", value="hard"),
                ],
                required=True,
            ),
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="generation",
                description="Generation of the Pokemon",
                choices=[
                    interactions.SlashCommandChoice(
                        name=f"Gen {i}", value=f"{i}"
                    )
                    for i in range(1, 10)
                ],
                required=False,
            ),
        ],
    )
    @interactions.cooldown(interactions.Buckets.USER, 3, 10)
    async def whos_that_pokemon(
        self,
        ctx: HybridContext,
        difficulty: str,
        generation: str = None,
    ) -> None:
        """Who's that Pokemon game."""

        _msg = await ctx.send("Generating...")

        if difficulty == "easy":
            cnt = 0

            while True:
                """List of Pokemon."""
                pokemon_list: list = get_pokemon(generation)

                """The correct Pokemon."""
                correct_pokemon: Any = pokemon_list[random.randint(0, 3)]

                """The image of the Pokemon."""
                _image = extract_pokemon_image(
                    f"https://www.serebii.net/art/th/{correct_pokemon['num']}.png"
                )

                """Process the image and background."""
                _black_image = Image.new("RGBA", _image.size, (0, 0, 0))
                bg = Image.open("./img/whos_that_pokemon.png")

                _num = (400, 230)
                text_img = Image.new("RGBA", bg.size, (255, 255, 255, 0))
                text_img.paste(bg, (0, 0))
                text_img.paste(_black_image, _num, _image)

                """Image for the user guessing the Pokemon."""
                out1 = io.BytesIO()
                text_img.save(out1, format="PNG")
                out1.seek(0)
                file = interactions.File(
                    file_name="image.png",
                    file=out1,
                    description="Guess the Pokemon.",
                )

                """Image for the correct Pokemon."""
                _text_img = Image.new("RGBA", bg.size, (255, 255, 255, 0))
                _text_img.paste(bg, (0, 0))
                _text_img.paste(_image, _num, _image)

                out2 = io.BytesIO()
                _text_img.save(out2, format="PNG")
                out2.seek(0)
                _file = interactions.File(
                    file_name="image.png",
                    file=out2,
                    description=f"{correct_pokemon['name']}",
                )

                _button_list = []
                for i in range(4):
                    _button_list.append(
                        interactions.Button(
                            style=interactions.ButtonStyle.SECONDARY,
                            label=f"{pokemon_list[i]['name']}",
                            custom_id=f"{pokemon_list[i]['num']}",
                        )
                    )

                msg = await _msg.edit(
                    content="**Who's that Pokemon?**",
                    components=_button_list,
                    file=file,
                )
                out1.close()

                try:

                    def _check(_ctx):
                        return int(_ctx.ctx.user.id) == int(
                            ctx.user.id
                        ) and int(_ctx.ctx.channel_id) == int(ctx.channel_id)

                    res = await self.client.wait_for_component(
                        components=_button_list,
                        messages=int(msg.id),
                        check=_check,
                        timeout=15,
                    )

                    if res.ctx.custom_id == str(correct_pokemon["num"]):
                        _button_disabled = []
                        for i in range(4):
                            _button_disabled.append(
                                interactions.Button(
                                    style=interactions.ButtonStyle.SECONDARY
                                    if str(pokemon_list[i]["num"])
                                    != str(correct_pokemon["num"])
                                    else interactions.ButtonStyle.SUCCESS,
                                    label=f"{pokemon_list[i]['name']}",
                                    custom_id=f"{pokemon_list[i]['num']}",
                                    disabled=True,
                                )
                            )

                        await res.ctx.edit_origin(
                            content="".join(
                                [
                                    "**Who's that Pokemon?**\n\n",
                                    f"It's **{correct_pokemon['name']}**!",
                                    f" {ctx.user.mention} had the right answer.",
                                ],
                            ),
                            components=_button_disabled,
                            file=_file,
                        )
                        out2.close()
                        cnt += 1
                        await asyncio.sleep(3)
                        await _msg.edit(
                            content=f"Generating...\nStreak: {cnt}",
                            components=[],
                            attachments=[],
                        )
                        continue

                    else:
                        _button_disabled = []
                        for i in range(4):
                            _button_disabled.append(
                                interactions.Button(
                                    style=(
                                        interactions.ButtonStyle.SECONDARY
                                        if str(pokemon_list[i]["num"])
                                        != str(correct_pokemon["num"])
                                        and str(pokemon_list[i]["num"])
                                        != str(res.ctx.custom_id)
                                        else (
                                            interactions.ButtonStyle.DANGER
                                            if str(pokemon_list[i]["num"])
                                            == str(res.ctx.custom_id)
                                            else interactions.ButtonStyle.SUCCESS
                                        )
                                    ),
                                    label=f"{pokemon_list[i]['name']}",
                                    custom_id=f"{pokemon_list[i]['num']}",
                                    disabled=True,
                                )
                            )

                        action_rows: list[interactions.ActionRow] = [
                            interactions.ActionRow(*_button_disabled),
                            interactions.ActionRow(
                                interactions.Button(
                                    style=interactions.ButtonStyle.LINK,
                                    label=f"{correct_pokemon['name']} (Bulbapedia)",
                                    url=f"https://bulbapedia.bulbagarden.net/wiki/{correct_pokemon['name']}_(Pokémon)",
                                )
                            ),
                        ]

                        await res.ctx.edit_origin(
                            content="".join(
                                [
                                    "**Who's that Pokemon?**\n\n",
                                    f"It's **{correct_pokemon['name']}**!",
                                    f" {ctx.user.mention} had the wrong answer.",
                                    f"\nStreak: {cnt}",
                                ],
                            ),
                            components=action_rows,
                            files=_file,
                        )
                        break

                except asyncio.TimeoutError:  # When timeout.
                    _button_disabled = []
                    for i in range(4):
                        _button_disabled.append(
                            interactions.Button(
                                style=interactions.ButtonStyle.SECONDARY,
                                label=f"{pokemon_list[i]['name']}",
                                custom_id=f"{pokemon_list[i]['num']}",
                                disabled=True,
                            )
                        )

                    action_rows: list[interactions.ActionRow] = [
                        interactions.ActionRow(*_button_disabled),
                        interactions.ActionRow(
                            interactions.Button(
                                style=interactions.ButtonStyle.LINK,
                                label=f"{correct_pokemon['name']} (Bulbapedia)",
                                url=f"https://bulbapedia.bulbagarden.net/wiki/{correct_pokemon['name']}_(Pokémon)",
                            )
                        ),
                    ]

                    await msg.edit(
                        content="".join(
                            [
                                "**Who's that Pokemon?**\n\n",
                                f"Timeout! It's **{correct_pokemon['name']}**!",
                                f"\nStreak: {cnt}",
                            ],
                        ),
                        components=action_rows,
                        files=_file,
                    )
                    break
            out2.close()  # Close the file.

        elif difficulty == "hard":
            cnt = 0

            while True:
                """List of Pokemon."""
                pokemon_list: list = get_pokemon(generation)

                """The correct Pokemon."""
                correct_pokemon: Any = pokemon_list[random.randint(0, 3)]

                """The image of the Pokemon."""
                _image = extract_pokemon_image(
                    f"https://www.serebii.net/art/th/{correct_pokemon['num']}.png"
                )

                """Process the image and background."""
                _black_image = Image.new("RGBA", _image.size, (0, 0, 0))
                bg = Image.open("./img/whos_that_pokemon.png")

                _num = (400, 230)
                text_img = Image.new("RGBA", bg.size, (255, 255, 255, 0))
                text_img.paste(bg, (0, 0))
                text_img.paste(_black_image, _num, _image)

                """Image for the user guessing the Pokemon."""
                out1 = io.BytesIO()
                text_img.save(out1, format="PNG")
                out1.seek(0)
                file = interactions.File(
                    file_name="image.png",
                    file=out1,
                    description="Guess the Pokemon.",
                )

                """Image for the correct Pokemon."""
                _text_img = Image.new("RGBA", bg.size, (255, 255, 255, 0))
                _text_img.paste(bg, (0, 0))
                _text_img.paste(_image, _num, _image)

                out2 = io.BytesIO()
                _text_img.save(out2, format="PNG")
                out2.seek(0)
                _file = interactions.File(
                    file_name="image.png",
                    file=out2,
                    description=f"{correct_pokemon['name']}",
                )

                button = interactions.Button(
                    style=interactions.ButtonStyle.SECONDARY,
                    label="Answer",
                    custom_id="answer",
                )
                msg = await _msg.edit(
                    content="**Who's that Pokemon?**",
                    components=button,
                    files=file,
                )

                try:

                    def _check(_ctx):
                        return int(_ctx.ctx.user.id) == int(ctx.user.id)

                    res = await self.client.wait_for_component(
                        components=[button],
                        check=_check,
                        messages=int(msg.id),
                        timeout=15,
                    )

                    modal = interactions.Modal(
                        title="Who's that Pokemon?",
                        custom_id="_wtp",
                    )
                    modal.add_components(
                        interactions.InputText(
                            label="Your answer",
                            style=interactions.TextStyles.SHORT,
                            placeholder="Ex: Pikachu ⚠ (Do not hit Cancel)",
                            custom_id="answer",
                            max_length=100,
                        ),
                    )

                    await res.ctx.send_modal(modal)

                    def _check(_ctx):
                        return int(_ctx.ctx.user.id) == int(ctx.user.id)

                    _res = await self.client.wait_for_modal(
                        modal=modal,
                        author=ctx.author,
                        timeout=15,
                    )

                    if (
                        _res.responses["answer"].lower().rstrip()
                        == correct_pokemon["name"].lower()
                    ):
                        button_disabled = interactions.Button(
                            style=interactions.ButtonStyle.SECONDARY,
                            label="Answer",
                            custom_id="answer",
                            disabled=True,
                        )

                        await _res.edit(
                            message=_res.message_id,
                            content="".join(
                                [
                                    "**Who's that Pokemon?**\n\n",
                                    f"It's **{correct_pokemon['name']}**! ",
                                    f"{ctx.user.mention} had the right answer.",
                                ]
                            ),
                            components=button_disabled,
                            files=_file,
                            attachments=[],
                        )
                        out2.close()
                        cnt += 1
                        await asyncio.sleep(3)
                        await _msg.edit(
                            content=f"Generating...\nStreak: {cnt}",
                            components=[],
                            attachments=[],
                        )
                        continue

                    else:
                        action_rows = [
                            interactions.ActionRow(
                                interactions.Button(
                                    style=interactions.ButtonStyle.SECONDARY,
                                    label="Answer",
                                    custom_id="answer",
                                    disabled=True,
                                )
                            ),
                            interactions.ActionRow(
                                interactions.Button(
                                    style=interactions.ButtonStyle.LINK,
                                    label=f"{correct_pokemon['name']} (Bulbapedia)",
                                    url=f"https://bulbapedia.bulbagarden.net/wiki/{correct_pokemon['name']}_(Pokémon)",
                                )
                            ),
                        ]

                        await _res.edit(
                            message=_res.message_id,
                            content="".join(
                                [
                                    "**Who's that Pokemon?**\n\n",
                                    f"It's **{correct_pokemon['name']}**!",
                                    f"{ctx.user.mention} had the wrong answer.",
                                    f"\nStreak: {cnt}",
                                ],
                            ),
                            components=action_rows,
                            files=_file,
                            attachments=[],
                        )
                        break

                except asyncio.TimeoutError:
                    action_rows = [
                        interactions.ActionRow(
                            interactions.Button(
                                style=interactions.ButtonStyle.SECONDARY,
                                label="Answer",
                                custom_id="answer",
                                disabled=True,
                            ),
                        ),
                        interactions.ActionRow(
                            interactions.Button(
                                style=interactions.ButtonStyle.LINK,
                                label=f"{correct_pokemon['name']} (Bulbapedia)",
                                url=f"https://bulbapedia.bulbagarden.net/wiki/{correct_pokemon['name']}_(Pokémon)",
                            ),
                        ),
                    ]

                    await msg.edit(
                        content="".join(
                            [
                                "**Who's that Pokemon?**\n\nTimeout! ",
                                f"It's **{correct_pokemon['name']}**!",
                                f"\nStreak: {cnt}",
                            ],
                        ),
                        components=action_rows,
                        attachments=[],
                        file=_file,
                    )
                    break
            out2.close()  # Close the file.


def setup(client) -> None:
    """Setup the extension."""
    WTP(client)
    logging.info("Loaded WTP extension.")
