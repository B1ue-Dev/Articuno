"""
/help command.

(C) 2022-2023 - B1ue-Dev
"""

import interactions
from interactions.ext.paginators import Page, Paginator


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
                if i == 15:
                    help_list.append(embed)
                    i = 0
                    embed = interactions.Embed(
                        title="List of available commands.",
                        color=0x7CB7D3,
                        thumbnail=interactions.EmbedAttachment(
                            url=self.client.user.avatar.url
                        ),
                    )

                if command.sub_cmd_name is None:
                    embed.add_field(
                        name=f"/{command.name}", value=command.description
                    )
                else:
                    if str(command.sub_cmd_name) != "None":
                        embed.add_field(
                            name=f"/{command.name} {command.sub_cmd_name}",
                            value=f"{command.sub_cmd_description}",
                        )

                i += 1

        paginator = Paginator.create_from_embeds(self.client, *help_list)
        await paginator.send(ctx)
