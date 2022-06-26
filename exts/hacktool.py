"""
This is for base64, brainfuck commands.

(C) 2022 - Jimmy-Blue
"""

import base64 as b64
import binascii
import interactions
from utils import brainfuck


class HackTool(interactions.Extension):
    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot

    @interactions.extension_command(
        name="base64",
        description="Base64 tools",
        options=[
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="encode",
                description="Encode a string",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="string",
                        description="String to encode",
                        required=True
                    )
                ]
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="decode",
                description="Decode a string",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="string",
                        description="String to decode",
                        required=True
                    )
                ]
            )
        ]
    )
    async def _base64(self, ctx: interactions.CommandContext, sub_command: str, string: str):
        if sub_command == "encode":
            string_message = string
            string_bytes = string_message.encode("utf-8")
            base64_bytes = b64.b64encode(string_bytes)
            base64_string = base64_bytes.decode("utf-8")
            await ctx.send(f"```{base64_string}```")
        elif sub_command == "decode":
            string_message = string
            string_bytes = string_message.encode("utf-8")
            try:
                base64_bytes = b64.b64decode(string_bytes)
                base64_string = base64_bytes.decode("utf-8")
                await ctx.send(f"```{base64_string}```")
            except binascii.Error:
                await ctx.send("```Invalid string. Please try again!```", ephemeral=True)


    @interactions.extension_command(
        name="brainfuck",
        description="Brainfuck interpreter/converter",
        options=[
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="convert",
                description="Convert a string to brainfuck code",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="string",
                        description="String to convert",
                        required=True
                    )
                ]
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="interpret",
                description="Interpret a brainfuck code",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="code",
                        description="Brainfuck code to interpret",
                        required=True
                    )
                ]
            )
        ]
    )
    async def _brainfuck(self, ctx: interactions.CommandContext, sub_command: str, string: str = None, code: str = None):
        if sub_command == "convert":
            string_bytes = brainfuck.Brainfuckery().convert(string)
            await ctx.send(f"```{string_bytes}```")
        elif sub_command == "interpret":
            string_bytes = brainfuck.Brainfuckery().interpret(code)
            await ctx.send(f"```{string_bytes}```")


def setup(bot):
    HackTool(bot)
