"""
/help command.

(C) 2022-2023 - B1ue-Dev
"""

import interactions
from interactions.ext.paginators import Paginator


class Help(interactions.Extension):
    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="help",
        description="Get a list of all available commands.",
    )
    async def help(self, ctx: interactions.SlashContext) -> None:
        """Get a list of all available commands."""

        embed = interactions.Embed(
            title="List of available commands.",
            color=0x7CB7D3,
            thumbnail=interactions.EmbedAttachment(
                url=self.client.user.avatar.url
            ),
        )
        help_list = []
        i = 0

        for command_index, command in enumerate(
            self.client.application_commands
        ):
            if isinstance(command, interactions.SlashCommand):
                if i == 10:
                    help_list.append(embed)
                    i = 0
                    embed = interactions.Embed(
                        title="List of available commands.",
                        color=0x7CB7D3,
                        thumbnail=interactions.EmbedAttachment(
                            url=self.client.user.avatar.url
                        ),
                    )

                embed.add_field(
                    name=f"/{command.name}"
                    + (
                        f" {command.group_name}"
                        if str(command.group_name) != "None"
                        else ""
                    )
                    + (
                        f" {command.sub_cmd_name}"
                        if str(command.sub_cmd_name) != "None"
                        else ""
                    ),
                    value=f"{command.sub_cmd_description}"
                    if str(command.sub_cmd_name) != "None"
                    else f"{command.description}",
                )
                i += 1

        paginator = Paginator.create_from_embeds(
            self.client, *help_list, timeout=30
        )
        print(help_list)
        await paginator.send(ctx)
