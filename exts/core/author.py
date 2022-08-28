"""
This module is for author commands.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import interactions
from const import VERSION


class Author(interactions.Extension):
    """Extension for author commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="about",
        description="Information about Articuno.",
    )
    async def _about(self, ctx: interactions.CommandContext):
        """Information about Articuno."""

        button = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="GitHub",
                url="https://github.com/Articuno-org/Articuno",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Top.gg",
                url="https://top.gg/bot/809084067446259722",
            ),
        ]

        embed = interactions.Embed(
            title="About Articuno",
            description="".join(
                [
                    "Articuno is a multi-purpose Discord Bot that can do a wide range of jobs, mostly ",
                    "with different fun commands. Highlight commands, such as `/img`, `/tag`, `/emoji`, `whos_that_pokemon`,",
                    " etc. The goal of Articuno is to make your server a better place, with different misc commands,",
                    " moderating your server with simple manners, and a built-in log system that requires simple ",
                    " setup.\n\nArticuno is a side-project that I work on, so commands can be broken sometimes. If",
                    " you encounter any issue, be sure to use `/invite` and join the support server to report the ",
                    "problem.\n\nWhenever that is creating tags with autocomplete, bringing joys to members, moderating",
                    " the server, Articuno has you covered.",
                ]
            ),
            color=0x7CB7D3,
            footer=interactions.EmbedFooter(
                text=f"Maintained by Blue#2095 • Version {VERSION}"
            ),
        )

        await ctx.send(embeds=embed, components=button)

    @interactions.extension_command(
        name="credits",
        description="Developers/Contributors to this project.",
    )
    async def _credits(self, ctx: interactions.CommandContext):
        """Developers/Contributors to this project."""

        profile = interactions.Button(
            style=interactions.ButtonStyle.LINK,
            label="Profile",
            url="https://blue.is-a.dev/",
        )

        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar_url}",
        )
        embed = interactions.Embed(
            title="Credits",
            description="Articuno is being maintained, developed and improved by Blue#2095.",
            color=0x7CB7D3,
            footer=footer,
        )

        await ctx.send(embeds=embed, components=[profile])

    @interactions.extension_command(
        name="invite",
        description="Invite Articuno to your server.",
    )
    async def _invite(self, ctx: interactions.CommandContext):
        """Invite Articuno to your server."""

        buttons = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Add me to your server",
                url="https://discord.com/oauth2/authorize?client_id=809084067446259722&permissions=1644905889023&scope=bot%20applications.commands",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Support server",
                url="https://discord.gg/SPd5RNhwfY",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Vote me on Top.gg",
                url="https://top.gg/bot/809084067446259722/vote",
            ),
        ]

        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar_url}",
        )
        embed = interactions.Embed(
            title="Invite Articuno to your server",
            description="Click the button below to invite Articuno to your server.\n\nIf you have any questions, feel free to join the support server.",
            color=0x7CB7D3,
            footer=footer,
        )

        await ctx.send(embeds=embed, components=buttons)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Author(client)
    logging.debug("""[%s] Loaded Author extension.""", log_time)
    print(f"[{log_time}] Loaded Author extension.")
