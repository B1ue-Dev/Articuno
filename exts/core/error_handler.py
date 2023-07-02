"""
Error system handler.

(C) 2022-2023 - B1ue-Dev
"""

import datetime
import traceback
import interactions
from const import LOG_CHANNEL


async def handle_error(
    self,
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

    log_channel = self.client.get_channel(LOG_CHANNEL)

    log_error = interactions.Embed(
        title="An error occurred!",
        color=0xED4245,
        description=f"```\n{traceb}\n```",
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

    await log_channel.send(embeds=log_error)

    if ctx and isinstance(ctx, interactions.InteractionContext):
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

        await ctx.send(embeds=embed, ephemeral=True)


class Error(interactions.Extension):
    """on_command_error callback."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.listen()
    async def on_error(
        self,
        event: interactions.events.CommandError,
    ) -> None:
        """For Error callback."""

        error_time = datetime.datetime.utcnow().timestamp()

        if isinstance(event.error, interactions.errors.BadArgument):
            return await event.ctx.send(f"{event.error}")

        elif isinstance(event.error, interactions.errors.CommandCheckFailure):
            if event.ctx.guild:
                return await event.ctx.send(
                    content="You do not have permission to do this action.",
                )
        # elif isinstance(event.error, interactions.errors.CommandOnCooldown):
        #     delta_wait = datetime.timedelta(
        #         seconds=event.error.cooldown.get_cooldown_time()
        #     )
        #     return await event.ctx.send(
        #         content=(
        #             "You are on cooldown. Try again in ",
        #             f" `{delta_wait}`."
        #         )
        #     )
        # This is planned later.
        # Currently, I don't have time to work on this.
        else:
            if not isinstance(event.ctx, interactions.InteractionContext):
                return await handle_error(
                    self, error=event.error, error_time=error_time
                )

            await handle_error(
                self, error=event.error, error_time=error_time, ctx=event.ctx
            )