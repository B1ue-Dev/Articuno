"""
This is for base64, brainfuck commands.

(C) 2022 - Jimmy-Blue
"""

import base64 as b64
import binascii
import interactions
from utils import brainfuck


class HackTool(interactions.Extension):
    """Extension for random tech tool command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(name="base64")
    async def _base64(self, *args, **kwargs):
        """Base64 commands."""
        ...

    @_base64.subcommand(name="encode")
    @interactions.option("The string you want to encode""")
    async def _base64_encode(self, ctx: interactions.CommandContext, string: str):
        """Encode a string using base64."""

        string_message = string
        string_bytes = string_message.encode("utf-8")
        base64_bytes = b64.b64encode(string_bytes)
        base64_string = base64_bytes.decode("utf-8")
        await ctx.send(f"```{base64_string}```")

    @_base64.subcommand(name="decode")
    @interactions.option("The string you want to decode")
    async def _base64_decode(self, ctx: interactions.CommandContext, string: str):
        """Decode a string using base64."""

        string_message = string
        string_bytes = string_message.encode("utf-8")
        try:
            base64_bytes = b64.b64decode(string_bytes)
            base64_string = base64_bytes.decode("utf-8")
            await ctx.send(f"```{base64_string}```")
        except binascii.Error:
            await ctx.send("```Invalid string. Please try again!```", ephemeral=True)

    @interactions.extension_command(name="brainfuck")
    async def _brainfuck(self, *args, **kwargs):
        """Brainfuck commands."""
        ...

    @_brainfuck.subcommand(name="convert")
    @interactions.option("The string to convert")
    async def _brainfuck_convert(self, ctx: interactions.CommandContext, string: str):
        """Convert a string into brainfuck code."""

        string_bytes = brainfuck.Brainfuckery().convert(string)
        await ctx.send(f"```{string_bytes}```")

    @_brainfuck.subcommand(name="interpret")
    @interactions.option("The code to interpret")
    async def _brainfuck_interpret(self, ctx: interactions.CommandContext, code: str):
        """Interpret a brainfuck code."""

        string_bytes = brainfuck.Brainfuckery().interpret(code)
        await ctx.send(f"```{string_bytes}```")


def setup(client) -> None:
    """Setup the extension."""
    log_time = (
        datetime.datetime.now() + datetime.timedelta(hours=7)
    ).strftime("%d/%m/%Y %H:%M:%S")
    HackTool(client)
    logging.debug("""[%s] Loaded HackTool extension.""", log_time)
    print(f"[{log_time}] Loaded HackTool extension.")
