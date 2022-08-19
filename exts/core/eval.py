"""
Eval command.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import io
import textwrap
import inspect
import contextlib
import traceback
import asyncio
from typing import List
import interactions
from interactions.ext.paginator import Page, Paginator


def page_paginator(text: str) -> List[str]:
    """
    This function takes a string and splits it into chunks of 1000 characters.

    :param text: The string to split.
    :type text: str
    :return: A list of strings.
    :rtype: list
    """

    last = 0
    pages = []
    for curr in range(0, len(text)):
        if curr % 1000 == 0:
            pages.append(text[last:curr])
            last = curr
            appd_index = curr
    if appd_index != len(text)-1:
        pages.append(text[last:curr])
    return list(filter(lambda a: a != '', pages))


class Eval(interactions.Extension):
    """Extension for /eval command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="eval",
        description="Evaluates some code.",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="code",
                description="Code to evaluate.",
                required=True
            )
        ]
    )
    async def _eval(self, ctx: interactions.CommandContext, code: str):
        """Evaluates some code."""

        if int(ctx.user.id) != 892080548342820925:
            return await ctx.send("You must be the bot owner to use this command. Also, no.")

        await ctx.defer()

        env = {
            'ctx': ctx,
            'channel': await ctx.get_channel(),
            'author': ctx.author,
            'user': ctx.user,
            'guild': await ctx.get_guild(),
            'message': ctx.message,
            'source': inspect.getsource,
            'interactions': interactions,
            'client': self.client,
            'self.client': self.client,
        }

        env.update(globals())
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(code, "  ")}'
        try:
            exec(to_compile, env)
        except Exception:
            return await ctx.send(f'```py\n{traceback.format_exc()}\n```')

        func = env['func']
        try:
            with contextlib.redirect_stdout(stdout):
                await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if value and len(value) < 1001:
                await ctx.send(f'```py\n{value}\n```')

            elif value and len(value) > 0:
                out_pages = page_paginator(value)
                pag_pages = []
                for page in out_pages:
                    pag_pages.append(Page(f"```py\n{page}```"))
                await Paginator(
                    client=self.client,
                    ctx=ctx,
                    pages=pag_pages,
                    timeout=12,
                    use_select=False,
                    remove_after_timeout=True
                ).run()

            else:
                await ctx.send(f"```py\nNone\n```", ephemeral=True)

    @interactions.extension_listener(name="on_message_create")
    async def _message_create(self, message: interactions.Message):
        channel = await message.get_channel()
        if message.content.startswith("$eval"):
            if int(message.author.id) != 892080548342820925:
                return await channel.send("You must be the bot owner to use this command. Also, no.")

            ends = int(len(message.content) - 6)
            code = str(message.content)[-ends:]

            env = {
                'ctx': channel,
                'channel': channel,
                'author': message.author,
                'user': interactions.User(**await self.client._http.get_user(int(message.author.id)), _client=self.client._http),
                'guild': await message.get_guild(),
                'message': message,
                'source': inspect.getsource,
                'interactions': interactions,
                'client': self.client,
                'self.client': self.client,
            }

            env.update(globals())
            stdout = io.StringIO()

            to_compile = f'async def func():\n{textwrap.indent(code, "  ")}'
            try:
                exec(to_compile, env)
            except Exception:
                return await channel.send(f'```py\n{traceback.format_exc()}\n```')

            func = env['func']
            try:
                with contextlib.redirect_stdout(stdout):
                    await func()
            except Exception:
                value = stdout.getvalue()
                return await channel.send(f'```py\n{value}{traceback.format_exc()}\n```')
            else:
                value = stdout.getvalue()
                if value and len(value) < 1001:
                    await channel.send(f'```py\n{value}\n```')
                elif value:
                    file = io.StringIO(value)
                    with file as f:
                        file = interactions.File(filename='output.txt', fp=f)
                        await channel.send(f'```py\n{value[:200]}...\n```', files=file)
                else:
                    await channel.send(f"```py\nNone\n```")


    @interactions.extension_command(
        name="shell",
        description="Runs a shell command.",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="command",
                description="The command to run.",
                required=True
            )
        ]
    )
    async def _shell(self, ctx: interactions.CommandContext, command: str):
        """Runs a shell command."""

        await ctx.defer()
        if int(ctx.author.id) != 892080548342820925:
            return await ctx.send("You must be the bot owner to use this command. Also, no.")

        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.wait()

        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10)
        out = stdout.decode() if stdout else stderr.decode()
        if len(out) == 0:
            return await ctx.send(f"```sh\n$ {command}\nReturn code {proc.returncode};\n```")
        if len(out) > 0 and len(out) < 1001:
            return await ctx.send(f"```sh\n$ {command}\n\n{out}\n\nReturn code {proc.returncode};\n```")
        out_pages = page_paginator(out)
        pag_pages = []
        for page in out_pages:
            pag_pages.append(Page(f"```sh\n$ {command}\n\n{page}\n\nReturn code {proc.returncode};\n```"))
        await Paginator(
            client=self.client,
            ctx=ctx,
            pages=pag_pages,
            timeout=10,
            use_select=False,
            remove_after_timeout=True
        ).run()


def setup(client) -> None:
    """Setup the extension."""
    log_time = (
        datetime.datetime.now() + datetime.timedelta(hours=7)
    ).strftime("%d/%m/%Y %H:%M:%S")
    Eval(client)
    logging.debug("""[%s] Loaded Eval extension.""", log_time)
    print(f"[{log_time}] Loaded Eval extension.")
