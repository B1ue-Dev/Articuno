"""
/eval command.

(C) 2022-2023 - B1ue-Dev
"""

import io
import textwrap
import inspect
import contextlib
import traceback
import logging
import asyncio
import interactions
from interactions.ext.paginators import Paginator
from interactions.ext.prefixed_commands import (
    prefixed_command,
    PrefixedContext,
)


class Eval(interactions.Extension):
    """Extension for /eval command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="eval",
        description="Evaluates some code.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="code",
                description="Code to evaluate.",
                required=True,
            )
        ],
    )
    async def eval(
        self, ctx: interactions.InteractionContext, code: str
    ) -> None:
        """Evaluates some code."""

        if int(ctx.user.id) != 892080548342820925:
            return await ctx.send(
                "You must be the bot owner to use this command. Also, no."
            )

        await ctx.defer()

        env = {
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "user": ctx.user,
            "guild": ctx.guild,
            "message": ctx.message,
            "source": inspect.getsource,
            "interactions": interactions,
            "client": self.client,
            "self.client": self.client,
        }

        env.update(globals())
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(code, "  ")}'
        try:
            exec(to_compile, env)
        except Exception:
            return await ctx.send(f"{traceback.format_exc()}")

        func = env["func"]
        try:
            with contextlib.redirect_stdout(stdout):
                await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f"{value}{traceback.format_exc()}")
        else:
            value = stdout.getvalue()
            if value and len(value) < 1001:
                await ctx.send(f"{value}")

            elif value and len(value) > 0:
                paginator = Paginator.create_from_string(
                    self.client,
                    content=value,
                    page_size=2000,
                )

                await paginator.send(ctx)
            else:
                await ctx.send("None", ephemeral=True)

    @prefixed_command(name="eval")
    async def _eval(self, ctx: PrefixedContext, *, code: str) -> None:
        """Evaluates some code."""

        if int(ctx.author.id) != 892080548342820925:
            return await ctx.send(
                "You must be the bot owner to use this command. Also, no."
            )

        env = {
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.message.author,
            "user": ctx.message.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "source": inspect.getsource,
            "interactions": interactions,
            "client": self.client,
            "self.client": self.client,
        }

        env.update(globals())
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(code, "  ")}'
        try:
            exec(to_compile, env)
        except Exception:
            return await ctx.send(f"{traceback.format_exc()}")

        func = env["func"]
        try:
            with contextlib.redirect_stdout(stdout):
                await func()
        except Exception:
            value = stdout.getvalue()
            return await ctx.send(f"{value}{traceback.format_exc()}")
        else:
            value = stdout.getvalue()
            if value and len(value) < 1001:
                await ctx.send(f"{value}")

            elif value and len(value) > 0:
                paginator = Paginator.create_from_string(
                    self.client,
                    content=value,
                    page_size=2000,
                )

                await paginator.send(ctx)
            else:
                await ctx.send("None", ephemeral=True)

    @interactions.slash_command(
        name="shell",
        description="Runs a shell command.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="command",
                description="The command to run.",
                required=True,
            )
        ],
    )
    async def shell(
        self, ctx: interactions.InteractionContext, command: str
    ) -> None:
        """Runs a shell command."""

        await ctx.defer()
        if int(ctx.author.id) != 892080548342820925:
            return await ctx.send(
                "You must be the bot owner to use this command. Also, no."
            )

        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.wait()

        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10)
        out = stdout.decode() if stdout else stderr.decode()
        if len(out) == 0:
            return await ctx.send(
                f"```sh\n$ {command}\nReturn code {proc.returncode};\n```"
            )
        if len(out) > 0 and len(out) < 1001:
            return await ctx.send(
                f"```sh\n$ {command}\n\n{out}\n\nReturn code {proc.returncode};\n```"
            )

        paginator = Paginator.create_from_string(
            self.client,
            content=out,
            page_size=2000,
        )

        await paginator.send(ctx)


def setup(client) -> None:
    """Setup the extension."""
    Eval(client)
    logging.info("Loaded Eval extension.")
