"""
Random base64, brainfuck commands.

(C) 2022-2023 - B1ue-Dev
"""

import base64 as b64
import binascii
import interactions
from utils import brainfuck


class HackTool(interactions.Extension):
    """Extension for random tech tool command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.slash_command(name="base64")
    async def base64(self, ctx: interactions.SlashContext) -> None:
        """Base64 commands."""
        ...

    @base64.subcommand()
    @interactions.slash_option(
        name="string",
        description="The string you want to encode",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def encode(
        self, ctx: interactions.SlashContext, string: str
    ) -> None:
        """Encodes a string using base64."""

        string_message = string
        string_bytes = string_message.encode("utf-8")
        base64_bytes = b64.b64encode(string_bytes)
        base64_string = base64_bytes.decode("utf-8")
        await ctx.send(f"```{base64_string}```")

    @base64.subcommand()
    @interactions.slash_option(
        name="string",
        description="The string you want to decode",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def decode(
        self, ctx: interactions.SlashContext, string: str
    ) -> None:
        """Decodes a string using base64."""

        string_message = string
        string_bytes = string_message.encode("utf-8")
        try:
            base64_bytes = b64.b64decode(string_bytes)
            base64_string = base64_bytes.decode("utf-8")
            await ctx.send(f"```{base64_string}```")
        except binascii.Error:
            await ctx.send(
                "```Invalid string. Please try again!```", ephemeral=True
            )

    @interactions.slash_command(name="brainfuck")
    async def brainfuck(self, ctx: interactions.SlashContext) -> None:
        """Brainfuck commands."""
        ...

    @brainfuck.subcommand()
    @interactions.slash_option(
        name="string",
        description="The string to convert",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def convert(
        self, ctx: interactions.SlashContext, string: str
    ) -> None:
        """Converts a string into brainfuck code."""

        string_bytes = brainfuck.Brainfuckery().convert(string)
        await ctx.send(f"```{string_bytes}```")

    @brainfuck.subcommand()
    @interactions.slash_option(
        name="code",
        description="The code to interpret",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def interpret(
        self, ctx: interactions.SlashContext, code: str
    ) -> None:
        """Interprets a brainfuck code."""

        string_bytes = brainfuck.Brainfuckery().interpret(code)
        await ctx.send(f"```{string_bytes}```")
