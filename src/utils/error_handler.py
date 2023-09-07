"""
Error system handler.

(C) 2022-2023 - B1ue-Dev
"""

import datetime
import traceback
import interactions
from interactions import models
from interactions.ext.prefixed_commands import PrefixedContext
from src.const import LOG_CHANNEL


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

    log_error = interactions.Embed(
        title="An error occurred!",
        color=0xED4245,
        description=f"```py\n{traceb[-4096:]}\n```",
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
    await _client.http.create_message(channel_id=LOG_CHANNEL, payload=payload)

    if ctx and isinstance(
        ctx, interactions.InteractionContext | PrefixedContext
    ):
        embed = interactions.Embed(
            title="**Uh oh...**",
            description="".join(
                [
                    "An error occurred. The developer team is dealing with the ",
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

        await ctx.send(embeds=embed)


class Error(interactions.Extension):
    """on_error callback."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.listen()
    async def on_error(
        self,
        event: interactions.events.Error,
    ) -> None:
        """For Error callback."""

        error_time = datetime.datetime.utcnow().timestamp()

        if isinstance(event.error, interactions.errors.BadArgument):
            return await event.ctx.send(f"{event.error}")

        elif isinstance(event.error, interactions.errors.CommandOnCooldown):
            await event.ctx.send(
                f"You are on cooldown. Please wait {round(event.error.cooldown.get_cooldown_time(), 2)} seconds."
            )

        elif isinstance(event.error, interactions.errors.CommandCheckFailure):
            if event.ctx.guild:
                return await event.ctx.send(
                    content="You do not have permission to do this action.",
                )

        elif isinstance(event.error, RuntimeError):
            pass

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
