"""
Error system handler.

(C) 2022-2023 - B1ue-Dev
"""

import datetime
import traceback
import logging
import interactions
from interactions import models
from interactions.ext.prefixed_commands import PrefixedContext
from src.const import LOG_CHANNEL

debug_system: bool = False


def enableDebug(opt: bool):
    global debug_system
    debug_system = opt


async def handle_error(
    _client: interactions.Client,
    error: Exception,
    error_time: float,
    ctx: interactions.BaseContext = None,
) -> None:
    """
    Function to handle the error.

    :param error: The error traceback.
    :type error: Exception
    :param error_time: The time when the error occured.
    :type error_time: float
    :param ctx: The context of the error.
    :type ctx: interactions.BaseContext
    """

    traceb2 = traceback.format_exception(
        type(error),
        value=error,
        tb=error.__traceback__,
        limit=4088,
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

    logging.error(traceb)

    log_error = interactions.Embed(
        title="An error occurred!",
        color=0xED4245,
        description=f"```\n{traceb[-4000:]}\n```",
    )
    err_field = [
        interactions.EmbedField(
            name="Occurred on", value=f"<t:{round(error_time)}:F>", inline=True
        )
    ]
    if ctx:
        err_field.append(
            interactions.EmbedField(
                name="Author",
                value=f"{ctx.user.username}#{ctx.user.discriminator}\n``{ctx.user.id}``",
                inline=True,
            )
        )
        if ctx.guild:
            err_field.append(
                interactions.EmbedField(
                    name="Guild",
                    value=f"{ctx.guild.name}\n``{ctx.guild.id}``",
                    inline=True,
                )
            )
    log_error.fields = err_field

    payload: dict = models.discord.message.process_message_payload(
        embeds=log_error
    )
    await _client.http.create_message(
        channel_id=(
            LOG_CHANNEL if debug_system is False else int(ctx.channel_id)
        ),
        payload=payload,
    )

    if ctx and isinstance(
        ctx, interactions.InteractionContext | PrefixedContext
    ):
        embed = interactions.Embed(
            title="**Uh oh...**",
            description="".join(
                [
                    "An error occurred. The developer is dealing with the ",
                    " problem now.\nHave any question? ",
                    "Join the [**support server**](https://discord.gg/mE967ub6Ct)",
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

        await ctx.send(
            embeds=embed, ephemeral=(True if debug_system is False else False)
        )


class Error(interactions.Extension):
    """Error callback."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.listen(disable_default_listeners=True)
    async def on_command_error(
        self,
        event: interactions.events.CommandError,
    ) -> None:
        """For CommandError callback."""

        error_time = datetime.datetime.now().timestamp()

        if isinstance(event.error, interactions.errors.BadArgument):
            return await event.ctx.send(f"{event.error}")

        elif isinstance(event.error, interactions.errors.CommandOnCooldown):
            await event.ctx.send(
                "Wow! Trying to catch up with Sonic or something?"
            )

        elif isinstance(event.error, interactions.errors.CommandCheckFailure):

            class Null:
                ...

            return Null

        else:
            if not isinstance(
                event.ctx, interactions.InteractionContext | PrefixedContext
            ):
                return await handle_error(
                    self.client, error=event.error, error_time=error_time
                )

            await handle_error(
                self.client,
                error=event.error,
                error_time=error_time,
                ctx=event.ctx,
            )
