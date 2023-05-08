"""
Trivia command.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import asyncio
import base64 as b64
import interactions
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

    @interactions.slash_command(
        name="trivia",
        description="Play a game of trivia.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.INTEGER,
                name="category",
                description="The category you want to play",
                choices=[
                    interactions.SlashCommandChoice(
                        name="General Knowledge",
                        value=9,
                    ),
                    interactions.SlashCommandChoice(
                        name="Book",
                        value=10,
                    ),
                    interactions.SlashCommandChoice(
                        name="Film",
                        value=11,
                    ),
                    interactions.SlashCommandChoice(
                        name="Music",
                        value=12,
                    ),
                    interactions.SlashCommandChoice(
                        name="Musicals & Theatres",
                        value=13,
                    ),
                    interactions.SlashCommandChoice(
                        name="Television",
                        value=14,
                    ),
                    interactions.SlashCommandChoice(
                        name="Video Games",
                        value=15,
                    ),
                    interactions.SlashCommandChoice(
                        name="Nature",
                        value=17,
                    ),
                    interactions.SlashCommandChoice(
                        name="Computers",
                        value=18,
                    ),
                    interactions.SlashCommandChoice(name="Sports", value=21),
                    interactions.SlashCommandChoice(
                        name="Geography",
                        value=22,
                    ),
                    interactions.SlashCommandChoice(
                        name="History",
                        value=23,
                    ),
                    interactions.SlashCommandChoice(
                        name="Animal",
                        value=27,
                    ),
                    interactions.SlashCommandChoice(
                        name="Vehicles",
                        value=28,
                    ),
                    interactions.SlashCommandChoice(
                        name="Comics",
                        value=29,
                    ),
                    interactions.SlashCommandChoice(
                        name="Japanese Anime & Manga",
                        value=31,
                    ),
                    interactions.SlashCommandChoice(
                        name="Cartoons",
                        value=32,
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
                        name="Easy",
                        value="easy",
                    ),
                    interactions.SlashCommandChoice(
                        name="Medium",
                        value="medium",
                    ),
                    interactions.SlashCommandChoice(
                        name="Hard",
                        value="hard",
                    ),
                ],
                required=True,
            ),
        ],
    )
    async def trivia(
        self,
        ctx: interactions.SlashContext,
        category: int,
        difficulty: str,
    ):
        """Plays a game of trivia."""

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
        _selected_category: str = category
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
