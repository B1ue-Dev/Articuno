"""
This module is for fun commands.

(C) 2022 - Jimmy-Blue
"""

import random
import asyncio
import datetime
import base64 as b64
import interactions
from interactions import extension_command as command
import pyfiglet
from googleapiclient.discovery import build
from better_profanity import profanity
from utils.utils import get_response
from const import AUTHORIZATION, GOOGLE_CLOUD, GOOGLE_CSE


choice_convert = {
    1: 'Rock',
    2: 'Paper',
    3: 'Scissors'
}


buttons = [
    interactions.ActionRow(
        components=[
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="◄",
                custom_id="previous",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="►",
                custom_id="next"
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="■",
                custom_id="stop"
            )
        ]
    )
]

rps_selection = interactions.SelectMenu(
    options=[
        interactions.SelectOption(
            label="Rock",
            emoji=interactions.Emoji(name="🪨"),
            value="1",
        ),
        interactions.SelectOption(
            label="Paper",
            emoji=interactions.Emoji(name="📃"),
            value="2",
        ),
        interactions.SelectOption(
            label="Scissors",
            emoji=interactions.Emoji(name="✂"),
            value="3",
        )
    ],
    placeholder="Choose your option",
    custom_id="rps_selection",
    min_values=1,
    max_values=1
)


class Fun(interactions.Extension):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name="coffee",
        description="Send an image of coffee"
    )
    async def _coffee(self, ctx: interactions.CommandContext):
        url = "https://coffee.alexflipnote.dev/random.json"
        resp = await get_response(url)
        file = resp['file']

        image = interactions.EmbedImageStruct(url=file)
        embed = interactions.Embed(
            title="Coffee ☕",
            color=0xc4771d,
            image=image
        )

        await ctx.send(embeds=embed)


    @command(
        name="ship",
        description="Ship 2 users",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="user1",
                description="User 1",
                required=False
            ),
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="user2",
                description="User 2",
                required=False
            )
        ]
    )
    async def _ship(self, ctx: interactions.CommandContext, user1: str = None, user2: str = None):
        shipnumber = int(random.randint(0, 100))
        guild = await ctx.get_guild()
        members_list = await guild.get_list_of_members(limit=1000)

        if not user1 and not user2:
            result = random.choice(members_list)
            user1 = ctx.user.username if ctx.member.nick is None else ctx.member.nick
            user2 = result.user.username if result.nick is None else result.nick
        if not user2 and user1:
            user_1 = user1
            user2 = user_1
            user1 = ctx.user.username if ctx.member.nick is None else ctx.member.nick
        if not user1 and user2:
            result = random.choice(members_list)
            user1 = result.user.username if result.nick is None else result.nick

        if 0 <= shipnumber <= 30:
            comment = "Really low! {}".format(
                random.choice(
                    [
                        'Friendzone.',
                        'Just "friends".',
                        'There is barely any love.',
                        'I sense a small bit of love!',
                        'Still in that friendzone ;(',
                        'No, just no!',
                        'But there is a small sense of romance from one person!'
                    ]
                )
            )
            heart = ":broken_heart:"
        elif 31 <= shipnumber <= 70:
            comment = "Moderate! {}".format(
                random.choice(
                    [
                        'Fair enough!',
                        'A small bit of love is in the air...',
                        'I feel like there is some romance progressing!',
                        'I am starting to feel some love!',
                        'At least this is acceptable.',
                        '...',
                        'I sense a bit of potential!',
                        'But it is very one-sided.'
                    ]
                )
            )
            heart = ":mending_heart:"
        elif 71 <= shipnumber <= 90:
            comment = "Almost perfect! {}".format(
                random.choice(
                    [
                        'I definitely can see that love is in the air.',
                        'I feel the love!',
                        'There is a sign of a match!',
                        'A few things can be imporved to make this a match made in heaven!',
                        'I can definitely feel the love.',
                        'This has a big potential.',
                        'I can see the love is there! Somewhere...'
                    ]
                )
            )
            heart = random.choice(
                [
                    ':revolving_hearts:',
                    ':heart_exclamation:',
                    ':heart_on_fire:',
                    ':heartbeat:'
                ]
            )
        elif 90 < shipnumber <= 100:
            comment = "True love! {}".format(
                random.choice(
                    [
                        'It is a match!', 
                        'There is a match made in heaven!',
                        'It is definitely a match!',
                        'Love is truely in the air!',
                        'Love is most definitely in the air!'
                    ]
                )
            )
            heart = random.choice(
                [
                    ':sparkling_heart:',
                    ':heart_decoration:',
                    ':hearts:',
                    ':two_hearts:',
                    ':heartpulse:'
                ]
            )

        if shipnumber <= 40:
            shipColor = 0xdd3939
        elif 41 < shipnumber < 80:
            shipColor = 0xff6600
        else:
            shipColor = 0x3be801

        field = [
            interactions.EmbedField(name=f"Result: {shipnumber}%", value=f"{comment}"),
        ]
        embed = interactions.Embed(
            title=f"**{user1}**    {heart}    **{user2}**",
            color=shipColor,
            fields=field,
            timestamp=datetime.datetime.utcnow()
        )

        await ctx.send(embeds=embed)


    @command(
        name="roll",
        description="Roll a dice"
    )
    async def _roll(self, ctx: interactions.CommandContext):
        dice = random.randint(1, 6)
        await ctx.send("I am rolling the dice...")
        await asyncio.sleep(1.5)
        await ctx.edit("The number is **{}**.".format(dice))


    @command(
        name="flip",
        description="Flip a coin"
    )
    async def _flip(self, ctx: interactions.CommandContext):
        coin = random.choice(["heads", "tails"])
        await ctx.send("I am flipping the coin...")
        await asyncio.sleep(1.5)
        await ctx.edit("The coin landed on **{}**.".format(coin))


    @command(
        name="gay",
        description="Calculate the gay percentage of a user",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="user",
                description="Targeted user",
                required=False
            )
        ]
    )
    async def _gay(self, ctx: interactions.CommandContext, user: str = None):
        if not user:
            user = ctx.user.username
        perc = int(random.randint(0, 100))

        embed = interactions.Embed(
            title="Gay measure tool",
            description=f"**{user}** is {perc}% gay.",
            color=random.randint(0, 0xFFFFFF)
        )

        await ctx.send(embeds=embed)


    @command(
        name="ascii",
        description="Make an ASCII art word",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="word",
                description="Word to convert",
                required=True
            )
        ]
    )
    async def _ascii(self, ctx: interactions.CommandContext, word: str):
        if len(word) > 10:
            return await ctx.send("Word too long!", ephemeral=True)
        else:
            ascii_art = pyfiglet.figlet_format(word)
            await ctx.send(f"```\n{ascii_art}```")


    @command(
        name="joke",
        description="Send a random joke"
    )
    async def _joke(self, ctx: interactions.CommandContext):
        url = "https://some-random-api.ml/joke"
        resp = await get_response(url)

        embed = interactions.Embed(
            description=resp['joke'],
            color=random.randint(0, 0xFFFFFF)
        )

        await ctx.send(embeds=embed)


    @command(
        name="quote",
        description="Send a quote"
    )
    async def _quote(self, ctx: interactions.CommandContext):
        url = 'https://api.quotable.io/random'
        resp = await get_response(url)
        author = resp['author']
        content = resp['content']
        dateAdded = resp['dateAdded']

        footer = interactions.EmbedFooter(text=f"Added on {dateAdded}")
        embed = interactions.Embed(
            title=f"From {author}",
            description=content,
            color=random.randint(0, 0xFFFFFF),
            footer=footer
        )

        await ctx.send(embeds=embed)


    @command(
        name="xkcd",
        description="Send a xkcd comic page",
        options=[
            interactions.Option(
                type=interactions.OptionType.INTEGER,
                name="page",
                description="The page you want to read (if any)",
                required=False
            )
        ]
    )
    async def _xkcd(self, ctx: interactions.CommandContext, page: int = None):
        url = "https://xkcd.com/info.0.json"
        resp = await get_response(url)
        newest = resp['num']
        if page is None:
            page = random.randint(1, newest)
        url = "https://xkcd.com/{page}/info.0.json"
        resp = await get_response(url.format(page=page))
        if resp is None:
            return await ctx.send("Invalid page. Please try again.", ephemeral=True)
        else:	
            month = resp['month']
            year = resp['year']
            day = resp['day']
            title = resp['title']
            alt = resp['alt']
            img = resp['img']

            footer = interactions.EmbedFooter(text=f"Page {page}/{newest} • Created on {year}-{month}-{day}")
            image = interactions.EmbedImageStruct(url=img)
            author = interactions.EmbedAuthor(
                name=f"{title}",
                url=f"https://xkcd.com/{page}/",
                icon_url="https://camo.githubusercontent.com/8bd4217be107c9c190ef649b3d1550841f8b45c32fc0b71aa851b9107d70cdea/68747470733a2f2f6173736574732e7365727661746f6d2e636f6d2f786b63642d626f742f62616e6e6572332e706e67"
            )
            embed = interactions.Embed(
                description=alt,
                color=random.randint(0, 0xFFFFFF),
                footer=footer,
                image=image,
                author=author
            )

            await ctx.send(embeds=embed)


    @command(
        name="dictionary",
        description="Define a word",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="word",
                description="The word you want to define",
                required=True
            )
        ]
    )
    async def _dictionary(self, ctx: interactions.CommandContext, word: str):
        url = "https://some-random-api.ml/dictionary"
        params = {
            "word": word
        }
        resp = await get_response(url, params=params)

        if resp is None:
            return await ctx.send("No word found. Please try again.", ephemeral=True)
        else:
            term = resp['word']
            definition = resp['definition']
            if len(definition) > 4096:
                definition = definition[:4000] + "..."
            embed = interactions.Embed(
                title=f"Definition of {term}",
                description=definition,
                color=random.randint(0, 0xFFFFFF)
            )

            await ctx.send(embeds=embed)


    @command(
        name="ai",
        description="Chat with an AI",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="message",
                description="The message you want to send",
                required=True
            )
        ]
    )
    async def _ai(self, ctx: interactions.CommandContext, message: str):
        url = "https://random-stuff-api.p.rapidapi.com/ai"
        params = {
            "msg": message,
            "bot_name": "Articuno",
            "bot_gender": "male",
            "bot_master": "Blue"
        }
        headers = {
            'authorization': AUTHORIZATION,
            'x-rapidapi-host': "random-stuff-api.p.rapidapi.com",
            'x-rapidapi-key': "aad44bed6dmshba8fa4c3f4d92c2p118235jsne1aae4f19e3f"				
        }
        resp = await get_response(url, params=params, headers=headers)
        msg = resp['AIResponse']
        await ctx.send(msg)


    @command(
        name="urban",
        description="Define a word on Urban Dictionary",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="term",
                description="The term you want to define",
                required=True
            )
        ]
    )
    async def _urban(self, ctx: interactions.CommandContext, term: str):
        channel = await ctx.get_channel()
        if channel.nsfw is False:
            return await ctx.send("Please use this command in a NSFW channel.", ephemeral=True)
        _ran = 0
        await ctx.defer()
        url = "https://api.urbandictionary.com/v0/define"
        params = {
            "term": term
        }
        resp = await get_response(url, params=params)
        if len(resp['list']) == 0:
            embed = interactions.Embed(
                description="No results found.",
            )
            await ctx.send(embeds=embed, ephemeral=True)
        else:
            ran = int(0)
            _ran = ran
            page = int(len(resp["list"]) - 1)
            definition = resp['list'][ran]['definition']
            if len(definition) > 700:
                definition = definition[:690] + "..."
            example = resp['list'][ran]['example']
            if len(example) > 700:
                example = example[:330] + "..."

            footer = interactions.EmbedFooter(
                text=f"👍 {resp['list'][ran]['thumbs_up']} • 👎 {resp['list'][ran]['thumbs_down']} • Page {ran}/{page}",
                icon_url="https://store-images.s-microsoft.com/image/apps.20202.13510798884772369.4d67f3fd-b81b-4f91-b3a0-8dcf0c039f62.e5abe879-5dc9-4adf-8fd8-6aad8bd2fb91"
            )
            embed = interactions.Embed(
                title=f"{resp['list'][ran]['word']}",
                footer=footer
            )
            embed.add_field(name="Definition", value=f"{definition}", inline=True)
            embed.add_field(name="Example", value=f"{example}", inline=True)

            msg = await ctx.send(embeds=embed, components=buttons)
            while True:
                try:
                    res = await self.bot.wait_for_component(components=buttons, messages = int(msg.id), timeout = 8)
                    if int(res.user.id) == int(ctx.user.id):
                        if res.custom_id == "previous":
                            if ran == 0:
                                ran = int(0)
                                _ran = ran
                            else:
                                ran = int(ran - 1)
                                _ran = ran
                                definition = resp['list'][ran]['definition']
                                if len(definition) > 700:
                                    definition = definition[:690] + "..."
                                example = resp['list'][ran]['example']
                                if len(example) > 700:
                                    example = example[:330] + "..."

                                footer = interactions.EmbedFooter(
                                    text=f"👍 {resp['list'][ran]['thumbs_up']} • 👎 {resp['list'][ran]['thumbs_down']} • Page {ran}/{page}",
                                    icon_url="https://store-images.s-microsoft.com/image/apps.20202.13510798884772369.4d67f3fd-b81b-4f91-b3a0-8dcf0c039f62.e5abe879-5dc9-4adf-8fd8-6aad8bd2fb91"
                                )
                                embed = interactions.Embed(
                                    title=f"{resp['list'][ran]['word']}",
                                    footer=footer
                                )
                                embed.add_field(name="Definition", value=f"{definition}", inline=True)
                                embed.add_field(name="Example", value=f"{example}", inline=True)
                                await res.edit(embeds=embed)
                        elif res.custom_id == "next":
                            if ran == page:
                                ran = int(page)
                                _ran = ran
                            else:
                                ran = int(ran + 1)
                                _ran = ran
                                definition = resp['list'][ran]['definition']
                                if len(definition) > 700:
                                    definition = definition[:690] + "..."
                                example = resp['list'][ran]['example']
                                if len(example) > 700:
                                    example = example[:330] + "..."

                                footer = interactions.EmbedFooter(
                                    text=f"👍 {resp['list'][ran]['thumbs_up']} • 👎 {resp['list'][ran]['thumbs_down']} • Page {ran}/{page}",
                                    icon_url="https://store-images.s-microsoft.com/image/apps.20202.13510798884772369.4d67f3fd-b81b-4f91-b3a0-8dcf0c039f62.e5abe879-5dc9-4adf-8fd8-6aad8bd2fb91"
                                )
                                embed = interactions.Embed(
                                    title=f"{resp['list'][ran]['word']}",
                                    footer=footer
                                )
                                embed.add_field(name="Definition", value=f"{definition}", inline=True)
                                embed.add_field(name="Example", value=f"{example}", inline=True)
                                await res.edit(embeds=embed)
                        elif res.custom_id == "stop":
                            await msg.delete()
                            break
                except asyncio.TimeoutError:
                    definition = resp['list'][_ran]['definition']
                    if len(definition) > 700:
                        definition = definition[:690] + "..."
                    example = resp['list'][_ran]['example']
                    if len(example) > 700:
                        example = example[:330] + "..."

                    footer = interactions.EmbedFooter(
                        text=f"👍 {resp['list'][_ran]['thumbs_up']} • 👎 {resp['list'][_ran]['thumbs_down']} • Page {ran}/{page}",
                        icon_url="https://store-images.s-microsoft.com/image/apps.20202.13510798884772369.4d67f3fd-b81b-4f91-b3a0-8dcf0c039f62.e5abe879-5dc9-4adf-8fd8-6aad8bd2fb91"
                    )
                    embed = interactions.Embed(
                        title=f"{resp['list'][_ran]['word']}",
                        footer=footer
                    )
                    embed.add_field(name="Definition", value=f"{definition}", inline=True)
                    embed.add_field(name="Example", value=f"{example}", inline=True)
                    await msg.edit(embeds=embed, components=[])


    @command(
        name="img",
        description="Search for images using Google Images",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="query",
                description="Query to search for",
                required=True
            )
        ]
    )
    async def _img(self, ctx: interactions.CommandContext, query: str):
        if profanity.contains_profanity(query) is True:
            return await ctx.send("No result found.", ephemeral=True)
        await ctx.defer()
        ran = int(0)
        resource = build("customsearch", "v1", developerKey=GOOGLE_CLOUD).cse()
        result = resource.list(
            q=f"{query}", cx=GOOGLE_CSE, searchType="image"
        ).execute()
        try:
            image_link = result["items"][ran]["link"]
            title = result["items"][ran]["title"]
            displayLink = result["items"][ran]["displayLink"]
            contextLink = result["items"][ran]["image"]["contextLink"]

            embed = interactions.Embed(title=f"Image for: {query}", color=0x000000)
            embed.set_footer(text=f"Google Search • Page {ran}/9", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png")
            embed.add_field(name=f"**{displayLink}**", value=f"[{title}]({contextLink})", inline=False)
            embed.set_image(url=image_link)

            msg = await ctx.send(embeds=embed, components=buttons)
            _ran = 0
            while True:
                try:
                    res = await self.bot.wait_for_component(components=buttons, messages=int(msg.id), timeout = 15)
                    if int(res.user.id) == int(ctx.user.id):
                        if res.custom_id == "next":
                            ran += 1
                            if ran < 9:
                                ran = ran
                                _ran = ran
                            image_link = result["items"][ran]["link"]
                            title = result["items"][ran]["title"]
                            displayLink = result["items"][ran]["displayLink"]
                            contextLink = result["items"][ran]["image"]["contextLink"]

                            embed = interactions.Embed(title=f"Image for: {query}", color=0x000000)
                            embed.set_footer(text=f"Google Search • Page {ran}/9", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png")
                            embed.add_field(name=f"**{displayLink}**", value=f"[{title}]({contextLink})", inline=False)
                            embed.set_image(url=image_link)

                            await res.edit(embeds=embed)

                        elif res.custom_id == "previous":
                            ran -= 1
                            if ran < 0:
                                ran = 0
                                _ran = ran
                            image_link = result["items"][ran]["link"]
                            title = result["items"][ran]["title"]
                            displayLink = result["items"][ran]["displayLink"]
                            contextLink = result["items"][ran]["image"]["contextLink"]

                            embed = interactions.Embed(title=f"Image for: {query}", color=0x000000)
                            embed.set_footer(text=f"Google Search • Page {ran}/9", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png")
                            embed.add_field(name=f"**{displayLink}**", value=f"[{title}]({contextLink})", inline=False)
                            embed.set_image(url=image_link)

                            await res.edit(embeds=embed)

                        elif res.custom_id == "stop":
                            await msg.delete()
                            break
                    else:
                        await res.edit()
                except asyncio.TimeoutError:
                    image_link = result["items"][_ran]["link"]
                    title = result["items"][_ran]["title"]
                    displayLink = result["items"][_ran]["displayLink"]
                    contextLink = result["items"][_ran]["image"]["contextLink"]

                    embed = interactions.Embed(title=f"Image for: {query}", color=0x000000)
                    embed.set_footer(
                        text=f"Google Search • Page {_ran}/9",
                        icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png"
                    )
                    embed.add_field(name=f"**{displayLink}**", value=f"[{title}]({contextLink})", inline=False)
                    embed.set_image(url=image_link)
                    await msg.edit(embeds=embed, components=[])
        except KeyError:
            await ctx.send("No result found.", ephemeral=True)


    @command(
        name="trivia",
        description="Play a game of trivia",
    )
    async def _trivia(self, ctx: interactions.CommandContext):
        await ctx.defer()
        buttons = [
            interactions.ActionRow(
                components=[
                    interactions.Button(
                        style=interactions.ButtonStyle.SUCCESS,
                        label="True",
                        custom_id="true"
                    ),
                    interactions.Button(
                        style=interactions.ButtonStyle.DANGER,
                        label="False",
                        custom_id="false"
                    ),
                ]
            )
        ]
        url = "https://opentdb.com/api.php?amount=1&type=boolean&encode=base64"
        resp = await get_response(url)
        if resp["response_code"] == 0:
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
        else:
            return await ctx.send("An error occured", ephemeral=True)
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
                interactions.ActionRow(
                    components=[
                        interactions.Button(
                            style=interactions.ButtonStyle.SUCCESS,
                            label="True",
                            custom_id="true",
                            disabled=True
                        ),
                        interactions.Button(
                            style=interactions.ButtonStyle.DANGER,
                            label="False",
                            custom_id="false",
                            disabled=True
                        ),
                    ]
                )
            ]
            try:
                res = await self.bot.wait_for_component(components=buttons, messages=int(ctx.message.id), timeout=15)
                if int(res.user.id) == int(ctx.user.id):
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
                else:
                    await res.edit()

            except asyncio.TimeoutError:
                await msg.edit(content="Time's up!", embeds=embed_ed, components=buttons_disabled)


    @command(
        name="rock_paper_scissors_ai",
        description="Play a game of rock paper scissors against the AI",
    )
    async def _rock_paper_scissors_ai(self, ctx: interactions.CommandContext):
        await ctx.defer()
        msg = await ctx.send(content=f"{ctx.user.mention} vs **Articuno**", components=rps_selection)
        while True:
            try:
                res = await self.bot.wait_for_component(components=rps_selection, messages=int(ctx.message.id), timeout=15)
                if int(res.user.id) == int(ctx.user.id):
                    rps_selection.disabled=True
                    bot_choice = int(random.randint(1, 3))
                    user_choice = int(res.data.values[0])
                    if user_choice == bot_choice:
                        await res.edit(
                            content=f"{res.user.mention} chose **{choice_convert[user_choice]}**.\n**Articuno** chose **{choice_convert[bot_choice]}**.\n\n> It's a tie!",
                            components=rps_selection
                        )
                    elif (user_choice - bot_choice) % 3 == 1:
                        await res.edit(
                            content=f"{res.user.mention} chose **{choice_convert[user_choice]}**.\n**Articuno** chose **{choice_convert[bot_choice]}**.\n\n> {res.user.mention} wins!",
                            components=rps_selection
                        )
                    elif (user_choice - bot_choice) % 3 == 2:
                        await res.edit(
                            content=f"{res.user.mention} chose **{choice_convert[user_choice]}**.\n**Articuno** chose **{choice_convert[bot_choice]}**.\n\n> **Articuno** wins!",
                            components=rps_selection
                        )
                    break
                else:
                    pass
            except asyncio.TimeoutError:
                rps_selection.disabled = True
                await msg.edit(content="Time's up!", components=rps_selection)
                break


    @command(
        name="rock_paper_scissors_human",
        description="Play a game of rock paper scissors against a user",
        options=[
            interactions.Option(
                type=interactions.OptionType.USER,
                name="user",
                description="The user to play against",
                required=True
            )
        ],	
        dm_permission=False
    )
    async def _rock_paper_scissors_human(self, ctx: interactions.CommandContext, user: interactions.User):
        accept_deny = [
            interactions.ActionRow(
                components=[
                    interactions.Button(
                        style=interactions.ButtonStyle.SUCCESS,
                        label="Accept",
                        custom_id="accept"
                    ),
                    interactions.Button(
                        style=interactions.ButtonStyle.DANGER,
                        label="Deny",
                        custom_id="deny"
                    )
                ]
            )
        ]
        if int(user.id) == int(ctx.user.id):
            return await ctx.send("You cannot challenge yourself.", ephemeral=True)
        elif int(user.id) == int(self.bot.me.id):
            return await ctx.send("To challenge me, do ``/rock_paper_scissors_ai`` instead.", ephemeral=True)
        await ctx.defer()
        msg = await ctx.send(content=f"{ctx.user.mention} challenged {user.mention}.", components=accept_deny)
        while True:
            try:
                op: interactions.ComponentContext = await self.bot.wait_for_component(components=accept_deny, messages=int(ctx.message.id), timeout=15)
                if int(op.user.id) == int(user.id):
                    if op.custom_id == "accept":
                        await op.edit(content=f"{ctx.user.mention} vs {user.mention}", components=rps_selection)
                        user1 = int(ctx.user.id)
                        user2 = int(user.id)
                        cmp_1 = 0
                        while True:
                            cmp1: interactions.ComponentContext = await self.bot.wait_for_component(components=rps_selection, messages=int(ctx.message.id), timeout=15)
                            if int(cmp1.user.id) == user1 or int(cmp1.user.id) == user2:
                                cmp_1 = int(cmp1.user.id)
                                await cmp1.edit(content=f"{cmp1.message.content}\n\n{cmp1.user.mention} has their option chosen.")
                                choice1 = int(cmp1.data.values[0])
                                break
                            else:
                                pass

                        while True:
                            cmp2: interactions.ComponentContext = await self.bot.wait_for_component(components=rps_selection, messages=int(ctx.message.id), timeout=15)
                            if int(cmp2.user.id) in {int(user1), int(user2)} and int(cmp2.user.id) != int(cmp_1):
                                rps_selection.disabled = True
                                choice2 = int(cmp2.data.values[0])
                                break
                            else:
                                pass

                        if choice1 == choice2:
                            await cmp2.edit(content=f"{ctx.user.mention} chose **{choice_convert[choice1]}**.\n{user.mention} chose **{choice_convert[choice2]}**.\n\n> It's a tie!", components=rps_selection)
                        elif (choice1 - choice2) % 3 == 1:
                            await cmp2.edit(content=f"{ctx.user.mention} chose **{choice_convert[choice1]}**.\n{user.mention} chose **{choice_convert[choice2]}**.\n\n> {ctx.user.mention} wins!", components=rps_selection)
                        elif (choice1 - choice2) % 3 == 2:
                            await cmp2.edit(content=f"{ctx.user.mention} chose **{choice_convert[choice1]}**.\n{user.mention} chose **{choice_convert[choice2]}**.\n\n> {user.mention} wins!", components=rps_selection)
                        break

                    elif op.custom_id == "deny":
                        await msg.edit(content=f"{user.mention} declined the challenge.", components=[])
                        break
                elif int(op.user.id) != int(user.id) and int(op.user.id) == int(ctx.user.id) and op.custom_id == "deny":
                    await op.edit(f"{ctx.user.mention} cancelled the challenge.", components=[])
                    break
                elif int(op.user.id) != int(user.id) and int(op.user.id) == int(ctx.user.id) and op.custom_id == "accept":
                    await op.send("You cannot accept the challenge by yourself.", components=[], ephemeral=True)
                else:
                    pass
            except asyncio.TimeoutError:
                await msg.edit(content="Time's up!", components=[])
                break


def setup(bot):
    Fun(bot)
