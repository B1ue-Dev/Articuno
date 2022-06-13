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
from interactions.ext.paginator import Page, Paginator
from const import OWNER_ID


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
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.extension_command(
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
    async def _eval(self, ctx: interactions.CommandContext, code: str):
        if str(ctx.user.id) != str(OWNER_ID):
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

        value = stdout.getvalue()
        if value and len(value) < 1001:
            await ctx.send(f'```py\n>>> {code}\n{value}\n```')
        elif value:
            out_pages = page_paginator(value)
            pag_pages = []
            for page in out_pages:
                pag_pages.append(Page(f"```py\n{page}```"))
            await Paginator(
                client=self.client,
                ctx=ctx,
                pages=pag_pages,
                timeout=10,
                use_select=False,
                remove_after_timeout=True
            ).run()


def setup(client):
    Eval(client)
