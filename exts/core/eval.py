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
import typing
import interactions
from interactions.ext.paginators import Paginator
from interactions.ext.prefixed_commands import (
    prefixed_command,
    PrefixedContext,
)


def cleanup_code(content: str) -> str:
    """Automatically removes code blocks from the code."""

    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])

    return content.strip("` \n")


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

        code = cleanup_code(code)

        env = {
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "source": inspect.getsource,
            "interactions": interactions,
            "client": self.client,
            "self.client": self.client,
        } | globals()

        env.update(globals())
        stdout = io.StringIO()
        code = cleanup_code(code)

        to_compile = "async def func():\n%s" % textwrap.indent(code, "  ")
        try:
            exec(to_compile, env)
        except Exception:
            return await ctx.send(f"{traceback.format_exc()}")

        func = env["func"]
        try:
            with contextlib.redirect_stdout(stdout):
                ret = await func()
        except Exception:
            return await ctx.send(content=f"{traceback.format_exc()}")
        else:
            return await self.handle_exec_result(ctx, ret, stdout.getvalue())

    @prefixed_command(name="eval")
    async def _eval(self, ctx: PrefixedContext, *, code: str) -> None:
        """Evaluates some code."""

        if int(ctx.user.id) != 892080548342820925:
            return await ctx.send(
                "You must be the bot owner to use this command. Also, no."
            )

        await ctx.channel.trigger_typing()

        env = {
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "source": inspect.getsource,
            "interactions": interactions,
            "client": self.client,
            "self.client": self.client,
        } | globals()

        env.update(globals())
        stdout = io.StringIO()
        code = cleanup_code(code)

        to_compile = "async def func():\n%s" % textwrap.indent(code, "  ")
        try:
            exec(to_compile, env)
        except Exception:
            return await ctx.reply(f"{traceback.format_exc()}")

        func = env["func"]
        try:
            with contextlib.redirect_stdout(stdout):
                ret = await func()
        except Exception:
            await ctx.message.add_reaction("❌")
            return await ctx.reply(content=f"{traceback.format_exc()}")
        else:
            return await self.handle_exec_result(ctx, ret, stdout.getvalue())

    async def handle_exec_result(
        self,
        ctx: typing.Union[PrefixedContext, interactions.SlashContext],
        result: typing.Any,
        value: typing.Any,
    ) -> interactions.Message:
        """Handles stdout result."""

        if result is None:
            result = value or "No Output."

        # If result from prefixed message command.
        if isinstance(ctx, PrefixedContext):
            await ctx.message.add_reaction("✅")

            if isinstance(result, interactions.Embed):
                return await ctx.send(embeds=result)

            if isinstance(result, interactions.File):
                return await ctx.message.reply(file=result)

            if isinstance(result, Paginator):
                return await result.reply(ctx)

            if hasattr(result, "__iter__"):
                if all(isinstance(r, interactions.Embed) for r in result):
                    paginator = Paginator.create_from_embeds(
                        self.client,
                        *list(result),
                    )
                    return await paginator.reply(ctx)

            if not isinstance(result, str):
                result = repr(result)

            result = result.replace(self.client.http.token, "[REDACTED TOKEN]")

            if len(result) <= 2000:
                return await ctx.message.reply(f"```py\n{result}\n```")

            paginator = Paginator.create_from_string(
                self.client,
                result,
                prefix="```py",
                suffix="```",
                page_size=2000,
            )
            return await paginator.reply(ctx)

        # If the result is from slash command.
        elif isinstance(ctx, interactions.SlashContext):
            if isinstance(result, interactions.Embed):
                return await ctx.send(embeds=result)

            if isinstance(result, interactions.File):
                return await ctx.send(file=result)

            if isinstance(result, Paginator):
                return await result.send(ctx)

            if hasattr(result, "__iter__"):
                if all(isinstance(r, interactions.Embed) for r in result):
                    paginator = Paginator.create_from_embeds(
                        self.client,
                        *list(result),
                    )
                    return await paginator.send(ctx)

            if not isinstance(result, str):
                result = repr(result)

            result = result.replace(self.client.http.token, "[REDACTED TOKEN]")

            if len(result) <= 2000:
                return await ctx.message.send(f"```py\n{result}\n```")

            paginator = Paginator.create_from_string(
                self.client,
                result,
                prefix="```py",
                suffix="```",
                page_size=2000,
            )
            return await paginator.send(ctx)

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
