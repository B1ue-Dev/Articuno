"""
Who's that Pokemon command.

(C) 2022-2026 - B1ue-Dev
"""

import logging
import io
import random
import asyncio
from time import time
from datetime import datetime
import interactions
from interactions.ext.paginators import Paginator
from interactions.ext.hybrid_commands import (
    hybrid_slash_subcommand,
    HybridContext,
)
from PIL import Image
from src.exts.fun.pokemon import Pokemon
from src.common.utils import get_response, get_color, rgb_to_int
from src.common.models import wtp_easy_saves, wtp_hard_saves


bg = Image.open("./src/assets/whos_that_pokemon_1_optimized.webp")


def _resize_pokemon_image(buf) -> Image.Image:
    """Resize the original Pokemon image to suit the background."""

    img = Image.open(buf).convert("RGBA")
    print(f"Image size: {img.size}")
    if img.size[1] <= 130:
        img = img.resize((int(img.width * 3.9), int(img.height * 3.9)))
    elif img.size[1] <= 160:
        img = img.resize((int(img.width * 3.4), int(img.height * 3.4)))
    elif img.size[1] <= 190:
        img = img.resize((int(img.width * 2.7), int(img.height * 2.7)))
    elif img.size[1] <= 235:
        img = img.resize((int(img.width * 2.35), int(img.height * 2.35)))
    else:
        img = img.resize((int(img.width * 2), int(img.height * 2)))

    return img


def _generate_image(img: Image, correct_pokemon: Pokemon) -> list[interactions.File]:
    """Generate the background with the Pokemon."""

    # Process the image and background.
    _black_image = Image.new("RGBA", img.size, (0, 0, 0))
    center_x, center_y = 470, 410
    paste_x = center_x - img.width // 2
    paste_y = center_y - img.height // 2
    paste_pos = (paste_x, paste_y)

    text_img = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    text_img.paste(bg, (0, 0))
    text_img.paste(_black_image, paste_pos, img)

    # Image for the user guessing the Pokemon.
    out1 = io.BytesIO()
    text_img.save(out1, format="PNG")
    out1.seek(0)
    file = interactions.File(
        file_name="image.png",
        file=out1,
        description="Guess the Pokemon.",
    )

    # Image for the correct Pokemon.
    _text_img = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    _text_img.paste(bg, (0, 0))
    _text_img.paste(img, paste_pos, img)

    out2 = io.BytesIO()
    _text_img.save(out2, format="PNG")
    out2.seek(0)
    _file = interactions.File(
        file_name="image.png",
        file=out2,
        description=f"{correct_pokemon.name}",
    )

    return [file, _file]


async def extract_pokemon_image(url: str, session) -> Image.Image:
    """
    Gets the Pokemon image after resize.
    :param url: The url of the Pokemon image.
    :type url: str
    :param session: The client session.
    :type session: ClientSession
    :return: The Image of resized Pokemon.
    :rtype: Image
    """

    buf = await get_response(url, session)
    img = await asyncio.to_thread(_resize_pokemon_image, buf)

    return img


async def generate_images(correct_pokemon: Pokemon, session) -> list[interactions.File]:
    """
    Generate the background with the Pokemon for the command.
    :param correct_pokemon: The correct Pokemon.
    :type correct_pokemon: Pokemon
    :param session: The client session.
    :type session: ClientSession
    :return: A list 2 File, guessing image and correct image.
    :rtype: list[interactions.File]
    """

    _image = await extract_pokemon_image(correct_pokemon.url, session)
    return await asyncio.to_thread(_generate_image, _image, correct_pokemon)


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


def _choice_buttons(pokemon_list: list) -> list[interactions.Button]:
    """
    Build the 4 answer-choice buttons with a give up button (easy mode)
    :param pokemon_list: A list of Pokemon
    :type pokemon_list: list
    :return: List of Button for selection
    :rtype: list[interactions.Button]
    """

    buttons = [
        interactions.Button(
            style=interactions.ButtonStyle.SECONDARY,
            label=Pokemon.get_pokemon(entry["name"]).name,
            custom_id=str(entry["num"]),
        )
        for entry in pokemon_list
    ]
    buttons.append(
        interactions.Button(
            style=interactions.ButtonStyle.DANGER,
            label="Give up",
            custom_id="give_up",
        )
    )
    return buttons


def _result_buttons(
    pokemon_list: list,
    correct_pokemon: Pokemon,
    chosen_id: str = None,
    if_chosen: bool = True,
) -> list[interactions.Button]:
    """Build the 4 disabled answer buttons showing a round's result (easy mode).

    :param pokemon_list: The 4 pokemon choices for this round.
    :type pokemon_list: list
    :param correct_pokemon: The correct Pokemon.
    :type correct_pokemon: Pokemon
    :param chosen_id: The custom_id that the user picked (None on timeout/no pick).
    :type chosen_id: str
    :param if_chosen: Whenever to highlight the button (if chosen) or not (timeout/give up)
    :type if_chosen: bool
    :return: List of disabled Button
    :rtype: list[interactions.Button]
    """

    buttons = []
    for entry in pokemon_list:
        num = str(entry["num"])
        label = Pokemon.get_pokemon(entry["name"]).name

        if not if_chosen:
            style = interactions.ButtonStyle.SECONDARY
        elif num == str(correct_pokemon.num):
            style = interactions.ButtonStyle.SUCCESS
        elif chosen_id is not None and num == str(chosen_id):
            style = interactions.ButtonStyle.DANGER
        else:
            style = interactions.ButtonStyle.SECONDARY

        buttons.append(
            interactions.Button(
                style=style,
                label=label,
                custom_id=num,
                disabled=True,
            )
        )
    return buttons


def _bulbapedia_button(pokemon: Pokemon) -> interactions.Button:
    """Build the 'View on Bulbapedia' link button for a Pokemon."""

    return interactions.Button(
        style=interactions.ButtonStyle.LINK,
        label=f"{pokemon.name} (Bulbapedia)",
        url=f"https://bulbapedia.bulbagarden.net/wiki/{pokemon.name.basename}_(Pokémon)",
    )


def _hard_mode_result(
    corrected_pokemon: Pokemon,
) -> list[interactions.ActionRow]:
    """Build the disabled 'Answer' button + Bulbapedia link row (hard mode)."""

    return [
        interactions.ActionRow(
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="Answer",
                custom_id="answer",
                disabled=True,
            ),
        ),
        interactions.ActionRow(_bulbapedia_button(corrected_pokemon)),
    ]


async def _fetch_save_doc(save_model, user_id: int, user_name: str):
    """Fetch the user's save document, creating it if it doesn't exist yet.

    Replaces the old "exists() query, then a separate find_one() query
    later when saving" pattern with a single fetch that's reused for the
    whole game session.
    """

    user_data = await save_model.find_one(save_model.user_id == user_id)
    if user_data is None:
        user_data = save_model(
            user_id=user_id,
            user_name=user_name,
            points=0,
            history=[],
        )
        await user_data.save()
    return user_data


async def _save_score(user_data, cnt: int, divisor: int = 10) -> int:
    """Add points/history for a finished round onto an already-fetched save doc.

    :param user_data: The user's save document (wtp_easy_saves / wtp_hard_saves instance).
    :param cnt: Current streak count.
    :param divisor: Streak bonus divisor (10 for easy mode, 5 for hard mode).
    :return: The score gained this round.
    """

    total_score = cnt * 10 + (cnt // divisor) * 10

    user_data.points += total_score
    if len(user_data.history) == 5:
        user_data.history.pop(0)
    user_data.history.append(
        {
            "created_at": round(datetime.now().timestamp()),
            "streak": cnt,
            "gained_point": total_score,
        }
    )
    await user_data.save()

    return total_score


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

            point_eligible = generation is None

            save_doc = None
            if point_eligible:
                save_doc = await _fetch_save_doc(
                    wtp_easy_saves, int(ctx.user.id), ctx.user.username
                )

            while True:
                """List of Pokemon."""
                pokemon_list: list = get_pokemon(generation, int(ctx.user.id))

                """The correct Pokemon."""
                corrected_pokemon: Pokemon = Pokemon.get_pokemon(
                    (pokemon_list[random.randint(0, 3)])["name"]
                )
                logging.info("Pokemon list: {}".format(pokemon_list))
                logging.info("Correct Pokemon: {}".format(corrected_pokemon))

                results = await generate_images(corrected_pokemon, self.client.session)
                file = results[0]
                _file = results[1]

                _button_list = _choice_buttons(pokemon_list)

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
                        _button_disabled = _result_buttons(
                            pokemon_list,
                            corrected_pokemon,
                            chosen_id=corrected_pokemon.num
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
                        _button_disabled = _result_buttons(
                            pokemon_list,
                            corrected_pokemon,
                            chosen_id=res.ctx.custom_id
                        )

                        action_rows: list[interactions.ActionRow] = [
                            interactions.ActionRow(*_button_disabled),
                            interactions.ActionRow(
                                _bulbapedia_button(corrected_pokemon)
                            ),
                        ]

                        # Calculating point
                        if point_eligible:
                            total_score = await _save_score(save_doc, cnt, divisor=10)

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
                        _button_disabled = _result_buttons(
                            pokemon_list,
                            corrected_pokemon,
                            chosen_id=res.ctx.custom_id
                        )

                        action_rows: list[interactions.ActionRow] = [
                            interactions.ActionRow(*_button_disabled),
                            interactions.ActionRow(
                                _bulbapedia_button(corrected_pokemon)
                            ),
                        ]
                        if point_eligible:
                            total_score = await _save_score(save_doc, cnt, divisor=10)

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
                    _button_disabled = _result_buttons(
                        pokemon_list, corrected_pokemon, if_chosen=False
                    )

                    action_rows: list[interactions.ActionRow] = [
                        interactions.ActionRow(*_button_disabled),
                        interactions.ActionRow(
                            _bulbapedia_button(corrected_pokemon)
                        ),
                    ]
                    try:
                        if point_eligible:
                            total_score = await _save_score(save_doc, cnt, divisor=10)

                            await msg.edit(
                                content="".join(
                                    [
                                        "**Who's that Pokemon?**\n\n",
                                        "Timeout! ",
                                        f"It's **{corrected_pokemon.name}**!",
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
                                    f"Timeout! It's **{corrected_pokemon.name}**!",
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

            point_eligible = generation is None

            save_doc = None
            if point_eligible:
                save_doc = await _fetch_save_doc(
                    wtp_hard_saves, int(ctx.user.id), ctx.user.username
                )

            while True:
                """List of Pokemon."""
                pokemon_list: list = get_pokemon(generation, int(ctx.user.id))

                """The correct Pokemon."""
                corrected_pokemon: Pokemon = Pokemon.get_pokemon(
                    (pokemon_list[random.randint(0, 3)])["name"]
                )

                logging.info("Pokemon list: {}".format(pokemon_list))
                logging.info("Correct Pokemon: {}".format(corrected_pokemon))

                results = await generate_images(corrected_pokemon, self.client.session)
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
                        action_rows = _hard_mode_result(corrected_pokemon)

                        # Calculating point
                        if point_eligible:
                            total_score = await _save_score(save_doc, cnt, divisor=5)

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
                            action_rows = _hard_mode_result(corrected_pokemon)

                            # Calculating point
                            if point_eligible:
                                total_score = await _save_score(save_doc, cnt, divisor=5)

                                await _res.edit(
                                    message=_res.message_id,
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
                    action_rows = _hard_mode_result(corrected_pokemon)

                    try:
                        if point_eligible:
                            total_score = await _save_score(save_doc, cnt, divisor=5)

                            await msg.edit(
                                content="".join(
                                    [
                                        "**Who's that Pokemon?**\n\n",
                                        f"**Timeout!** It's **{corrected_pokemon.name}**!",
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
                                    f"**Timeout!** It's **{corrected_pokemon.name}**!",
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

        buf = await get_response(ctx.user.avatar_url, session=self.client.session)
        color_tuple = await asyncio.to_thread(get_color, buf)
        color = rgb_to_int(color_tuple)

        user_data = None
        if mode == "easy":
            user_data = await wtp_easy_saves.find_one(
                wtp_easy_saves.user_id == int(ctx.user.id)
            )
        elif mode == "hard":
            user_data = await wtp_hard_saves.find_one(
                wtp_hard_saves.user_id == int(ctx.user.id)
            )

        if user_data is None:
            embed = interactions.Embed(
                title="You have no history",
                description="You have not played Who's that Pokemon yet.",
                color=color,
            )
            return await ctx.send(embed=embed)

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
