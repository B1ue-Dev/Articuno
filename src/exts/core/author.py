"""
/author commands.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import interactions
from src.const import VERSION, TOPGGAPI
from src.utils.utils import (
    handle_username,
    get_response,
)


class Author(interactions.Extension):
    """Extension for author commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.topgg: str = "https://top.gg/bot/809084067446259722"
        self.github: str = "https://github.com/B1ue-Dev/Articuno"
        self.invite_url: str = (
            "https://discord.com/oauth2/authorize?client_id=809084067446259722&permissions=1644905889023&scope=bot%20applications.commands"
        )

    @interactions.slash_command(
        name="about",
        description="Information about Articuno.",
    )
    async def about(self, ctx: interactions.SlashContext) -> None:
        """Information about Articuno."""

        button = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="GitHub",
                url=self.github,
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Top.gg",
                url=self.topgg,
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Donate to keep the project alive",
                url="https://buymeacoffee.com/b1uedev",
            ),
        ]

        embed = interactions.Embed(
            title="About Articuno",
            description="".join(
                [
                    "Articuno is a multi-purpose Discord Bot that can do a wide range of jobs, mostly with different fun commands. ",
                    "Highlight commands, such as `/img`, `/tag`, `/emoji`, `/whos_that_pokemon`, etc. The goal of Articuno is to ",
                    "make your server a better place, with different fun commands in any possible way.",
                    "\n\nArticuno is now under maintenance mode, meaning it should be bug-free. ",
                    "If you encounter any issue be sure to use `/invite` and join the support server to report the ",
                    "problem.\n\nWhenever creating tags, bringing joys to members with the most ridiculous or random way, ",
                    "Articuno has you covered!",
                ]
            ),
            color=0x7CB7D3,
            footer=interactions.EmbedFooter(
                text=f"Maintained by @b1uedev  •  Version {VERSION}"
            ),
        )

        await ctx.send(embeds=embed, components=button)

    @interactions.slash_command(
        name="credits",
        description="Developers/Contributors to this project.",
    )
    async def credits(self, ctx: interactions.SlashContext) -> None:
        """Developers/Contributors to this project."""

        profile = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Profile",
                url="https://blue.is-a.dev/",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Donate to keep the project alive",
                url="https://buymeacoffee.com/b1uedev",
            ),
        ]

        footer = interactions.EmbedFooter(
            text=f"Requested by {handle_username(ctx.user.username, ctx.user.discriminator)}",
            icon_url=f"{ctx.user.avatar.url}",
        )
        embed = interactions.Embed(
            title="Credits",
            description="Articuno is being maintained by @b1uedev.\nIf you like Articuno and want to have it online, donate to keep the project alive. Thanks!",
            color=0x7CB7D3,
            footer=footer,
        )

        await ctx.send(embeds=embed, components=profile)

    @interactions.slash_command(
        name="invite",
        description="Invite Articuno to your server.",
    )
    async def invite(self, ctx: interactions.SlashContext) -> None:
        """Invite Articuno to your server."""

        buttons = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Add me to your server",
                url=self.invite_url,
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Support server",
                url="https://discord.gg/mE967ub6Ct",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Vote me on Top.gg",
                url=f"{self.topgg}/vote",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Donate to keep the project alive",
                url="https://buymeacoffee.com/b1uedev",
            ),
        ]

        footer = interactions.EmbedFooter(
            text=f"Requested by {handle_username(ctx.user.username, ctx.user.discriminator)}",
            icon_url=f"{ctx.user.avatar.url}",
        )
        embed = interactions.Embed(
            title="Invite Articuno to your server",
            description="".join(
                [
                    "Click the button below to invite Articuno to your server.",
                    "\n\nIf you have any questions, feel free to join the support server.",
                ]
            ),
            color=0x7CB7D3,
            footer=footer,
        )

        await ctx.send(embeds=embed, components=buttons)

    @interactions.slash_command(
        name="vote", description="Vote for Articuno on Top-gg."
    )
    async def vote(self, ctx: interactions.SlashContext) -> None:
        """Vote for Articuno on Top-gg."""

        url: str = "https://top.gg/api/bots/809084067446259722/check"
        headers: dict = {"Authorization": TOPGGAPI}
        params: dict = {"userId": ctx.user.id}
        resp = await get_response(url=url, headers=headers, params=params)

        button = interactions.Button(
            style=interactions.ButtonStyle.LINK,
            label="Vote here",
            url=f"{self.topgg}/vote",
        )

        embed = interactions.Embed(
            title="Vote for Articuno on Top-gg.",
            description="".join(
                [
                    "Thanks for voting. ",
                    f"""You have voted for Articuno {resp["voted"]} times.""",
                    " While you get nothing, it helps the bot grow!",
                ]
            ),
            color=0x7CB7D3,
        )

        await ctx.send(
            content=f"{self.topgg}/vote", embed=embed, components=[button]
        )


def setup(client) -> None:
    """Setup the extension."""
    Author(client)
    logging.info("Loaded Author extension.")
