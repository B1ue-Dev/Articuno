"""
Hangman command.

(C) 2023 - B1ue-Dev
"""

import logging
import asyncio
from unicodedata import normalize
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
from src.utils.utils import get_response


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

    resp = await get_response(url="https://random-words-api.vercel.app/word")
    return (resp[0]["word"], resp[0]["definition"])


class Hangman(interactions.Extension):
    """Extension for hangman command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @hybrid_slash_command(
        name="hangman",
        description="Plays a game of hangman.",
    )
    async def hangman(self, ctx: HybridContext) -> None:
        """Plays a game of hangman."""

        await ctx.defer()

        resp = await get_word()
        correct_word: str = normalize(
            "NFKD", resp[0].encode("ASCII", "ignore").decode("ASCII")
        )
        definition: str = resp[1]
        word_completion: str = str("_" * len(correct_word))
        guessed: bool = False
        guessed_letters: list = []
        guessed_words: list = []
        tries: int = 6

        button: list(button) = [  # noqa: F821
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

        over_button: list(button) = [
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
                            embed.description = (
                                f"Good job! {ans} is in the word."
                            )
                            embed.fields = []
                            embed.add_field(
                                name=f"Word ({len(word_completion)} characters): `{word_completion}`",
                                value=f"""```\n{display_hangman(tries)}\n```""",
                            )
                            await _res.edit(
                                message=_res.message_id, embed=embed
                            )

                    elif len(ans) == len(ans) and ans.isalpha():
                        if ans in guessed_words:
                            embed.description = (
                                f"You already guessed the word {ans}."
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
                            await _res.edit(
                                message=_res.message_id, embed=embed
                            )
                        else:
                            guessed = True
                            word_completion = ans
                            embed = interactions.Embed(
                                title=f"{ctx.user.username} hangman game.",
                                description=f"Congrats! The word is `{correct_word}`.\nDefinition: {definition}",
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
                        await _res.edit(message=_res.message_id, embed=embed)

            except asyncio.TimeoutError:
                embed = interactions.Embed(
                    title=f"{ctx.user.username} hangman game.",
                    description=f"Time out! The word is `{correct_word}`.\nDefinition: {definition}",
                    color=0x7CB7D3,
                )
                embed.add_field(
                    name="\u200b",
                    value=f"""```\n{display_hangman(tries)}\n```""",
                )
                return await msg.edit(embed=embed, components=over_button)

        if guessed is False:
            embed = interactions.Embed(
                title=f"{ctx.user.username} hangman game.",
                description=f"Sorry, you ran out of tries. The word is `{correct_word}`.\nDefinition: {definition}",
                color=0x7CB7D3,
            )
            embed.add_field(
                name="\u200b",
                value=f"""```\n{display_hangman(tries)}\n```""",
            )
            await msg.edit(embed=embed, components=over_button)


def setup(client) -> None:
    """Setup the extension."""
    Hangman(client)
    logging.info("Loaded Hangman extension.")
