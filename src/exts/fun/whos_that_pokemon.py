"""
Who's that Pokemon command.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import io
import random
import asyncio
from time import time
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
from PIL import Image
from src.exts.fun.pokemon import Pokemon
from src.utils.utils import get_response


async def extract_pokemon_image(url: str) -> Image.Image:
    """
    Format the Pokemon image from the URL.

    :param url: The URL of the image.
    :type url: str
    :return: The formatted image.
    :rtype: Image
    """

    _resp = await get_response(url)
    img = Image.open(_resp).convert("RGBA")
    if img.size[0] > 120 and img.size[1] > 240:
        img = img.resize((int(img.width * 2.2), int(img.height * 2.2)))
    else:
        img = img.resize((int(img.width * 3), int(img.height * 3)))

    return img


async def generate_images(correct_pokemon: Pokemon) -> list[Image.Image]:
    """Generate the images for the command."""

    """The image of the Pokemon."""
    _image = await extract_pokemon_image(correct_pokemon.url)

    """Process the image and background."""
    _black_image = Image.new("RGBA", _image.size, (0, 0, 0))
    bg = Image.open("./src/img/whos_that_pokemon.png")

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
        description=f"{correct_pokemon.name}",
    )

    return [file, _file]


def get_pokemon(generation: int = None, user_id: int = None) -> list:
    """
    Get a random Pokemon from the database.

    :param generation: The generation of the Pokemon.
    :type generation: int
    :return: The Pokemon list.
    :rtype: list
    """

    seed = hash(str(user_id) + str(time()))
    random.seed(seed)

    pokemon_list = Pokemon.get_gen_list(generation)
    indices = list(range(len(pokemon_list)))
    chosen_indices = random.sample(indices, 4)
    chosen_pokemon = [
        {
            "num": list(pokemon_list.values())[i]["num"],
            "name": list(pokemon_list.values())[i]["name"],
        }
        for i in chosen_indices
    ]

    return chosen_pokemon


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
                pokemon_list: list = get_pokemon(generation, int(ctx.user.id))

                """The correct Pokemon."""
                corrected_pokemon: Pokemon = Pokemon.get_pokemon(
                    (pokemon_list[random.randint(0, 3)])["name"]
                )

                results = await generate_images(corrected_pokemon)
                file = results[0]
                _file = results[1]

                _button_list = []
                for i in range(4):
                    _button_list.append(
                        interactions.Button(
                            style=interactions.ButtonStyle.SECONDARY,
                            label=f"{pokemon_list[i]['name']}",
                            custom_id=f"{pokemon_list[i]['num']}",
                        )
                    )
                _button_list.append(
                    interactions.Button(
                        style=interactions.ButtonStyle.DANGER,
                        label="Give up",
                        custom_id="give_up",
                    )
                )

                msg = await _msg.edit(
                    content="**Who's that Pokemon?**",
                    components=_button_list,
                    file=file,
                )

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

                    if res.ctx.custom_id == str(corrected_pokemon.num):
                        _button_disabled = []
                        for i in range(4):
                            _button_disabled.append(
                                interactions.Button(
                                    style=interactions.ButtonStyle.SECONDARY
                                    if str(pokemon_list[i]["num"])
                                    != str(corrected_pokemon.num)
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
                                    f"It's **{corrected_pokemon.name}**!",
                                    f" {ctx.user.mention} had the right answer.",
                                ],
                            ),
                            components=_button_disabled,
                            file=_file,
                        )
                        cnt += 1
                        await asyncio.sleep(3)
                        await _msg.edit(
                            content=f"Generating...\nStreak: {cnt}",
                            components=[],
                            attachments=[],
                        )
                        continue

                    if res.ctx.custom_id == "give_up":
                        _button_disabled = []
                        for i in range(4):
                            _button_disabled.append(
                                interactions.Button(
                                    style=(
                                        interactions.ButtonStyle.SECONDARY
                                        if str(pokemon_list[i]["num"])
                                        != str(corrected_pokemon.num)
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
                                    label=f"{corrected_pokemon.name} (Bulbapedia)",
                                    url=f"https://bulbapedia.bulbagarden.net/wiki/{corrected_pokemon.name}_(Pokémon)",
                                )
                            ),
                        ]

                        await res.ctx.edit_origin(
                            content="".join(
                                [
                                    "**Who's that Pokemon?**\n\n",
                                    f"It's **{corrected_pokemon.name}**!",
                                    f" {ctx.user.mention} gave up.",
                                    f"\nStreak: {cnt}",
                                ],
                            ),
                            components=action_rows,
                            files=_file,
                        )
                        break

                    else:
                        _button_disabled = []
                        for i in range(4):
                            _button_disabled.append(
                                interactions.Button(
                                    style=(
                                        interactions.ButtonStyle.SECONDARY
                                        if str(pokemon_list[i]["num"])
                                        != str(corrected_pokemon.num)
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
                                    label=f"{corrected_pokemon.name} (Bulbapedia)",
                                    url=f"https://bulbapedia.bulbagarden.net/wiki/{corrected_pokemon.name}_(Pokémon)",
                                )
                            ),
                        ]

                        await res.ctx.edit_origin(
                            content="".join(
                                [
                                    "**Who's that Pokemon?**\n\n",
                                    f"It's **{corrected_pokemon.name}**!",
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
                                label=f"{corrected_pokemon.name} (Bulbapedia)",
                                url=f"https://bulbapedia.bulbagarden.net/wiki/{corrected_pokemon.name}_(Pokémon)",
                            )
                        ),
                    ]

                    await msg.edit(
                        content="".join(
                            [
                                "**Who's that Pokemon?**\n\n",
                                f"Timeout! It's **{corrected_pokemon.name}**!",
                                f"\nStreak: {cnt}",
                            ],
                        ),
                        components=action_rows,
                        files=_file,
                    )
                    break

        elif difficulty == "hard":
            cnt = 0

            while True:
                """List of Pokemon."""
                pokemon_list: list = get_pokemon(generation, int(ctx.user.id))

                """The correct Pokemon."""
                corrected_pokemon: Pokemon = Pokemon.get_pokemon(
                    (pokemon_list[random.randint(0, 3)])["name"]
                )

                results = await generate_images(corrected_pokemon)
                file = results[0]
                _file = results[1]

                button = [
                    interactions.Button(
                        style=interactions.ButtonStyle.SECONDARY,
                        label="Answer",
                        custom_id="answer",
                    ),
                    interactions.Button(
                        style=interactions.ButtonStyle.DANGER,
                        label="Give up",
                        custom_id="give_up",
                    ),
                ]
                msg = await _msg.edit(
                    content="**Who's that Pokemon?**",
                    components=button,
                    files=file,
                )

                try:

                    def _check(_ctx):
                        return int(_ctx.ctx.user.id) == int(ctx.user.id)

                    res = await self.client.wait_for_component(
                        components=button,
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
                    if res.ctx.custom_id == "give_up":
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
                                    label=f"{corrected_pokemon.name} (Bulbapedia)",
                                    url=f"https://bulbapedia.bulbagarden.net/wiki/{corrected_pokemon.name}_(Pokémon)",
                                )
                            ),
                        ]

                        await res.ctx.edit_origin(
                            content="".join(
                                [
                                    "**Who's that Pokemon?**\n\n",
                                    f"It's **{corrected_pokemon.name}**!",
                                    f" {ctx.user.mention} gave up.",
                                    f"\nStreak: {cnt}",
                                ],
                            ),
                            components=action_rows,
                            files=_file,
                        )
                        break

                    else:
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
                            == corrected_pokemon.name.lower()
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
                                        f"It's **{corrected_pokemon.name}**! ",
                                        f"{ctx.user.mention} had the right answer.",
                                    ]
                                ),
                                components=button_disabled,
                                files=_file,
                                attachments=[],
                            )
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
                                        label=f"{corrected_pokemon.name} (Bulbapedia)",
                                        url=f"https://bulbapedia.bulbagarden.net/wiki/{corrected_pokemon.name}_(Pokémon)",
                                    )
                                ),
                            ]

                            await _res.edit(
                                message=_res.message_id,
                                content="".join(
                                    [
                                        "**Who's that Pokemon?**\n\n",
                                        f"It's **{corrected_pokemon.name}**!",
                                        f" {ctx.user.mention} had the wrong answer.",
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
                                label=f"{corrected_pokemon.name} (Bulbapedia)",
                                url=f"https://bulbapedia.bulbagarden.net/wiki/{corrected_pokemon.name}_(Pokémon)",
                            ),
                        ),
                    ]

                    await msg.edit(
                        content="".join(
                            [
                                "**Who's that Pokemon?**\n\nTimeout! ",
                                f"It's **{corrected_pokemon.name}**!",
                                f"\nStreak: {cnt}",
                            ],
                        ),
                        components=action_rows,
                        attachments=[],
                        file=_file,
                    )
                    break


def setup(client) -> None:
    """Setup the extension."""
    WTP(client)
    logging.info("Loaded WTP extension.")
