"""
Trivia command.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import asyncio
import base64 as b64
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
from utils.utils import get_response


class Trivia(interactions.Extension):
    """Extension for /trivia."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    async def get_question(self, category: str, difficulty: str) -> list:
        """Get a list of 50 questions."""

        url = "https://opentdb.com/api.php"
        params = {
            "amount": "10",
            "type": "boolean",
            "encode": "base64",
            "category": category,
            "difficulty": difficulty,
        }
        resp = await get_response(url=url, params=params)

        return resp

    @hybrid_slash_command(
        name="trivia",
        description="Play a game of trivia.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="category",
                description="The category you want to play",
                choices=[
                    interactions.SlashCommandChoice(
                        name="general",
                        value="general",
                    ),
                    interactions.SlashCommandChoice(
                        name="book",
                        value="book",
                    ),
                    interactions.SlashCommandChoice(
                        name="film",
                        value="film",
                    ),
                    interactions.SlashCommandChoice(
                        name="music",
                        value="music",
                    ),
                    interactions.SlashCommandChoice(
                        name="theatres",
                        value="theatres",
                    ),
                    interactions.SlashCommandChoice(
                        name="television",
                        value="television",
                    ),
                    interactions.SlashCommandChoice(
                        name="games",
                        value="games",
                    ),
                    interactions.SlashCommandChoice(
                        name="nature",
                        value="nature",
                    ),
                    interactions.SlashCommandChoice(
                        name="computers",
                        value="computers",
                    ),
                    interactions.SlashCommandChoice(
                        name="sports", value="sports"
                    ),
                    interactions.SlashCommandChoice(
                        name="geography",
                        value="geography",
                    ),
                    interactions.SlashCommandChoice(
                        name="history",
                        value="history",
                    ),
                    interactions.SlashCommandChoice(
                        name="animal",
                        value="animal",
                    ),
                    interactions.SlashCommandChoice(
                        name="vehicles",
                        value="vehicles",
                    ),
                    interactions.SlashCommandChoice(
                        name="comics",
                        value="comics",
                    ),
                    interactions.SlashCommandChoice(
                        name="anime",
                        value="anime",
                    ),
                    interactions.SlashCommandChoice(
                        name="cartoons",
                        value="cartoons",
                    ),
                ],
                required=True,
            ),
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="difficulty",
                description="The difficulty level",
                choices=[
                    interactions.SlashCommandChoice(
                        name="easy",
                        value="easy",
                    ),
                    interactions.SlashCommandChoice(
                        name="medium",
                        value="medium",
                    ),
                    interactions.SlashCommandChoice(
                        name="hard",
                        value="hard",
                    ),
                ],
                required=True,
            ),
        ],
    )
    @interactions.cooldown(interactions.Buckets.USER, 1, 10)
    async def trivia(
        self,
        ctx: HybridContext,
        category: str,
        difficulty: str,
    ):
        """Plays a game of trivia."""

        value_convert: dict = {
            "general": 9,
            "book": 10,
            "film": 11,
            "music": 12,
            "theatres": 13,
            "television": 14,
            "games": 15,
            "nature": 17,
            "computers": 18,
            "sports": 21,
            "geography": 22,
            "history": 23,
            "animal": 27,
            "vehicles": 28,
            "comics": 29,
            "anime": 31,
            "cartoons": 32,
        }

        _msg = await ctx.send(content="Getting question...")

        buttons = [
            interactions.Button(
                style=interactions.ButtonStyle.SUCCESS,
                label="True",
                custom_id="true",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.DANGER,
                label="False",
                custom_id="false",
            ),
        ]

        cnt, i = 0, 0
        _selected_category: str = value_convert[category]
        _selected_difficulty: str = difficulty
        resp = await Trivia.get_question(
            self, _selected_category, _selected_difficulty
        )

        while True:
            if i != 9:
                pass
            else:
                i = 0
                resp = await Trivia.get_question(
                    self, _selected_category, _selected_difficulty
                )

            _category = b64.b64decode(resp["results"][i]["category"])
            category = _category.decode("utf-8")
            _question = b64.b64decode(resp["results"][i]["question"])
            question = _question.decode("utf-8")
            _correct_answer = b64.b64decode(
                resp["results"][i]["correct_answer"]
            )
            correct_answer = _correct_answer.decode("utf-8")
            embed = interactions.Embed(
                title="Trivia",
                description=f"**{category}**: {question}",
                author=interactions.EmbedAuthor(
                    name=f"{ctx.user.username}#{ctx.user.discriminator}",
                    icon_url=ctx.user.avatar_url,
                ),
            )
            msg = await _msg.edit(content="", embeds=embed, components=buttons)

            embed_ed = interactions.Embed(
                title="Trivia",
                description=f"**{category}**: {question}",
                author=interactions.EmbedAuthor(
                    name=f"{ctx.user.username}#{ctx.user.discriminator}",
                    icon_url=ctx.user.avatar.url,
                ),
            )
            buttons_disabled = [
                interactions.Button(
                    style=interactions.ButtonStyle.SUCCESS,
                    label="True",
                    custom_id="true",
                    disabled=True,
                ),
                interactions.Button(
                    style=interactions.ButtonStyle.DANGER,
                    label="False",
                    custom_id="false",
                    disabled=True,
                ),
            ]

            try:

                def _check(_ctx):
                    return int(_ctx.ctx.user.id) == int(ctx.user.id) and int(
                        _ctx.ctx.channel_id
                    ) == int(ctx.channel_id)

                res = await self.client.wait_for_component(
                    components=buttons,
                    messages=int(_msg.id),
                    check=_check,
                    timeout=15,
                )

                author_answer: str = ""
                if res.ctx.custom_id == "true":
                    if correct_answer == "True":
                        author_answer = "correct"
                    elif correct_answer == "False":
                        author_answer = "wrong"
                elif res.ctx.custom_id == "false":
                    if correct_answer == "True":
                        author_answer = "wrong"
                    elif correct_answer == "False":
                        author_answer = "correct"

                if author_answer == "correct":
                    embed_ed.add_field(
                        name="‎",
                        value=f"{res.ctx.user.mention} had the correct answer.",
                        inline=False,
                    )
                    await res.ctx.edit_origin(
                        content="",
                        embeds=embed_ed,
                        components=buttons_disabled,
                    )
                    cnt += 1
                    await asyncio.sleep(3)
                    await msg.edit(
                        content=f"Getting question...\nStreak: {cnt}",
                        components=[],
                        embeds=[],
                    )
                    await asyncio.sleep(3)
                    i += 1
                    continue

                elif author_answer == "wrong":
                    embed_ed.add_field(
                        name="‎",
                        value=f"{res.ctx.user.mention} had the wrong answer.",
                        inline=False,
                    )
                    await res.ctx.edit_origin(
                        content=f"Streak: {cnt}",
                        embeds=embed_ed,
                        components=buttons_disabled,
                    )
                    break

            except asyncio.TimeoutError:
                await msg.edit(
                    content=f"Time's up! Streak: {cnt}",
                    embeds=embed_ed,
                    components=buttons_disabled,
                )
                break


def setup(client) -> None:
    """Setup the extension."""
    Trivia(client)
    logging.info("Loaded Trivia extension.")
