"""
Eval command.

(C) 2022-2023 - Jimmy-Blue
"""

import logging
import datetime
import io
import string
import re
import textwrap
import inspect
import contextlib
import traceback
import asyncio
import interactions
from interactions.ext.paginators import Paginator
from interactions.ext.prefixed_commands import prefixed_command, PrefixedContext


def page_paginator(text: str) -> list[str]:
    """
    This function takes a string and splits it into chunks of 1000 characters.

    :param text: The string to split.
    :type text: str
    :return: A list of strings.
    :rtype: list
    """

    words = [
        re.sub("^[{0}]+|[{0}]+$".format(string.punctuation), "", w)
        for w in text.split()
    ]
    pages = []
    s = ""
    for i in range(len(words)):
        if len(s) < 1000:
            if i == len(words) - 1:
                s += f"{words[i]} "
                pages.append(s)
            else:
                s += f"{words[i]} "
        else:
            pages.append(s)
            s = ""
            if i == len(words) - 1:
                s += f"\n{words[i]} "
                pages.append(s)
            else:
                s += f"\n{words[i]} "
    return pages


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
    async def eval(self, ctx: interactions.InteractionContext, code: str) -> None:
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
            return await ctx.send(f"```py\n{traceback.format_exc()}\n```")

        func = env["func"]
        try:
            with contextlib.redirect_stdout(stdout):
                await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            if value and len(value) < 1001:
                await ctx.send(f"```py\n{value}\n```")

            elif value and len(value) > 0:
                out_pages = page_paginator(value)
                pag_pages = []
                for page in out_pages:
                    pag_pages.append(f"```py\n{page}\n```")

                paginator = Paginator.create_from_list(
                    self.client,
                    content=pag_pages,
                    page_size=2000,
                )

                await paginator.send(ctx)
            else:
                await ctx.send("```py\nNone\n```", ephemeral=True)

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
            return await ctx.send(f"```py\n{traceback.format_exc()}\n```")

        func = env["func"]
        try:
            with contextlib.redirect_stdout(stdout):
                await func()
        except Exception:
            value = stdout.getvalue()
            return await ctx.send(
                f"```py\n{value}{traceback.format_exc()}\n```"
            )
        else:
            value = stdout.getvalue()
            if value and len(value) < 1001:
                await ctx.send(f"```py\n{value}\n```")

            elif value and len(value) > 0:
                out_pages = page_paginator(value)
                pag_pages = []
                for page in out_pages:
                    pag_pages.append(f"```py\n{page}\n```")

                paginator = Paginator.create_from_list(
                    self.client,
                    content=pag_pages,
                    page_size=2000,
                )

                await paginator.send(ctx)
            else:
                await ctx.send("```py\nNone\n```", ephemeral=True)

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
    async def shell(self, ctx: interactions.InteractionContext, command: str) -> None:
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
        out_pages = page_paginator(out)
        pag_pages = []
        for page in out_pages:
            pag_pages.append(
                f"```sh\n$ {command}\n\n{page}\n\nReturn code {proc.returncode};\n```"
            )

        paginator = Paginator.create_from_list(
            self.client,
            content=pag_pages,
            page_size=2000,
        )

        await paginator.send(ctx)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Eval(client)
    logging.debug("""[%s] Loaded Eval extension.""", log_time)
