"""
Error system handler.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import traceback
import interactions
from interactions import LibraryException


class Error(interactions.Extension):
    """on_command_error callback."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_listener(name="on_command_error")
    async def on_command_error(self, ctx: interactions.CommandContext, error: Exception):
        """For every Exception callback."""

        if isinstance(error, LibraryException):

            if int(error.code) == 50013:
                return await ctx.send("You do not have permission to perform this action." ,ephemeral=True)

            error_time = datetime.datetime.utcnow().timestamp()

            traceb2 = traceback.format_exception(
                type(error),
                value=error,
                tb=error.__traceback__,
                limit=1000,
            )
            traceb = "".join(traceb2)
            traceb = traceb.replace("`","")
            traceb = traceb.replace("\\n","\n")
            traceb = traceb.replace("\\t","\t")
            traceb = traceb.replace("\\r","\r")
            traceb = traceb.replace("\\","/")
            er = ""
            for i in traceb:
                er = er + f"{i}"

            await ctx.get_guild()

            embed = interactions.Embed(
                title="**Uh oh...**",
                description="".join(
                    [
                        "An error occurred. The developer team is dealing with the problem now.\n",
                        "Have any question? Join the [**support server**](https://discord.gg/rQHRQ8JjSY) for more help."
                    ]
                ),
                color=0xed4245,
                fields=[
                    interactions.EmbedField(
                        name="Error",
                        value=f"```py\n{type(error).__name__}: {error}\n```",
                    ),
                ],
            )

            await ctx.send(embeds=embed, ephemeral=True)

            log_channel = interactions.Channel(
                **await self.client._http.get_channel(957090401418899526),
                _client=self.client._http,
            )
            command_name = ctx.data._json["name"]

            log_error = interactions.Embed(
                title="An error occurred!",
                description="".join(
                    [
                        f"Caused by **/{command_name}**.\n",
                        f"Author: {ctx.user.username}#{ctx.user.discriminator} ``{ctx.user.id}``\n",
                        f"Guild: {ctx.guild.name} ``{ctx.guild_id}``\n",
                        f"Occurred on: <t:{round(error_time)}:F>",
                    ]
                ),
                color=0xed4245,
                fields=[
                    interactions.EmbedField(
                        name="Traceback",
                        value=f"```py\n{traceb}\n```" if len(traceb) < 1024 else f"```py\n...{traceb[-1000:]}\n```",
                    )
                ]
            )
            await log_channel.send(embeds=log_error)

        else:
            error_time = datetime.datetime.utcnow().timestamp()

            traceb2 = traceback.format_exception(
                type(error),
                value=error,
                tb=error.__traceback__,
                limit=1000,
            )
            traceb = "".join(traceb2)
            traceb = traceb.replace("`","")
            traceb = traceb.replace("\\n","\n")
            traceb = traceb.replace("\\t","\t")
            traceb = traceb.replace("\\r","\r")
            traceb = traceb.replace("\\","/")
            er = ""
            for i in traceb:
                er = er + f"{i}"

            await ctx.get_guild()

            embed = interactions.Embed(
                title="**Uh oh...**",
                description="".join(
                    [
                        "An error occurred. The developer team is dealing with the problem now.\n",
                        "Have any question? Join the [**support server**](https://discord.gg/rQHRQ8JjSY) for more help."
                    ]
                ),
                color=0xed4245,
                fields=[
                    interactions.EmbedField(
                        name="Error",
                        value=f"```py\n{type(error).__name__}: {error}\n```",
                    ),
                ],
            )

            await ctx.send(embeds=embed, ephemeral=True)

            log_channel = interactions.Channel(
                **await self.client._http.get_channel(957090401418899526),
                _client=self.client._http,
            )
            command_name = ctx.data._json["name"]

            log_error = interactions.Embed(
                title="An error occurred!",
                description="".join(
                    [
                        f"Caused by **/{command_name}**.\n",
                        f"Author: {ctx.user.username}#{ctx.user.discriminator} ``{ctx.user.id}``\n",
                        f"Guild: {ctx.guild.name} ``{ctx.guild_id}``\n",
                        f"Occurred on: <t:{round(error_time)}:F>",
                    ]
                ),
                color=0xed4245,
                fields=[
                    interactions.EmbedField(
                        name="Traceback",
                        value=f"```py\n{traceb}\n```" if len(traceb) < 1024 else f"```py\n...{traceb[-1000:]}\n```",
                    )
                ]
            )
            await log_channel.send(embeds=log_error)




def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.now() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Error(client)
    logging.debug("""[%s] Loaded Error extension.""", log_time)
    print(f"[{log_time}] Loaded Error extension.")
