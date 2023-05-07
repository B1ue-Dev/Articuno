"""
Error system handler.

(C) 2022-2023 - B1ue-Dev
"""

import datetime
import traceback
import interactions
from const import LOG_CHANNEL


class Error(interactions.Extension):
    """on_command_error callback."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.log_channel: int = LOG_CHANNEL

    @interactions.listen()
    async def on_command_error(
        self,
        ctx: interactions.events.CommandError,
    ) -> None:
        """For CommandError callback."""

        if not isinstance(ctx.ctx, interactions.SlashContext):
            return

        _ctx: interactions.SlashContext = ctx.ctx

        error_time = datetime.datetime.utcnow().timestamp()

        error: Exception = ctx.error
        traceb2 = traceback.format_exception(
            type(error),
            value=error,
            tb=error.__traceback__,
            limit=1000,
        )
        traceb = "".join(traceb2)
        traceb = traceb.replace("`", "")
        traceb = traceb.replace("\\n", "\n")
        traceb = traceb.replace("\\t", "\t")
        traceb = traceb.replace("\\r", "\r")
        traceb = traceb.replace("\\", "/")
        er = ""
        for i in traceb:
            er = er + f"{i}"

        embed = interactions.Embed(
            title="**Uh oh...**",
            description="".join(
                [
                    "An error occurred. The developer team is dealing with the ",
                    " problem now.\nHave any question? ",
                    "Join the [**support server**](https://discord.gg/ndy95mBfJs)",
                    " for more help.",
                ]
            ),
            color=0xED4245,
            fields=[
                interactions.EmbedField(
                    name="Error",
                    value=f"```py\n{type(error).__name__}: {error}\n```",
                ),
            ],
        )

        await _ctx.send(embeds=embed, ephemeral=True)

        log_channel = self.client.get_channel(self.log_channel)
        command_name: str = _ctx.command.name
        subcommand_name: str = None
        if _ctx.command.is_subcommand:
            subcommand_name = _ctx.command.to_dict().get("name")
        full_command = f"""{command_name}{" " + subcommand_name if subcommand_name else ""}"""

        log_error = interactions.Embed(
            title="An error occurred!",
            description="".join(
                [
                    f"""Caused by **/{full_command}**\n""",
                    f"Author: {_ctx.user.username}#{_ctx.user.discriminator} ``{_ctx.user.id}``\n",
                    f"Guild: {_ctx.guild.name} ``{_ctx.guild.id}``\n",
                    f"Occurred on: <t:{round(error_time)}:F>",
                ]
            ),
            color=0xED4245,
            fields=[
                interactions.EmbedField(
                    name="Traceback",
                    value=f"```\n{traceb}\n```"
                    if len(traceb) < 1024
                    else f"```\n...{traceb[-1000:]}\n```",
                )
            ],
        )

        await log_channel.send(embeds=log_error)
