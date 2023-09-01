"""
jsk-based command.

(C) 2022-2023 - B1ue-Dev
"""

import io
import asyncio
import platform
import sys
import textwrap
import inspect
import contextlib
import traceback
import typing
from datetime import datetime
from interactions.ext.prefixed_commands import (
    prefixed_command,
    PrefixedContext,
)
import psutil
import interactions
from interactions.ext.paginators import Paginator
from interactions.ext.debug_extension.utils import get_cache_state
from src.utils import utils
from src.const import VERSION


class _Jsk:
    """Static class for jsk data."""

    uptime: datetime = round(datetime.now().timestamp())
    """The start time of the bot."""
    ipy: str = interactions.__version__
    """The interactions.py version."""
    py: str = platform.python_version()
    """The Python version."""
    platf: str = platform.platform()
    """The system name."""
    _py: str = sys.version
    """The full Python version."""
    _platf: str = sys.platform
    """The core system name."""


def cleanup_code(content: str) -> str:
    """Automatically removes code blocks from the code."""

    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])

    return content.strip("` \n")


class Jsk(interactions.Extension):
    """Extension for jsk-based command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @prefixed_command()
    async def jsk(self, ctx: PrefixedContext) -> None:
        """Get basic information about the bot."""

        if int(ctx.user.id) != int(self.client.owner.id):
            return await ctx.send(
                "You must be the bot owner to perform this action."
            )

        proc: "psutil.Process" = psutil.Process()
        rss_mem: str = f"{utils.natural_size(proc.memory_full_info().rss)}"
        vms_mem: str = f"{utils.natural_size(proc.memory_full_info().vms)}"
        cpu_perc: str = f"{psutil.cpu_percent()}%"
        threads: str = f"{proc.num_threads()} Threads"
        pid: int = proc.pid
        name: str = proc.name()
        latency = f"{self.client.latency * 1000:.0f}ms"
        guild_count: str = str(len(self.client.guilds))
        user_count: int = 0
        for guild in self.client.guilds:
            user_count += guild.member_count

        text: str = "".join(
            [
                f"{self.client.user.username} `{VERSION}` - interactions.py `{_Jsk.ipy}`, ",
                f"Python `{_Jsk.py}` on `{_Jsk.platf}`.\n",
                f"This bot was loaded {utils.pretty_date(_Jsk.uptime)}.\n\n",
                f"Using {rss_mem} physical memory and {vms_mem} virual memory.\n",
                f"Running on PID {pid} ({name}) with {threads}, at ",
                f"{cpu_perc} CPU.\n\n",
                f"{self.client.user.username} can see {guild_count} guilds and {user_count} users.\n",
                f"Websocket latency: {latency}.",
            ]
        )

        await ctx.send(content=text)

    @jsk.subcommand()
    async def cache(self, ctx: PrefixedContext) -> None:
        """Shows the current cache."""

        await ctx.send(f"```\n{get_cache_state(self.client)}\n```")

    @jsk.subcommand()
    async def shutdown(self, ctx: PrefixedContext) -> None:
        """Shuts down the bot."""

        await ctx.reply("💤 Shutting down...")
        await self.client.stop()

    @jsk.subcommand()
    async def reload(self, ctx: PrefixedContext, module: str) -> None:
        """Reloads an extension."""

        if module in ["~", "."]:
            msg = await ctx.send("Reloading all extensions...")
            _msg: str = ""
            for ext in (
                e.extension_name for e in self.client.ext.copy().values()
            ):
                await asyncio.sleep(0.8)
                try:
                    _msg += f"🔀 {ext}\n"
                    self.client.reload_extension(ext)
                except Exception:
                    _msg += f"⚠ {ext}\n"
                    continue
                await msg.edit(content=f"{_msg}")
            await msg.add_reaction("✅")
        else:
            self.client.reload_extension(module)
            await ctx.reply(f"🔀 Reloaded `{module}`.")

    @jsk.subcommand()
    async def load(self, ctx: PrefixedContext, module: str) -> None:
        """Loads an extension."""

        if module in ["~", "."]:
            msg = await ctx.send("Loading all extensions...")
            _msg: str = ""
            for ext in (
                e.extension_name for e in self.client.ext.copy().values()
            ):
                await asyncio.sleep(0.8)
                try:
                    _msg += f"📥 {ext}\n"
                    self.client.load_extension(ext)
                except Exception:
                    _msg += f"⚠ {ext}\n"
                    continue
                await msg.edit(content=f"{_msg}")
            await msg.add_reaction("✅")
        else:
            self.client.load_extension(module)
            await ctx.reply(f"📥 Loaded `{module}`.")

    @jsk.subcommand()
    async def unload(self, ctx: PrefixedContext, module: str) -> None:
        """Unloads an extension."""

        if module in ["~", "."]:
            msg = await ctx.send("Unloading all extensions...")
            _msg: str = ""
            for ext in (
                e.extension_name for e in self.client.ext.copy().values()
            ):
                await asyncio.sleep(0.8)
                try:
                    _msg += f"📤 {ext}\n"
                    self.client.unload_extension(ext)
                except Exception:
                    _msg += f"⚠ {ext}\n"
                    continue
                await msg.edit(content=f"{_msg}")
            await msg.add_reaction("✅")
        else:
            self.client.unload_extension(module)
            await ctx.reply(f"📤 Unloaded `{module}`.")

    @jsk.subcommand()
    async def eval(self, ctx: PrefixedContext, *, code: str) -> None:
        """Evaluates code."""

        if int(ctx.user.id) != 892080548342820925:
            return await ctx.send(
                "You must be the bot owner to perform this action."
            )
        if isinstance(ctx.channel, interactions.GuildText):
            await ctx.channel.trigger_typing()

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

    @jsk.subcommand()
    async def shell(self, ctx: PrefixedContext, *, cmd: str) -> None:
        """Executes statements in the system shell."""

        if int(ctx.user.id) != int(self.client.owner.id):
            return await ctx.send(
                "You must be the bot owner to perform this action."
            )

        async with ctx.channel.typing:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )

            output, _ = await process.communicate()
            output_str = output.decode("utf-8")
            output_str += f"\nReturn code {process.returncode}"

        if len(output_str) <= 2000:
            return await ctx.message.reply(f"```sh\n{output_str}```")

        paginator = Paginator.create_from_string(
            self.client,
            output_str,
            prefix="```sh",
            suffix="```",
            page_size=4000,
        )
        return await paginator.reply(ctx)

    async def handle_exec_result(
        self,
        ctx: typing.Union[PrefixedContext, interactions.SlashContext],
        result: typing.Any,
        value: typing.Any,
    ) -> interactions.Message:
        """Handles stdout result."""

        if result is None:
            result = value or "No Output."

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
