"""
/author commands.

(C) 2022-2023 - B1ue-Dev
"""

import interactions
from interactions.ext.prefixed_commands import (
    prefixed_command,
    PrefixedContext,
)
from const import VERSION


class Author(interactions.Extension):
    """Extension for author commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="about",
        description="Information about Articuno.",
    )
    async def about(self, ctx: interactions.InteractionContext) -> None:
        """Information about Articuno."""

        button = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="GitHub",
                url="https://github.com/Jimmy-Blue/Articuno",
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
                text=f"Maintained by Blue#2095  •  Version {VERSION}"
            ),
        )

        await ctx.send(embeds=embed, components=button)

    @prefixed_command(name="about")
    async def _about(self, ctx: PrefixedContext) -> None:
        """Information about Articuno."""

        button = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="GitHub",
                url="https://github.com/Jimmy-Blue/Articuno",
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
                text=f"Maintained by Blue#2095  •  Version {VERSION}"
            ),
        )

        await ctx.send(embeds=embed, components=button)

    @interactions.slash_command(
        name="credits",
        description="Developers/Contributors to this project.",
    )
    async def credits(self, ctx: interactions.InteractionContext) -> None:
        """Developers/Contributors to this project."""

        profile = interactions.Button(
            style=interactions.ButtonStyle.LINK,
            label="Profile",
            url="https://blue.is-a.dev/",
        )

        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar.url}",
        )
        embed = interactions.Embed(
            title="Credits",
            description="Articuno is being maintained, developed and improved by Blue#2095.",
            color=0x7CB7D3,
            footer=footer,
        )

        await ctx.send(embeds=embed, components=[profile])

    @prefixed_command(name="credits")
    async def _credits(self, ctx: PrefixedContext) -> None:
        """Developers/Contributors to this project."""

        profile = interactions.Button(
            style=interactions.ButtonStyle.LINK,
            label="Profile",
            url="https://blue.is-a.dev/",
        )

        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar.url}",
        )
        embed = interactions.Embed(
            title="Credits",
            description="Articuno is being maintained, developed and improved by Blue#2095.",
            color=0x7CB7D3,
            footer=footer,
        )

        await ctx.send(embeds=embed, components=[profile])

    @interactions.slash_command(
        name="invite",
        description="Invite Articuno to your server.",
    )
    async def invite(self, ctx: interactions.InteractionContext) -> None:
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
            icon_url=f"{ctx.user.avatar.url}",
        )
        embed = interactions.Embed(
            title="Invite Articuno to your server",
            description="Click the button below to invite Articuno to your server.\n\nIf you have any questions, feel free to join the support server.",
            color=0x7CB7D3,
            footer=footer,
        )

        await ctx.send(embeds=embed, components=buttons)

    @prefixed_command(name="invite")
    async def _msg_invite(self, ctx: PrefixedContext) -> None:
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
            icon_url=f"{ctx.user.avatar.url}",
        )
        embed = interactions.Embed(
            title="Invite Articuno to your server",
            description="Click the button below to invite Articuno to your server.\n\nIf you have any questions, feel free to join the support server.",
            color=0x7CB7D3,
            footer=footer,
        )

        await ctx.send(embeds=embed, components=buttons)
