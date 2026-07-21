"""
jsk-based command.

(C) 2022-2026 - B1ue-Dev
"""

import io
import asyncio
import platform
import sys
import textwrap
import inspect
import contextlib
import traceback
import time
import typing
from datetime import datetime
from interactions.ext.prefixed_commands import (
    prefixed_command,
    PrefixedContext,
)
import psutil
import interactions
from interactions import check, is_owner
from interactions.ext.paginators import Paginator
from interactions.ext.debug_extension.utils import get_cache_state, debug_embed
from src.common import utils
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
    @check(is_owner())
    async def jsk(self, ctx: PrefixedContext) -> None:
        """Get basic information about the bot."""

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
    @check(is_owner())
    async def cache(self, ctx: PrefixedContext) -> None:
        """Shows the current cache."""

        await ctx.send(f"```\n{get_cache_state(self.client)}\n```")

    @jsk.subcommand()
    @check(is_owner())
    async def shutdown(self, ctx: PrefixedContext) -> None:
        """Shuts down the bot."""

        await ctx.reply("💤 Shutting down...")
        await self.client.stop()

    @jsk.subcommand(aliases=["r"])
    @check(is_owner())
    async def reload(self, ctx: PrefixedContext, module: str) -> None:
        """Reloads an extension."""

        if module in ["~", "."]:
            msg = await ctx.send("Reloading all extensions...")
            _msg: str = ""
            for ext in (e.extension_name for e in self._exts):
                await asyncio.sleep(0.8)
                try:
                    if "jsk" in ext or "error_handler" in ext:
                        pass
                    else:
                        _msg += f"🔀 `{ext}`\n"
                        self.client.reload_extension(ext)
                except Exception:
                    _msg += f"⚠ `{ext}`\n"
                    continue
                await msg.edit(
                    content=f"Reloading all extensions...\n\n{_msg}"
                )
            await msg.add_reaction("✅")
        else:
            self.client.reload_extension(module)
            await ctx.reply(f"🔀 Reloaded `{module}`.")

    @jsk.subcommand(aliases=["l"])
    @check(is_owner())
    async def load(self, ctx: PrefixedContext, module: str) -> None:
        """Loads an extension."""

        try:
            self.client.load_extension(module)
            await ctx.message.add_reaction("✅")
            await ctx.reply(f"📤 Loaded `{module}`.")
        except Exception:
            await ctx.message.add_reaction("❌")
            await ctx.reply(f"⚠ Error in loading `{module}`.")

    @jsk.subcommand(aliases=["u"])
    @check(is_owner())
    async def unload(self, ctx: PrefixedContext, module: str) -> None:
        """Unloads an extension."""

        try:
            self.client.unload_extension(module)
            await ctx.message.add_reaction("✅")
            await ctx.reply(f"📤 Unloaded `{module}`.")
        except Exception:
            await ctx.message.add_reaction("❌")
            await ctx.reply(f"⚠ Error in unloading `{module}`.")

    @jsk.subcommand(aliases=["e", "py"])
    @check(is_owner())
    async def eval(self, ctx: PrefixedContext, *, body: str) -> None:
        """Evaluates code."""

        if isinstance(ctx.channel, interactions.GuildText):
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

        body = (
            "\n".join(body.split("\n")[1:-1])
            if body.startswith("```") and body.endswith("```")
            else body.strip("` \n")
        )

        stdout = io.StringIO()

        to_compile = f"async def func():\n{textwrap.indent(body, '  ')}"
        try:
            exec(to_compile, env)  # noqa: S102
        except SyntaxError:
            return await ctx.reply(f"```py\n{traceback.format_exc()}\n```")

        func = env["func"]
        try:
            with contextlib.redirect_stdout(stdout):
                ret = await func()
        except Exception:
            await ctx.message.add_reaction("❌")
            raise
        else:
            return await self.handle_exec_result(ctx, ret, stdout.getvalue())

    @jsk.subcommand(aliases=["sh"])
    @check(is_owner())
    async def shell(self, ctx: PrefixedContext, *, cmd: str) -> None:
        """Executes statements in the system shell."""

        msg = await ctx.send("⏳ Running shell command...")

        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        output_lines = []
        last_update_time = time.monotonic()

        while True:
            line = await process.stdout.readline()
            if not line:
                break

            output_lines.append(line.decode("utf-8"))

            now = time.monotonic()
            if now - last_update_time >= 5:
                preview_output = "".join(output_lines)[-1900:]
                try:
                    await msg.edit(content=f"```sh\n{preview_output}```")
                except Exception:
                    pass
                last_update_time = now

        # Wait for the process to fully complete
        return_code = await process.wait()
        output_lines.append(
            f"\n\n[✅ Command finished — Return code {return_code}]"
        )
        final_output = "".join(output_lines)

        # Send final output
        if len(final_output) > 2000:
            paginator = Paginator.create_from_string(
                self.client,
                final_output,
                prefix="```sh",
                suffix="```",
                page_size=4000,
            )
            return await paginator.reply(ctx)

        return await msg.edit(content=f"```sh\n{final_output}```")

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

        if isinstance(result, interactions.Message):
            try:
                e = debug_embed(
                    "Exec", timestamp=result.created_at, url=result.jump_url
                )
                e.description = result.content
                e.set_author(
                    result.author.tag,
                    icon_url=result.author.display_avatar.url,
                )
                e.add_field(
                    "\u200b",
                    f"[Jump To]({result.jump_url})\n{result.channel.mention}",
                )

                return await ctx.message.reply(embeds=e)
            except Exception:
                return await ctx.message.reply(result.jump_url)

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
