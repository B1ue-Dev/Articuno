"""
This module is for fun commands.

(C) 2022 - Jimmy-Blue
"""

import logging
import random
import asyncio
import datetime
import aiohttp
import interactions
from interactions.ext import molter
from utils.utils import get_response
from const import AUTHORIZATION


class Fun(molter.MolterExtension):
    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @molter.prefixed_command(name="coffee")
    async def _coffee(self, ctx: molter.MolterContext):
        """Sends an image of coffee."""

        url = "https://coffee.alexflipnote.dev/random.json"
        resp = await get_response(url)
        file = resp["file"]

        image = interactions.EmbedImageStruct(url=file)
        embed = interactions.Embed(title="Coffee ☕", color=0xC4771D, image=image)

        await ctx.send(embeds=embed)

    @molter.prefixed_command(name="ship")
    async def _ship(
        self,
        ctx: molter.MolterContext,
        user1: str,
        user2: str,
    ):
        """Ship 2 users."""

        shipnumber = int(random.randint(0, 100))

        if 0 <= shipnumber <= 30:
            comment = "Really low! {}".format(
                random.choice(
                    [
                        "Friendzone.",
                        'Just "friends".',
                        "There is barely any love.",
                        "I sense a small bit of love!",
                        "Still in that friendzone ;(",
                        "No, just no!",
                        "But there is a small sense of romance from one person!",
                    ]
                )
            )
            heart = ":broken_heart:"
        elif 31 <= shipnumber <= 70:
            comment = "Moderate! {}".format(
                random.choice(
                    [
                        "Fair enough!",
                        "A small bit of love is in the air...",
                        "I feel like there is some romance progressing!",
                        "I am starting to feel some love!",
                        "At least this is acceptable.",
                        "...",
                        "I sense a bit of potential!",
                        "But it is very one-sided.",
                    ]
                )
            )
            heart = ":mending_heart:"
        elif 71 <= shipnumber <= 90:
            comment = "Almost perfect! {}".format(
                random.choice(
                    [
                        "I definitely can see that love is in the air.",
                        "I feel the love!",
                        "There is a sign of a match!",
                        "A few things can be imporved to make this a match made in heaven!",
                        "I can definitely feel the love.",
                        "This has a big potential.",
                        "I can see the love is there! Somewhere...",
                    ]
                )
            )
            heart = random.choice(
                [
                    ":revolving_hearts:",
                    ":heart_exclamation:",
                    ":heart_on_fire:",
                    ":heartbeat:",
                ]
            )
        elif 90 < shipnumber <= 100:
            comment = "True love! {}".format(
                random.choice(
                    [
                        "It is a match!",
                        "There is a match made in heaven!",
                        "It is definitely a match!",
                        "Love is truely in the air!",
                        "Love is most definitely in the air!",
                    ]
                )
            )
            heart = random.choice(
                [
                    ":sparkling_heart:",
                    ":heart_decoration:",
                    ":hearts:",
                    ":two_hearts:",
                    ":heartpulse:",
                ]
            )

        if shipnumber <= 40:
            shipColor = 0xDD3939
        elif 41 < shipnumber < 80:
            shipColor = 0xFF6600
        else:
            shipColor = 0x3BE801

        field = [
            interactions.EmbedField(name=f"Result: {shipnumber}%", value=f"{comment}"),
        ]
        embed = interactions.Embed(
            title=f"**{user1}**    {heart}    **{user2}**",
            color=shipColor,
            fields=field,
            timestamp=datetime.datetime.utcnow(),
        )

        await ctx.send(embeds=embed)

    @molter.prefixed_command(name="roll")
    async def _roll(self, ctx: molter.MolterContext):
        """Rolls a dice."""

        dice = random.randint(1, 6)
        await ctx.send("I am rolling the dice...")
        await asyncio.sleep(1.5)
        await ctx.edit(f"The number is **{dice}**.")

    @molter.prefixed_command(name="flip")
    async def _flip(self, ctx: molter.MolterContext):
        """Flips a coin."""

        coin = random.choice(["heads", "tails"])
        await ctx.send("I am flipping the coin...")
        await asyncio.sleep(1.5)
        await ctx.edit(f"The coin landed on **{coin}**.")

    @molter.prefixed_command(name="gay")
    async def _gay(self, ctx: molter.MolterContext, *, user: str = None):
        """Calculates the gay percentage of a user."""

        if not user:
            user = ctx.user.username
        perc = int(random.randint(0, 100))

        embed = interactions.Embed(
            title="Gay measure tool",
            description=f"**{user}** is {perc}% gay.",
            color=random.randint(0, 0xFFFFFF),
        )

        await ctx.send(embeds=embed)

    @molter.prefixed_command(name="joke")
    async def _joke(self, ctx: molter.MolterContext):
        """Sends a random joke."""

        url = "https://some-random-api.ml/joke"
        resp = await get_response(url)

        embed = interactions.Embed(
            description=resp["joke"],
            color=random.randint(0, 0xFFFFFF),
        )

        await ctx.send(embeds=embed)

    @molter.prefixed_command(name="quote")
    async def _quote(self, ctx: molter.MolterContext):
        """Sends a quote."""

        url = "https://api.quotable.io/random"
        resp = await get_response(url)
        author = resp["author"]
        content = resp["content"]
        dateAdded = resp["dateAdded"]

        footer = interactions.EmbedFooter(text=f"Added on {dateAdded}")
        embed = interactions.Embed(
            title=f"From {author}",
            description=content,
            color=random.randint(0, 0xFFFFFF),
            footer=footer,
        )

        await ctx.send(embeds=embed)

    @molter.prefixed_command(name="xkcd")
    async def _xkcd(self, ctx: molter.MolterContext, page: int = None):
        """Sends a xkcd comic page."""

        url = "https://xkcd.com/info.0.json"
        resp = await get_response(url)
        newest = resp["num"]
        if page is None:
            page = random.randint(1, newest)
        url = "https://xkcd.com/{page}/info.0.json"
        resp = await get_response(url.format(page=page))
        if resp is None:
            return await ctx.send("Invalid page. Please try again.", ephemeral=True)

        month = resp["month"]
        year = resp["year"]
        day = resp["day"]
        title = resp["title"]
        alt = resp["alt"]
        img = resp["img"]

        footer = interactions.EmbedFooter(
            text=f"Page {page}/{newest} • Created on {year}-{month}-{day}"
        )
        image = interactions.EmbedImageStruct(url=img)
        author = interactions.EmbedAuthor(
            name=f"{title}",
            url=f"https://xkcd.com/{page}/",
            icon_url="https://camo.githubusercontent.com/8bd4217be107c9c190ef649b3d1550841f8b45c32fc0b71aa851b9107d70cdea/68747470733a2f2f6173736574732e7365727661746f6d2e636f6d2f786b63642d626f742f62616e6e6572332e706e67",
        )
        embed = interactions.Embed(
            description=alt,
            color=random.randint(0, 0xFFFFFF),
            footer=footer,
            image=image,
            author=author,
        )

        await ctx.send(embeds=embed)

    @molter.prefixed_command(name="dictionary")
    async def _dictionary(self, ctx: molter.MolterContext, word: str):
        """Defines a word."""

        url = "https://some-random-api.ml/dictionary"
        params = {"word": word}
        resp = await get_response(url, params=params)

        if resp is None:
            return await ctx.send("No word found. Please try again.", ephemeral=True)

        term = resp["word"]
        definition = resp["definition"]
        if len(definition) > 4096:
            definition = definition[:4000] + "..."
        embed = interactions.Embed(
            title=f"Definition of {term}",
            description=definition,
            color=random.randint(0, 0xFFFFFF),
        )

        await ctx.send(embeds=embed)

    @molter.prefixed_command(name="ai")
    async def _ai(self, ctx: molter.MolterContext, *, message: str):
        customize_url = "https://v6.rsa-api.xyz/ai/customize"
        response_url = "https://v6.rsa-api.xyz/ai/response"
        param = {
            "user_id": str(ctx.user.id),
            "message": message,
        }
        headers = {
            "Authorization": AUTHORIZATION,
        }
        params = {
            "BotName": "Articuno",
            "BotMaster": "Blue",
            "BotGender": "Male",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(customize_url, headers=headers, data=params) as res:
                async with session.get(
                    response_url, params=param, headers=headers
                ) as resp:
                    if resp.status == 200:
                        if resp.content_type == "application/json":
                            resp = await resp.json()

                            await ctx.send(content=resp["message"])


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Fun(client)
    logging.debug("""[%s] Loaded Fun extension.""", log_time)
