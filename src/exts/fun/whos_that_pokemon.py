"""
Who's that Pokemon command.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import io
import random
import asyncio
from time import time
from datetime import datetime
from beanie import PydanticObjectId
import interactions
from interactions.ext.paginators import Paginator
from interactions.ext.hybrid_commands import (
    hybrid_slash_subcommand,
    HybridContext,
)
from PIL import Image
from src.exts.fun.pokemon import Pokemon
from src.exts.core.info import get_color
from src.common.utils import get_response, wtp_easy_saves, wtp_hard_saves


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
    print(f"Image size: {img.size}")
    if img.size[1] <= 130:
        print("small image")
        img = img.resize((int(img.width * 3.9), int(img.height * 3.9)))
    elif img.size[1] <= 160:
        print("medium image")
        img = img.resize((int(img.width * 3.4), int(img.height * 3.4)))
    elif img.size[1] <= 190:
        print("large image")
        img = img.resize((int(img.width * 2.7), int(img.height * 2.7)))
    elif img.size[1] <= 235:
        print("extra large image")
        img = img.resize((int(img.width * 2.35), int(img.height * 2.35)))
    else:
        print("????? image")
        img = img.resize((int(img.width * 2), int(img.height * 2)))

    return img


async def generate_images(correct_pokemon: Pokemon) -> list[Image.Image]:
    """Generate the images for the command."""

    """The image of the Pokemon."""
    _image = await extract_pokemon_image(correct_pokemon.url)

    """Process the image and background."""
    _black_image = Image.new("RGBA", _image.size, (0, 0, 0))
    bg = Image.open("./src/assets/whos_that_pokemon_1_optimized.png")
    bg_width, bg_height = bg.size
    center_x, center_y = 470, 410
    paste_x = center_x - _image.width // 2
    paste_y = center_y - _image.height // 2
    paste_pos = (paste_x, paste_y)

    text_img = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    text_img.paste(bg, (0, 0))
    text_img.paste(_black_image, paste_pos, _image)

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
    _text_img.paste(_image, paste_pos, _image)

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
            "name": list(pokemon_list.keys())[i],
        }
        for i in chosen_indices
    ]

    return chosen_pokemon


class WTP(interactions.Extension):
    """Extension for /whos_that_pokemon command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @hybrid_slash_subcommand(
        base="whos_that_pokemon",
        base_description="Who's that Pokemon game.",
        name="play",
        description="Play Who's that Pokemon game.",
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

                # Only allow points if generation is not specified
                point_eligible = True
                if generation is not None:
                    point_eligible = False

                if point_eligible:
                    if not await wtp_easy_saves.find_one(
                        wtp_easy_saves.user_id == int(ctx.user.id)
                    ).exists():
                        await wtp_easy_saves(
                            user_id=int(ctx.user.id),
                            user_name=ctx.user.username,
                            points=0,
                            history=[],
                        ).save()

                """The correct Pokemon."""
                corrected_pokemon: Pokemon = Pokemon.get_pokemon(
                    (pokemon_list[random.randint(0, 3)])["name"]
                )
                logging.info("Pokemon list: {}".format(pokemon_list))
                logging.info("Correct Pokemon: {}".format(corrected_pokemon))

                results = await generate_images(corrected_pokemon)
                file = results[0]
                _file = results[1]

                _button_list = []
                for i in range(4):
                    _button_list.append(
                        interactions.Button(
                            style=interactions.ButtonStyle.SECONDARY,
                            label=f"{Pokemon.get_pokemon(pokemon_list[i]['name']).name}",
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
                    content=f"""**Who's that Pokemon?**\n\n{"Point system enabled (random generation)." if point_eligible else "Point system disabled (specific generation)."}""",
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
                                    style=(
                                        interactions.ButtonStyle.SECONDARY
                                        if str(pokemon_list[i]["num"])
                                        != str(corrected_pokemon.num)
                                        else interactions.ButtonStyle.SUCCESS
                                    ),
                                    label=f"{Pokemon.get_pokemon(pokemon_list[i]['name']).name}",
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
                                    label=f"{Pokemon.get_pokemon(pokemon_list[i]['name']).name}",
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
                                    url=f"https://bulbapedia.bulbagarden.net/wiki/{corrected_pokemon.name.basename}_(Pokémon)",
                                )
                            ),
                        ]

                        # Calculating point
                        if point_eligible:
                            total_score = cnt * 10 + (cnt // 10) * 10

                            user_data = await wtp_easy_saves.get(
                                PydanticObjectId(
                                    (
                                        await wtp_easy_saves.find_one(
                                            wtp_easy_saves.user_id
                                            == int(ctx.user.id)
                                        )
                                    ).id
                                )
                            )
                            user_data.points = user_data.points + total_score
                            created_at: int = round(datetime.now().timestamp())
                            if len(user_data.history) == 5:
                                user_data.history.pop(0)
                            user_data.history.append(
                                {
                                    "created_at": created_at,
                                    "streak": cnt,
                                    "gained_point": total_score,
                                }
                            )
                            await user_data.save()

                            await res.ctx.edit_origin(
                                content="".join(
                                    [
                                        "**Who's that Pokemon?**\n\n",
                                        f"It's **{corrected_pokemon.name}**!",
                                        f" {ctx.user.mention} gave up.",
                                        f"\nStreak: {cnt}",
                                        f"\nTotal score: {total_score}",
                                    ],
                                ),
                                components=action_rows,
                                files=_file,
                            )
                            break
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
                                    label=f"{Pokemon.get_pokemon(pokemon_list[i]['name']).name}",
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
                                    url=f"https://bulbapedia.bulbagarden.net/wiki/{corrected_pokemon.name.basename}_(Pokémon)",
                                )
                            ),
                        ]
                        if point_eligible:
                            total_score = cnt * 10 + (cnt // 10) * 10

                            user_data = await wtp_easy_saves.get(
                                PydanticObjectId(
                                    (
                                        await wtp_easy_saves.find_one(
                                            wtp_easy_saves.user_id
                                            == int(ctx.user.id)
                                        )
                                    ).id
                                )
                            )
                            user_data.points = user_data.points + total_score
                            created_at: int = round(datetime.now().timestamp())
                            if len(user_data.history) == 5:
                                user_data.history.pop(0)
                            user_data.history.append(
                                {
                                    "created_at": created_at,
                                    "streak": cnt,
                                    "gained_point": total_score,
                                }
                            )
                            await user_data.save()

                            await res.ctx.edit_origin(
                                content="".join(
                                    [
                                        "**Who's that Pokemon?**\n\n",
                                        f"It's **{corrected_pokemon.name}**!",
                                        f" {ctx.user.mention} had the wrong answer.",
                                        f"\nStreak: {cnt}",
                                        f"\nTotal score: {total_score}",
                                    ],
                                ),
                                components=action_rows,
                                files=_file,
                            )
                            break
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
                                label=f"{Pokemon.get_pokemon(pokemon_list[i]['name']).name}",
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
                                url=f"https://bulbapedia.bulbagarden.net/wiki/{corrected_pokemon.name.basename}_(Pokémon)",
                            )
                        ),
                    ]
                    try:
                        if point_eligible:
                            total_score = cnt * 10 + (cnt // 10) * 10

                            user_data = await wtp_easy_saves.get(
                                PydanticObjectId(
                                    (
                                        await wtp_easy_saves.find_one(
                                            wtp_easy_saves.user_id
                                            == int(ctx.user.id)
                                        )
                                    ).id
                                )
                            )
                            user_data.points = user_data.points + total_score
                            created_at: int = round(datetime.now().timestamp())
                            if len(user_data.history) == 5:
                                user_data.history.pop(0)
                            user_data.history.append(
                                {
                                    "created_at": created_at,
                                    "streak": cnt,
                                    "gained_point": total_score,
                                }
                            )
                            await user_data.save()

                            await msg.edit(
                                content="".join(
                                    [
                                        "**Who's that Pokemon?**\n\n",
                                        "Timeout! ",
                                        f"It's **{corrected_pokemon.name.basename}**!",
                                        f"\nStreak: {cnt}",
                                        f"\nTotal score: {total_score}",
                                    ],
                                ),
                                components=action_rows,
                                files=_file,
                            )
                            return
                        return await msg.edit(
                            content="".join(
                                [
                                    "**Who's that Pokemon?**\n\n",
                                    f"Timeout! It's **{corrected_pokemon.name.basename}**!",
                                    f"\nStreak: {cnt}",
                                ],
                            ),
                            components=action_rows,
                            files=_file,
                        )
                    except interactions.client.errors.NotFound:
                        return

        elif difficulty == "hard":
            cnt = 0

            while True:
                """List of Pokemon."""
                pokemon_list: list = get_pokemon(generation, int(ctx.user.id))

                # Only allow points if generation is not specified
                point_eligible = True
                if generation is not None:
                    point_eligible = False

                if point_eligible:
                    if not await wtp_hard_saves.find_one(
                        wtp_hard_saves.user_id == int(ctx.user.id)
                    ).exists():
                        await wtp_hard_saves(
                            user_id=int(ctx.user.id),
                            user_name=ctx.user.username,
                            points=0,
                            history=[],
                        ).save()

                """The correct Pokemon."""
                corrected_pokemon: Pokemon = Pokemon.get_pokemon(
                    (pokemon_list[random.randint(0, 3)])["name"]
                )

                logging.info("Pokemon list: {}".format(pokemon_list))
                logging.info("Correct Pokemon: {}".format(corrected_pokemon))

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
                    content=f"""**Who's that Pokemon?**\n\n{"Point system enabled (random generation)." if point_eligible else "Point system disabled (specific generation)."}""",
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
                                    url=f"https://bulbapedia.bulbagarden.net/wiki/{corrected_pokemon.name.basename}_(Pokémon)",
                                )
                            ),
                        ]

                        # Calculating point
                        if point_eligible:
                            total_score = cnt * 10 + (cnt // 5) * 10

                            user_data = await wtp_hard_saves.get(
                                PydanticObjectId(
                                    (
                                        await wtp_hard_saves.find_one(
                                            wtp_hard_saves.user_id
                                            == int(ctx.user.id)
                                        )
                                    ).id
                                )
                            )
                            user_data.points = user_data.points + total_score
                            created_at: int = round(datetime.now().timestamp())
                            if len(user_data.history) == 5:
                                user_data.history.pop(0)
                            user_data.history.append(
                                {
                                    "created_at": created_at,
                                    "streak": cnt,
                                    "gained_point": total_score,
                                }
                            )
                            await user_data.save()

                            await res.ctx.edit_origin(
                                content="".join(
                                    [
                                        "**Who's that Pokemon?**\n\n",
                                        f"It's **{corrected_pokemon.name}**!",
                                        f" {ctx.user.mention} gave up.",
                                        f"\nStreak: {cnt}",
                                        f"\nTotal score: {total_score}",
                                    ],
                                ),
                                components=action_rows,
                                files=_file,
                            )
                            break

                        await res.ctx.edit_origin(
                            content="".join(
                                [
                                    "**Who's that Pokemon?**\n\n",
                                    f"It's **{corrected_pokemon.name.basename}**!",
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
                            _res.responses["answer"]
                            .lower()
                            .rstrip()
                            .replace("hisui ", "")
                            .replace("hisuian ", "")
                            == corrected_pokemon.name.basename.lower()
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
                                        f"It's **{corrected_pokemon.name.basename}**! ",
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
                                        url=f"https://bulbapedia.bulbagarden.net/wiki/{corrected_pokemon.name.basename}_(Pokémon)",
                                    )
                                ),
                            ]

                            # Calculating point
                            if point_eligible:
                                total_score = cnt * 10 + (cnt // 5) * 10

                                user_data = await wtp_hard_saves.get(
                                    PydanticObjectId(
                                        (
                                            await wtp_hard_saves.find_one(
                                                wtp_hard_saves.user_id
                                                == int(ctx.user.id)
                                            )
                                        ).id
                                    )
                                )
                                user_data.points = (
                                    user_data.points + total_score
                                )
                                created_at: int = round(
                                    datetime.now().timestamp()
                                )
                                if len(user_data.history) == 5:
                                    user_data.history.pop(0)
                                user_data.history.append(
                                    {
                                        "created_at": created_at,
                                        "streak": cnt,
                                        "gained_point": total_score,
                                    }
                                )
                                await user_data.save()

                                await _res.edit(
                                    message=_res.message_id,
                                    content="".join(
                                        [
                                            "**Who's that Pokemon?**\n\n",
                                            f"It's **{corrected_pokemon.name}**!",
                                            f" {ctx.user.mention} gave up.",
                                            f"\nStreak: {cnt}",
                                            f"\nTotal score: {total_score}",
                                        ],
                                    ),
                                    components=action_rows,
                                    files=_file,
                                )
                                break

                            await _res.edit(
                                message=_res.message_id,
                                content="".join(
                                    [
                                        "**Who's that Pokemon?**\n\n",
                                        f"It's **{corrected_pokemon.name.basename}**!",
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
                                url=f"https://bulbapedia.bulbagarden.net/wiki/{corrected_pokemon.name.basename}_(Pokémon)",
                            ),
                        ),
                    ]

                    try:
                        # Calculating point
                        if point_eligible:
                            total_score = cnt * 10 + (cnt // 5) * 10

                            user_data = await wtp_hard_saves.get(
                                PydanticObjectId(
                                    (
                                        await wtp_hard_saves.find_one(
                                            wtp_hard_saves.user_id
                                            == int(ctx.user.id)
                                        )
                                    ).id
                                )
                            )
                            user_data.points = user_data.points + total_score
                            created_at: int = round(datetime.now().timestamp())
                            if len(user_data.history) == 5:
                                user_data.history.pop(0)
                            user_data.history.append(
                                {
                                    "created_at": created_at,
                                    "streak": cnt,
                                    "gained_point": total_score,
                                }
                            )
                            await user_data.save()

                            await msg.edit(
                                content="".join(
                                    [
                                        "**Who's that Pokemon?**\n\n",
                                        f"It's **{corrected_pokemon.name}**!",
                                        f" {ctx.user.mention} gave up.",
                                        f"\nStreak: {cnt}",
                                        f"\nTotal score: {total_score}",
                                    ],
                                ),
                                components=action_rows,
                                files=_file,
                            )
                            return
                        return await msg.edit(
                            content="".join(
                                [
                                    "**Who's that Pokemon?**\n\nTimeout! ",
                                    f"It's **{corrected_pokemon.name.basename}**!",
                                    f"\nStreak: {cnt}",
                                ],
                            ),
                            components=action_rows,
                            attachments=[],
                            file=_file,
                        )
                    except interactions.client.errors.NotFound:
                        return

    @hybrid_slash_subcommand(
        base="whos_that_pokemon",
        base_description="Who's that Pokemon game.",
        name="leaderboard",
        description="View the Who's that Pokemon game leaderboard.",
    )
    @interactions.slash_option(
        name="mode",
        description="View mode",
        opt_type=interactions.OptionType.STRING,
        choices=[
            interactions.SlashCommandChoice(name="easy", value="easy"),
            interactions.SlashCommandChoice(name="hard", value="hard"),
        ],
        required=True,
    )
    async def wtp_leaderboard(
        self,
        ctx: HybridContext,
        mode: str,
    ) -> None:
        """View the Who's that Pokemon game leaderboard."""

        await ctx.defer()

        embeds = []
        current_embed = None
        i: int = 0
        current_position: int = 0

        leaderboard: list = []
        if mode == "easy":
            leaderboard = (
                await wtp_easy_saves.find_all()
                .sort("-points")
                .to_list()
            )
        elif mode == "hard":
            leaderboard = (
                await wtp_hard_saves.find_all()
                .sort("-points")
                .to_list()
            )
        for position, user in enumerate(leaderboard, start=1):
            value: str = ""
            if user.user_id == int(ctx.user.id):
                current_position = position
                value = f"**{user.user_name} - {user.points} points**"
            else:
                value = f"{user.user_name} - {user.points} points"
            if i % 10 == 0:
                if current_embed:
                    embeds.append(current_embed)
                current_embed = interactions.Embed(color=0x4192C7)

            current_embed.add_field(
                name=f"#{position}",
                value=value,
            )
            i += 1
        if current_embed:
            embeds.append(current_embed)

        paginator = Paginator.create_from_embeds(
            self.client,
            *embeds,
            timeout=60,
        )
        await paginator.send(
            ctx=ctx,
            content=(
                f"You are at top {current_position}."
                if current_position != 0
                else ""
            ),
        )

    @hybrid_slash_subcommand(
        base="whos_that_pokemon",
        base_description="Who's that Pokemon game.",
        name="history",
        description="View your Who's that Pokemon game history.",
    )
    @interactions.slash_option(
        name="mode",
        description="View mode",
        opt_type=interactions.OptionType.STRING,
        choices=[
            interactions.SlashCommandChoice(name="easy", value="easy"),
            interactions.SlashCommandChoice(name="hard", value="hard"),
        ],
        required=True,
    )
    async def wtp_history(
        self,
        ctx: HybridContext,
        mode: str,
    ) -> None:
        """View your Who's that Pokemon game history."""

        await ctx.defer()
        color = await get_response(ctx.user.avatar_url)

        def clamp(x):
            return max(0, min(x, 255))

        color = await get_color(color)
        color = "#{0:02x}{1:02x}{2:02x}".format(
            clamp(color[0]), clamp(color[1]), clamp(color[2])
        )
        color = str("0x" + color[1:])
        color = int(color, 16)

        user_data = None
        if mode == "easy":
            try:
                user_data = await wtp_easy_saves.get(
                    PydanticObjectId(
                        (
                            await wtp_easy_saves.find_one(
                                wtp_easy_saves.user_id == int(ctx.user.id)
                            )
                        ).id
                    )
                )
            except AttributeError:
                embed = interactions.Embed(
                    title="You have no history.",
                    description="You have not played Who's that Pokemon yet.",
                    color=color,
                )
                return await ctx.send(embeds=embed)
        elif mode == "hard":
            try:
                user_data = await wtp_hard_saves.get(
                    PydanticObjectId(
                        (
                            await wtp_hard_saves.find_one(
                                wtp_hard_saves.user_id == int(ctx.user.id)
                            )
                        ).id
                    )
                )
            except AttributeError:
                embed = interactions.Embed(
                    title="You have no history.",
                    description="You have not played Who's that Pokemon yet.",
                    color=color,
                )
                return await ctx.send(embeds=embed)

        fields = []
        for index, history in enumerate(reversed(list(user_data.history))):
            fields.append(
                interactions.EmbedField(
                    name=f"#{index+1}",
                    value="".join(
                        [
                            f"""<t:{history["created_at"]}:f> UTC\n""",
                            f"""Streak: {history["streak"]}\n""",
                            f"""Gained {history["gained_point"]} point""",
                        ]
                    ),
                )
            )
        embed = interactions.Embed(
            title=f"Your score is {user_data.points}.",
            color=color,
            fields=fields,
            thumbnail=interactions.EmbedAttachment(
                url=ctx.user.avatar_url,
            ),
        )

        await ctx.send(embeds=embed)


def setup(client) -> None:
    """Setup the extension."""
    WTP(client)
    logging.info("Loaded WTP extension.")
