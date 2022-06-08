"""
This module is for eval command.

(C) 2022 - Jimmy-Blue
"""

import io
import textwrap
import inspect
import contextlib
import traceback
import asyncio
import interactions
from interactions import extension_command as command
from interactions.ext.paginator import Page, Paginator


def page_paginator(text: str):
    """
    This function takes a string and splits it into chunks of 1000 characters
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
    def __init__(self, bot):
        self.bot = bot


    @command(
        name='eval',
        description='Evaluates some code',
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="code",
                description="Code to evaluate",
                required=True
            )
        ]
    )
    async def _eval_paginator(self, ctx: interactions.CommandContext, code: str):
        if int(ctx.user.id) != 892080548342820925:
            return await ctx.send("You must be the bot owner to use this command. Also, no.")

        await ctx.defer()

        blocked_words = ['.delete()', 'os', 'subprocess', 'history()', '("token")', "('token')",
                        'aW1wb3J0IG9zCnJldHVybiBvcy5lbnZpcm9uLmdldCgndG9rZW4nKQ==', 'aW1wb3J0IG9zCnByaW50KG9zLmVudmlyb24uZ2V0KCd0b2tlbicpKQ==']
        for x in blocked_words:
            if x in code:
                return await ctx.send('Your code contains certain blocked words.', ephemeral=True)

        env = {
            'ctx': ctx,
            'channel': await ctx.get_channel(),
            'author': ctx.author,
            'user': ctx.user,
            'guild': await ctx.get_guild(),
            'message': ctx.message,
            'source': inspect.getsource,
            'interactions': interactions
        }

        env.update(globals())
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(code, "  ")}'
        try:
            exec(to_compile, env)
        except Exception:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
            return

        func = env['func']
        try:
            with contextlib.redirect_stdout(stdout):
                await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
            return
        else:
            value = stdout.getvalue()
            if value and len(value) < 1001:
                await ctx.send(f'```py\n>>> {code}\n{value}\n```')
            elif value:
                out_pages = page_paginator(value)
                pag_pages = []
                for page in out_pages:
                    pag_pages.append(Page(f"```py\n{page}```"))
                await Paginator(
                    client=self.bot,
                    ctx=ctx,
                    pages=pag_pages,
                    timeout=10,
                    use_select=False,
                    remove_after_timeout=True
                ).run()


    @interactions.extension_listener(name="on_message_create")
    async def _message_create(self, message: interactions.Message):
        channel = await message.get_channel()
        if message.content.startswith("$eval"):
            if int(message.author.id) != 892080548342820925:
                return await channel.send("You must be the bot owner to use this command. Also, no.")
            ends = int(len(message.content) - 6)
            code = str(message.content)[-ends:]
            blocked_words = ['.delete()', 'os', 'subprocess', 'history()', '("token")', "('token')",
                            'aW1wb3J0IG9zCnJldHVybiBvcy5lbnZpcm9uLmdldCgndG9rZW4nKQ==', 'aW1wb3J0IG9zCnByaW50KG9zLmVudmlyb24uZ2V0KCd0b2tlbicpKQ==']
            for x in blocked_words:
                if x in code:
                    return await channel.send('Your code contains certain blocked words.', ephemeral=True)

            env = {
                'ctx': channel,
                'channel': channel,
                'author': message.author,
                'user': interactions.User(**await self.bot._http.get_user(int(message.author.id)), _client=self.bot._http),
                'guild': await message.get_guild(),
                'message': message,
                'source': inspect.getsource,
                'interactions': interactions
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


    @command(
        name="shell",
        description="Runs a shell command",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="command",
                description="The command to run",
                required=True
            )
        ]
    )
    async def _shell(self, ctx: interactions.CommandContext, command: str):
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
            client=self.bot,
            ctx=ctx,
            pages=pag_pages,
            timeout=10,
            use_select=False,
            remove_after_timeout=True
        ).run()


def setup(bot):
    Eval(bot)
