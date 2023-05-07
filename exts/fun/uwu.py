"""
UwU related commands.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import random
import interactions
from interactions.ext.prefixed_commands import (
    prefixed_command,
    PrefixedContext,
)


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

    def create_uwu_text(self, text: str) -> str:
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


class UwU(interactions.Extension):
    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="uwu",
        description="UwU a text.",
    )
    @interactions.slash_option(
        name="text",
        description="The text to UwU.",
        opt_type=interactions.OptionType.STRING,
        required=True,
        max_length=700,
    )
    async def uwu(self, ctx: interactions.SlashContext, text: str) -> None:
        """UwU a text."""

        res = OwO.create_uwu_text(self, text)
        await ctx.send(res)

    @prefixed_command(name="uwu")
    async def _uwu(self, ctx: PrefixedContext, *, text: str) -> None:
        """UwU a text."""

        res = OwO.create_uwu_text(self, text)
        await ctx.send(res)

    @interactions.context_menu(
        name="UwU-fier",
        context_type=interactions.CommandType.MESSAGE,
    )
    async def uwu_fier(self, ctx: interactions.InteractionContext) -> None:
        """Context menu of UwU command."""

        text: interactions.Message = ctx.target
        if len(text.content) > 1000:
            return await ctx.send(
                "Text too long. Please try again.", ephemeral=True
            )

        res = OwO.create_uwu_text(self, text=text.content)
        await ctx.send(res)


def setup(client) -> None:
    """Setup the extension."""
    UwU(client)
    logging.info("Loaded UwU extension.")