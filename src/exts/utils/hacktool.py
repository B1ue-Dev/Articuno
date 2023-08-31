"""
Random base64, brainfuck commands.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import base64 as b64
import binascii
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_subcommand,
    HybridContext,
)
from src.utils import brainfuck, utils


class HackTool(interactions.Extension):
    """Extension for random tech tool command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @hybrid_slash_subcommand(
        base="base64",
        base_description="Base64 commands.",
        name="encode",
        description="Encodes a string using base64.",
    )
    @interactions.slash_option(
        name="string",
        description="The string you want to encode",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def encode(self, ctx: HybridContext, string: str) -> None:
        """Encodes a string using base64."""

        string_message = string
        string_bytes = string_message.encode("utf-8")
        base64_bytes = b64.b64encode(string_bytes)
        base64_string = base64_bytes.decode("utf-8")
        if len(base64_string) < 1024:
            await ctx.send(f"```{base64_string}```")
        else:
            _io = utils.send_as_file(base64_string)
            await ctx.send(
                content="Too long. Sent by text file instead.",
                file=interactions.File(
                    file=_io,
                    file_name="encoded.txt",
                    description="The encoded content.",
                ),
            )

    @hybrid_slash_subcommand(
        base="base64",
        base_description="Base64 commands.",
        name="decode",
        description="Decodes a string using base64.",
    )
    @interactions.slash_option(
        name="string",
        description="The string you want to decode",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def decode(self, ctx: HybridContext, string: str) -> None:
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

    @hybrid_slash_subcommand(
        base="brainfuck",
        base_description="Brainfuck commands.",
        name="convert",
        description="Converts a string into brainfuck code.",
    )
    @interactions.slash_option(
        name="string",
        description="The string to convert",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def convert(self, ctx: HybridContext, string: str) -> None:
        """Converts a string into brainfuck code."""

        string_bytes = brainfuck.Brainfuckery().convert(string)
        if len(string_bytes) < 1024:
            await ctx.send(f"```{string_bytes}```")
        else:
            _io = utils.send_as_file(string_bytes)
            await ctx.send(
                content="Too long. Sent by text file instead.",
                file=interactions.File(
                    file=_io,
                    file_name="encoded.txt",
                    description="The encoded content.",
                ),
            )

    @hybrid_slash_subcommand(
        base="brainfuck",
        base_description="Brainfuck commands.",
        name="interpret",
        description="Interprets a brainfuck code.",
    )
    @interactions.slash_option(
        name="code",
        description="The code to interpret",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def interpret(self, ctx: HybridContext, code: str) -> None:
        """Interprets a brainfuck code."""

        string_bytes = brainfuck.Brainfuckery().interpret(code)
        await ctx.send(f"```{string_bytes}```")


def setup(client) -> None:
    """Setup the extension."""

    HackTool(client)
    logging.info("Loaded HackTool extension.")
