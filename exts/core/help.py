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
        name="help", description="Get a list of all available commands"
    )
    async def help(self, ctx: interactions.SlashContext) -> None:
        """Get a list of all available commands."""
        help_list = []
        commands = sorted(
            self.client.application_commands, key=lambda x: str(x.name)
        )

        for i in range(0, len(commands), 10):
            listed = []
            for command in commands[i : i + 10]:
                if type(command) is not interactions.SlashCommand:
                    continue
                cmd_name = f"/{command.name}"
                group_name = (
                    f" {command.group_name}" if command.group_name else ""
                )
                sub_cmd_name = (
                    f" {command.sub_cmd_name}" if command.sub_cmd_name else ""
                )
                name = f"{cmd_name}{group_name}{sub_cmd_name}"
                description = (
                    command.sub_cmd_description
                    if command.sub_cmd_name
                    else command.description
                )
                listed.append(
                    interactions.EmbedField(
                        name=f"{name}", value=f"{description}"
                    )
                )

            help_list.append(
                interactions.Embed(
                    title="List of available commands.",
                    color=0x7CB7D3,
                    thumbnail=interactions.EmbedAttachment(
                        url=self.client.user.avatar.url
                    ),
                    fields=listed,
                )
            )

        paginator = Paginator.create_from_embeds(
            self.client, *help_list, timeout=30
        )
        await paginator.send(ctx)
