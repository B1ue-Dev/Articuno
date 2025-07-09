"""
Hangman command.

(C) 2023 - B1ue-Dev
"""

import logging
import asyncio
from datetime import datetime
from typing import List
from unicodedata import normalize
from beanie import PydanticObjectId
import interactions
from interactions.ext.paginators import Paginator
from interactions.ext.hybrid_commands import (
    HybridContext,
    hybrid_slash_subcommand,
)
from src.exts.core.info import get_color
from src.common.utils import get_response, hangman_saves


def display_hangman(tries):
    stages = [  # final state: head, torso, both arms, and both legs
        """
    --------
    |      |
    |      O
    |     \\|/
    |      |
    |     / \\
    -
""",
        # head, torso, both arms, and one leg
        """
    --------
    |      |
    |      O
    |     \\|/
    |      |
    |     /
    -
""",
        # head, torso, and both arms
        """
    --------
    |      |
    |      O
    |     \\|/
    |      |
    |
    -
""",
        # head, torso, and one arm
        """
    --------
    |      |
    |      O
    |     \\|
    |      |
    |
    -
""",
        # head and torso
        """
    --------
    |      |
    |      O
    |      |
    |      |
    |
    -
""",
        # head
        """
    --------
    |      |
    |      O
    |
    |
    |
    -
""",
        # initial empty state
        """
    --------
    |      |
    |
    |
    |
    |
    -
""",
    ]
    return stages[tries]


async def get_word() -> str:
    """Get a word from the API."""

    resp: dict = await get_response(
        url="https://random-words-api-b1uedev.vercel.app/word"
    )
    return (resp[0]["word"], resp[0]["definition"])


class Hman(interactions.Extension):
    """Extension for hangman command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @hybrid_slash_subcommand(
        base="hangman",
        base_description="Hangman game.",
        name="play",
        description="Plays a game of hangman",
    )
    async def hangman_play(self, ctx: HybridContext) -> None:
        """Plays a game of hangman."""

        await ctx.defer()

        resp: dict = await get_word()
        correct_word: str = normalize(
            "NFKD", resp[0].encode("ASCII", "ignore").decode("ASCII")
        ).lower()
        definition: str = resp[1]
        word_completion: str = str("_" * len(correct_word))
        guessed: bool = False
        guessed_letters: list = []
        guessed_words: list = []
        tries: int = 6
        print(correct_word)

        button: List[interactions.Button] = [  # noqa: F821
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

        over_button: List[interactions.Button] = [
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="Answer",
                custom_id="answer",
                disabled=True,
            ),
        ]

        embed = interactions.Embed(
            title=f"{ctx.user.username} hangman game.",
            color=0x7CB7D3,
        )
        embed.add_field(
            name=f"Word ({len(word_completion)} characters): `{word_completion}`",
            value=f"""```\n{display_hangman(tries)}\n```""",
        )

        if not await hangman_saves.find_one(
            hangman_saves.user_id == int(ctx.user.id)
        ).exists():
            await hangman_saves(
                user_id=int(ctx.user.id),
                user_name=ctx.user.username,
                highest_point=0,
                history=[],
            ).save()

        msg = await ctx.send(embed=embed, components=button)

        # Loop through for each guess until
        # tries is 0.
        while not guessed and tries > 0:
            try:

                def _check(_ctx):
                    return int(_ctx.ctx.user.id) == int(ctx.user.id)

                res = await self.client.wait_for_component(
                    components=button,
                    check=_check,
                    messages=int(msg.id),
                    timeout=30,
                )

                modal = interactions.Modal(
                    title=f"{ctx.user.username} hangman game.",
                    custom_id=f"hangman_{str(ctx.user.id)}",
                )
                modal.add_components(
                    interactions.InputText(
                        label="Your guess",
                        style=interactions.TextStyles.SHORT,
                        placeholder="Guess a character or a word ⚠ (Do not hit Cancel)",
                        custom_id="answer",
                        max_length=100,
                    ),
                )

                # If the user gives up, set tries
                # to 0, disable the components and
                # show the word.
                if res.ctx.custom_id == "give_up":
                    tries: int = 0

                    embed = interactions.Embed(
                        title=f"{ctx.user.username} hangman game.",
                        color=0x7CB7D3,
                    )
                    embed.add_field(
                        name=f"Word ({len(correct_word)} characters): `{correct_word}`",
                        value=f"""```\n{display_hangman(tries)}\n```""",
                    )
                    return await res.ctx.edit_origin(
                        embed=embed, components=over_button
                    )

                # If the user answer, decrease tries 1
                # and process the guessed word/character.
                else:
                    await res.ctx.send_modal(modal)

                    def _check(_ctx):
                        return int(_ctx.ctx.user.id) == int(ctx.user.id)

                    _res = await self.client.wait_for_modal(
                        modal=modal,
                        author=ctx.author,
                        timeout=15,
                    )

                    ans = _res.responses["answer"].lower().rstrip()

                    if len(ans) == 1 and ans.isalpha():
                        if ans in guessed_letters:
                            embed.description = (
                                f"You already guessed the character {ans}."
                            )
                            embed.set_footer(
                                text="\n".join(
                                    [
                                        "Guessed letters: "
                                        + ", ".join(guessed_letters),
                                        "Guessed words: "
                                        + ", ".join(guessed_words),
                                    ]
                                )
                            )
                            await _res.edit(
                                message=_res.message_id, embed=embed
                            )
                        elif ans not in correct_word:
                            tries -= 1
                            if tries == 0:
                                await _res.edit(message=_res.message_id)
                                break
                            guessed_letters.append(ans)
                            embed.description = f"{ans} is not in the word."
                            embed.fields = []
                            embed.add_field(
                                name=f"Word ({len(word_completion)} characters): `{word_completion}`",
                                value=f"""```\n{display_hangman(tries)}\n```""",
                            )
                            embed.set_footer(
                                text="\n".join(
                                    [
                                        "Guessed letters: "
                                        + ", ".join(guessed_letters),
                                        "Guessed words: "
                                        + ", ".join(guessed_words),
                                    ]
                                )
                            )
                            await _res.edit(
                                message=_res.message_id, embed=embed
                            )
                        else:
                            guessed_letters.append(ans)
                            word_as_list = list(word_completion)
                            indices = [
                                i
                                for i, letter in enumerate(correct_word)
                                if letter == ans
                            ]
                            for index in indices:
                                word_as_list[index] = ans
                            word_completion = "".join(word_as_list)
                            if "_" not in word_completion:
                                guessed = True
                                word_completion = ans
                                gained_point: int = (10 + tries) * (
                                    2 if tries > 3 else 1
                                )
                                print(gained_point)

                                user_data = await hangman_saves.get(
                                    PydanticObjectId(
                                        (
                                            await hangman_saves.find_one(
                                                hangman_saves.user_id
                                                == int(ctx.user.id)
                                            )
                                        ).id
                                    )
                                )
                                user_data.highest_point = (
                                    user_data.highest_point + gained_point
                                )
                                created_at: int = round(
                                    datetime.now().timestamp()
                                )
                                if len(user_data.history) == 5:
                                    user_data.history.pop(0)
                                user_data.history.append(
                                    {
                                        "created_at": created_at,
                                        "word": correct_word,
                                        "tries": 6 - tries,
                                        "gained_point": gained_point,
                                    }
                                )
                                await user_data.save()

                                embed = interactions.Embed(
                                    title=f"{ctx.user.username} hangman game.",
                                    description="".join(
                                        [
                                            f"Congrats! The word is `{correct_word}`.\nDefinition: {definition}\n",
                                            f"You get {gained_point} points. Your total point is {user_data.highest_point}",
                                        ]
                                    ),
                                    color=0x7CB7D3,
                                )
                                embed.add_field(
                                    name="\u200b",
                                    value=f"""```\n{display_hangman(tries)}\n```""",
                                )

                                return await _res.edit(
                                    message=_res.message_id,
                                    embed=embed,
                                    components=over_button,
                                )

                            embed.description = (
                                f"Good job! {ans} is in the word."
                            )
                            embed.fields = []
                            embed.add_field(
                                name=f"Word ({len(word_completion)} characters): `{word_completion}`",
                                value=f"""```\n{display_hangman(tries)}\n```""",
                            )
                            embed.set_footer(
                                text="\n".join(
                                    [
                                        "Guessed letters: "
                                        + ", ".join(guessed_letters),
                                        "Guessed words: "
                                        + ", ".join(guessed_words),
                                    ]
                                )
                            )
                            await _res.edit(
                                message=_res.message_id, embed=embed
                            )

                    elif len(ans) == len(ans) and ans.isalpha():
                        if ans in guessed_words:
                            embed.description = (
                                f"You already guessed the word {ans}."
                            )
                            embed.set_footer(
                                text="\n".join(
                                    [
                                        "Guessed letters: "
                                        + ", ".join(guessed_letters),
                                        "Guessed words: "
                                        + ", ".join(guessed_words),
                                    ]
                                )
                            )
                            await _res.edit(
                                message=_res.message_id, embed=embed
                            )
                        elif ans != correct_word:
                            tries -= 1
                            if tries == 0:
                                await _res.edit(message=_res.message_id)
                                break
                            guessed_words.append(ans)
                            embed.description = (
                                f"{ans} is not the corrected word."
                            )
                            embed.fields = []
                            embed.add_field(
                                name=f"Word ({len(word_completion)} characters): `{word_completion}`",
                                value=f"""```\n{display_hangman(tries)}\n```""",
                            )
                            embed.set_footer(
                                text="\n".join(
                                    [
                                        "Guessed letters: "
                                        + ", ".join(guessed_letters),
                                        "Guessed words: "
                                        + ", ".join(guessed_words),
                                    ]
                                )
                            )
                            await _res.edit(
                                message=_res.message_id, embed=embed
                            )
                        else:
                            guessed = True
                            word_completion = ans
                            gained_point: int = (10 + tries) * (
                                2 if tries > 3 else 1
                            )
                            print(gained_point)

                            user_data = await hangman_saves.get(
                                PydanticObjectId(
                                    (
                                        await hangman_saves.find_one(
                                            hangman_saves.user_id
                                            == int(ctx.user.id)
                                        )
                                    ).id
                                )
                            )
                            user_data.highest_point = (
                                user_data.highest_point + gained_point
                            )
                            created_at: int = round(datetime.now().timestamp())
                            if len(user_data.history) == 5:
                                user_data.history.pop(0)
                            user_data.history.append(
                                {
                                    "created_at": created_at,
                                    "word": correct_word,
                                    "tries": 6 - tries,
                                    "gained_point": gained_point,
                                }
                            )
                            await user_data.save()

                            embed = interactions.Embed(
                                title=f"{ctx.user.username} hangman game.",
                                description="".join(
                                    [
                                        f"Congrats! The word is `{correct_word}`.\nDefinition: {definition}\n",
                                        f"You get {gained_point} points. Your total point is {user_data.highest_point}",
                                    ]
                                ),
                                color=0x7CB7D3,
                            )
                            embed.add_field(
                                name="\u200b",
                                value=f"""```\n{display_hangman(tries)}\n```""",
                            )

                            return await _res.edit(
                                message=_res.message_id,
                                embed=embed,
                                components=over_button,
                            )

                    else:
                        tries -= 1
                        if tries == 0:
                            await _res.edit(message=_res.message_id)
                            break
                        guessed_words.append(ans)
                        embed.description = f"{ans} is not a valid guess."
                        embed.fields = []
                        embed.add_field(
                            name=f"Word ({len(word_completion)} characters): `{word_completion}`",
                            value=f"""```\n{display_hangman(tries)}\n```""",
                        )
                        embed.set_footer(
                            text="\n".join(
                                [
                                    "Guessed letters: "
                                    + ", ".join(guessed_letters),
                                    "Guessed words: "
                                    + ", ".join(guessed_words),
                                ]
                            )
                        )
                        await _res.edit(message=_res.message_id, embed=embed)

            except asyncio.TimeoutError:
                user_data = await hangman_saves.get(
                    PydanticObjectId(
                        (
                            await hangman_saves.find_one(
                                hangman_saves.user_id == int(ctx.user.id)
                            )
                        ).id
                    )
                )
                created_at: int = round(datetime.now().timestamp())
                if len(user_data.history) == 5:
                    user_data.history.pop(0)
                user_data.history.append(
                    {
                        "created_at": created_at,
                        "word": correct_word,
                        "tries": 6 - tries,
                        "gained_point": 0,
                    }
                )
                await user_data.save()

                embed = interactions.Embed(
                    title=f"{ctx.user.username} hangman game.",
                    description="".join(
                        [
                            f"Time out! The word is `{correct_word}`.\nDefinition: {definition}\n",
                            f"You get 0 point. Your total point is {user_data.highest_point}",
                        ]
                    ),
                    color=0x7CB7D3,
                )
                embed.add_field(
                    name="\u200b",
                    value=f"""```\n{display_hangman(tries)}\n```""",
                )
                try:
                    return await msg.edit(embed=embed, components=over_button)
                except interactions.client.errors.NotFound:
                    return

        if guessed is False:
            user_data = await hangman_saves.get(
                PydanticObjectId(
                    (
                        await hangman_saves.find_one(
                            hangman_saves.user_id == int(ctx.user.id)
                        )
                    ).id
                )
            )
            created_at: int = round(datetime.now().timestamp())
            if len(user_data.history) == 5:
                user_data.history.pop(0)
            user_data.history.append(
                {
                    "created_at": created_at,
                    "word": correct_word,
                    "tries": 6 - tries,
                    "gained_point": 0,
                }
            )
            await user_data.save()

            embed = interactions.Embed(
                title=f"{ctx.user.username} hangman game.",
                description="".join(
                    [
                        f"Sorry, you ran out of tries. The word is `{correct_word}`.\nDefinition: {definition}",
                        f"\nYou get 0 point. Your total point is {user_data.highest_point}",
                    ]
                ),
                color=0x7CB7D3,
            )
            embed.add_field(
                name="\u200b",
                value=f"""```\n{display_hangman(tries)}\n```""",
            )
            await msg.edit(embed=embed, components=over_button)

    @hybrid_slash_subcommand(
        base="hangman",
        base_description="Hangman game.",
        name="history",
        description="Shows your history",
    )
    async def hangman_history(self, ctx: HybridContext) -> None:
        """Shows your history."""

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
        user_data = await hangman_saves.get(
            PydanticObjectId(
                (
                    await hangman_saves.find_one(
                        hangman_saves.user_id == int(ctx.user.id)
                    )
                ).id
            )
        )

        fields = []
        for index, history in enumerate(reversed(list(user_data.history))):
            fields.append(
                interactions.EmbedField(
                    name=f"#{index+1}",
                    value="".join(
                        [
                            f"""<t:{history["created_at"]}:f> UTC\n""",
                            f"""Word: {history["word"]}\n""",
                            f"""Total tries: {history["tries"]}\n""",
                            f"""Gained {history["gained_point"]} point""",
                        ]
                    ),
                )
            )
        embed = interactions.Embed(
            title=f"Your highest score is {user_data.highest_point}.",
            color=color,
            fields=fields,
            thumbnail=interactions.EmbedAttachment(
                url=ctx.user.avatar_url,
            ),
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_subcommand(
        base="hangman",
        base_description="Hangman game.",
        name="leaderboard",
        description="Shows the top leaderboard.",
    )
    async def hangman_leaderboard(self, ctx: HybridContext) -> None:
        """Shows the top leaderboard."""

        await ctx.defer()

        embeds = []
        current_embed = None
        i: int = 0
        current_position: int = 0

        leaderboard = (
            await hangman_saves.find_all().sort("-highest_point").to_list()
        )
        for position, user in enumerate(leaderboard, start=1):
            value: str = ""
            if user.user_id == int(ctx.user.id):
                current_position = position
                value = f"**{user.user_name} - {user.highest_point} points**"
            else:
                value = f"{user.user_name} - {user.highest_point} points"
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


def setup(client) -> None:
    """Setup the extension."""
    Hman(client)
    logging.info("Loaded Hangman extension.")
