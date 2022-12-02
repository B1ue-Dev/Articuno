"""
UwU

2022 - Jimmy-Blue
"""

import logging
import datetime
import random
import interactions
from interactions.ext import molter


class OwO:
    """OwO"""

    smileys = [
        "(ᵘʷᵘ)",
        "(ᵘﻌᵘ)",
        "(◡ ω ◡)",
        "(◡ ꒳ ◡)",
        "(◡ w ◡)",
        "(◡ ሠ ◡)",
        "(˘ω˘)",
        "(⑅˘꒳˘)",
        "(˘ᵕ˘)",
        "(˘ሠ˘)",
        "(˘³˘)",
        "(˘ε˘)",
        "(˘˘˘)",
        "( ᴜ ω ᴜ )",
        "(„ᵕᴗᵕ„)",
        "(ㅅꈍ ˘ ꈍ)",
        "(⑅˘꒳˘)",
        "( ｡ᵘ ᵕ ᵘ ｡)",
        "( ᵘ ꒳ ᵘ ✼)",
        "( ˘ᴗ˘ )",
        "(ᵕᴗ ᵕ⁎)",
        "*:･ﾟ✧(ꈍᴗꈍ)✧･ﾟ:*",
        "*˚*(ꈍ ω ꈍ).₊̣̇.",
        "(。U ω U。)",
        "(U ᵕ U❁)",
        "(U ﹏ U)",
        "(◦ᵕ ˘ ᵕ◦)",
        "ღ(U꒳Uღ)",
        "♥(。U ω U。)",
        "– ̗̀ (ᵕ꒳ᵕ) ̖́-",
        "( ͡U ω ͡U )",
        "( ͡o ᵕ ͡o )",
        "( ͡o ꒳ ͡o )",
        "( ˊ.ᴗˋ )",
        "(ᴜ‿ᴜ✿)",
        "~(˘▾˘~)",
        "(｡ᴜ‿‿ᴜ｡)",
        "UwU",
        ">w<",
        "^w^",
        "(◕ᴥ◕)",
        "ʕ•ᴥ•ʔ",
        "ʕ￫ᴥ￩ʔ",
        "(*^ω^)",
        "(◕‿◕✿)",
        "(*^.^*)",
        "(*￣з￣)",
        "(つ✧ω✧)つ",
        "(/ =ω=)/",
    ]

    mappings = [
        ["r", "w"],
        ["l", "w"],
        ["na", "nya"],
        ["ni", "nyi"],
        ["nu", "nyu"],
        ["ne", "nye"],
        ["no", "nyo"],
        ["ove", "uv"],
    ]

    prefixes = [
        "OwO",
        "OwO *what's this?*",
        "*blushes*",
    ]

    def create_uwu_text(text: str) -> str:
        """
        Create UwU text from a given text.
        :param text: The text to UwU.
        :type text: str
        :return: The UwU text.
        :rtype: str
        """

        for src, dst in OwO.mappings:
            if src in text:
                text = text.replace(src, dst)
        text = f"{random.choice(OwO.prefixes)} {text}"
        text = f"{text} {random.choice(OwO.smileys)}"

        return text


class UwU(molter.MolterExtension):
    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="uwu",
        description="UwU a text.",
    )
    @interactions.option("The text to UwU.")
    async def _uwu(self, ctx: interactions.CommandContext, text: str):
        if len(text) > 1000:
            return await ctx.send("Text too long. Please try again.", ephemeral=True)

        res = OwO.create_uwu_text(text)
        await ctx.send(res)

    @molter.prefixed_command(name="uwu")
    async def _msg_uwu(self, ctx: molter.MolterContext, *, text: str):
        if len(text) > 1000:
            return await ctx.send("Text too long. Please try again.")

        res = OwO.create_uwu_text(text)
        await ctx.send(res)

    @interactions.extension_message_command(name="UwU-fier")
    async def _translate(self, ctx: interactions.CommandContext):
        text = ctx.target.content
        if len(text) > 1000:
            return await ctx.send("Text too long. Please try again.", ephemeral=True)

        res = OwO.create_uwu_text(text)
        await ctx.send(res)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    UwU(client)
    logging.debug("""[%s] Loaded Fun extension.""", log_time)
