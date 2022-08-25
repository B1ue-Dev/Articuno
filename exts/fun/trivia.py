"""
Trivia command.

(C) 2022 - Jimmy-Blue
"""

import logging
import random
import asyncio
import datetime
import base64 as b64
import interactions
from interactions.ext.wait_for import wait_for_component
from utils.utils import get_response


class Trivia(interactions.Extension):
    """Extension for /trivia."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="trivia",
        description="Play a game of trivia.",
        options=[
            interactions.Option(
                type=interactions.OptionType.INTEGER,
                name="category",
                description="The category you want to play",
                choices=[
                    interactions.Choice(
                        name="General Knowledge",
                        value=9,
                    ),
                    interactions.Choice(
                        name="Film",
                        value=11,
                    ),
                    interactions.Choice(
                        name="Music",
                        value=12,
                    ),
                    interactions.Choice(
                        name="Video Games",
                        value=15,
                    ),
                    interactions.Choice(
                        name="Computers",
                        value=18,
                    ),
                    interactions.Choice(
                        name="Sports",
                        value=21
                    ),
                    interactions.Choice(
                        name="Comics",
                        value=29,
                    ),
                    interactions.Choice(
                        name="Japanese Anime & Manga",
                        value=31,
                    ),
                ],
                required=False,
            ),
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="difficulty",
                description="The difficulty level",
                choices=[
                    interactions.Choice(
                        name="Easy",
                        value="easy",
                    ),
                    interactions.Choice(
                        name="Medium",
                        value="medium",
                    ),
                    interactions.Choice(
                        name="Hard",
                        value="hard",
                    ),
                ],
            ),
        ],
    )
    async def _trivia(
        self,
        ctx: interactions.CommandContext,
        category: int = 9,
        difficulty: str = "",

    ):
        """Plays a game of trivia."""

        await ctx.defer()

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

        url = f"https://opentdb.com/api.php"
        params = {
            "amount": "1",
            "type": "boolean",
            "encode": "base64",
            "category": category,
            "difficulty": difficulty,
        }
        resp = await get_response(url=url, params=params)

        if resp["response_code"] != 0:
            return await ctx.send("An error occured", ephemeral=True)

        _category = b64.b64decode(resp["results"][0]["category"])
        category = _category.decode("utf-8")
        _question = b64.b64decode(resp["results"][0]["question"])
        question = _question.decode("utf-8")
        _correct_answer = b64.b64decode(resp["results"][0]["correct_answer"])
        correct_answer = _correct_answer.decode("utf-8")
        embed = interactions.Embed(
            title="Trivia",
            description=f"**{category}**: {question}",
            author=interactions.EmbedAuthor(
                name=f"{ctx.user.username}#{ctx.user.discriminator}",
                icon_url=ctx.user.avatar_url
            )
        )
        msg = await ctx.send(embeds=embed, components=buttons)


        while True:
            embed_ed = interactions.Embed(
                title="Trivia",
                description=f"**{category}**: {question}",
                author=interactions.EmbedAuthor(
                    name=f"{ctx.user.username}#{ctx.user.discriminator}",
                    icon_url=ctx.user.avatar_url
                )
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
                def check(_ctx: interactions.ComponentContext) -> bool:
                    if (
                        int(_ctx.author.id) == int(ctx.user.id)
                        and int(_ctx.channel_id) == int(ctx.channel_id)
                    ):
                        return True
                    else:
                        return False

                res: interactions.ComponentContext = await wait_for_component(
                    self.client,
                    components=buttons,
                    messages=int(ctx.message.id),
                    check=check,
                    timeout=15,
                )

                if res.custom_id == "true":
                    if correct_answer == "True":
                        author_answer = "correct"
                    elif correct_answer == "False":
                        author_answer = "wrong"
                elif res.custom_id == "false":
                    if correct_answer == "True":
                        author_answer = "wrong"
                    elif correct_answer == "False":
                        author_answer = "correct"

                if author_answer == "correct":
                    embed_ed.add_field(name="‎", value=f"{res.user.mention} had the correct answer.", inline=False)
                    await res.edit(embeds=embed_ed, components=buttons_disabled)
                    await res.send(content=f"{res.user.mention}, you were correct.", ephemeral=True)
                    break
                elif author_answer == "wrong":
                    embed_ed.add_field(name="‎", value=f"{res.user.mention} had the wrong answer.", inline=False)
                    await res.edit(embeds=embed_ed, components=buttons_disabled)
                    await res.send(content=f"{res.user.mention}, you were wrong.", ephemeral=True)
                    break


            except asyncio.TimeoutError:
                await msg.edit(content="Time's up!", embeds=embed_ed, components=buttons_disabled)

def setup(client) -> None:
    """Setup the extension."""
    log_time = (
        datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    ).strftime("%d/%m/%Y %H:%M:%S")
    Trivia(client)
    logging.debug("""[%s] Loaded Trivia extension.""", log_time)
    print(f"[{log_time}] Loaded Trivia extension.")
