"""
This module is for a tag system.

(C) 2022 - Jimmy-Blue
"""

import json
import datetime
import interactions
from interactions import extension_command as command
from utils.permission import Permissions, has_permission


class Tag(interactions.Extension):
    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot
        self.edited_name = None

    @command(
        name="tag",
        description="Tag system",
        options=[
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="create",
                description="Create a tag",
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="view",
                description="View a tag",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="tag_name",
                        description="The name of the tag",
                        required=True,
                        autocomplete=True,
                    )
                ],
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="edit",
                description="Edit a tag",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="tag_name",
                        description="The name of the tag",
                        required=True,
                        autocomplete=True,
                    )
                ],
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="info",
                description="Information about a tag",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="tag_name",
                        description="The name of the tag",
                        required=True,
                        autocomplete=True,
                    )
                ],
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="delete",
                description="Delete a tag",
                options=[
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name="tag_name",
                        description="The name of the tag",
                        required=True,
                        autocomplete=True,
                    )
                ],
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name="list",
                description="List all tags",
            ),
        ],
        dm_permission=False,
    )
    async def _tag(
        self,
        ctx: interactions.CommandContext,
        sub_command: str,
        tag_name: str = None,
    ):

        if sub_command == "create":
            if not (
                has_permission(
                    int(ctx.author.permissions),
                    Permissions.MANAGE_MESSAGES,
                )
                or has_permission(
                    int(ctx.author.permissions),
                    Permissions.ADMINISTRATOR,
                )
            ):
                return await ctx.send(
                    content="You do not have permission to perform this action.",
                    ephemeral=True,
                )

            modal = interactions.Modal(
                title="Create new tag",
                custom_id="new_tag",
                components=[
                    interactions.TextInput(
                        style=interactions.TextStyleType.SHORT,
                        label="Name of the tag",
                        placeholder="The name of the tag you wish to create",
                        custom_id="tag_name",
                        max_length=100,
                    ),
                    interactions.TextInput(
                        style=interactions.TextStyleType.PARAGRAPH,
                        label="Description of the tag",
                        placeholder="The description of the tag you wish to create.",
                        custom_id="tag_description",
                        max_length=2000,
                    ),
                ],
            )

            await ctx.popup(modal)

        if sub_command == "view":
            guild_id = str(ctx.guild_id)

            db = json.loads(open("./db/tag.json", "r").read())
            if guild_id not in db:
                return await ctx.send(
                    content="This guild does not have any registered tag.",
                    ephemeral=True,
                )

            if tag_name not in db[guild_id]:
                return await ctx.send(content="Tag not found.", ephemeral=True)

            await ctx.send(content=db[guild_id][tag_name]["description"])

        if sub_command == "edit":
            if not (
                has_permission(
                    int(ctx.author.permissions),
                    Permissions.MANAGE_MESSAGES,
                )
                or has_permission(
                    int(ctx.author.permissions),
                    Permissions.ADMINISTRATOR,
                )
            ):
                return await ctx.send(
                    content="You do not have permission to perform this action.",
                    ephemeral=True,
                )

            guild_id = str(ctx.guild_id)
            db = json.loads(open("./db/tag.json", "r").read())

            if guild_id not in db:
                return await ctx.send(
                    content="This guild does not have any registered tag.",
                    ephemeral=True,
                )

            if tag_name not in db[guild_id]:
                return await ctx.send(content="Tag not found.", ephemeral=True)

            self.edited_name = tag_name
            modal = interactions.Modal(
                title=f"Edit tag: {tag_name}",
                custom_id="edit_tag",
                components=[
                    interactions.TextInput(
                        style=interactions.TextStyleType.SHORT,
                        label="Name of the tag",
                        placeholder="The name of the tag you want to edit.",
                        custom_id="name",
                        max_length=100,
                        value=tag_name,
                    ),
                    interactions.TextInput(
                        style=interactions.TextStyleType.PARAGRAPH,
                        label="Description of the tag",
                        placeholder="The description of the tag you want to edit.",
                        custom_id="description",
                        max_length=2000,
                        value=db[guild_id][tag_name]["description"],
                    ),
                ],
            )

            await ctx.popup(modal)

        if sub_command == "info":
            guild_id = str(ctx.guild_id)
            db = json.loads(open("./db/tag.json", "r").read())

            if guild_id not in db:
                return await ctx.send(
                    content="This guild does not have any registered tag.",
                    ephemeral=True,
                )

            if tag_name not in db[guild_id]:
                return await ctx.send(content="Tag not found.", ephemeral=True)

            author = db[guild_id][tag_name]["author"]
            created_on = db[guild_id][tag_name]["created_on"]
            last_edited_on = db[guild_id][tag_name]["last_edited_on"]
            last_edited_by = db[guild_id][tag_name]["last_edited_by"]

            footer = interactions.EmbedFooter(
                text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
                icon_url=f"{ctx.author.user.avatar_url}",
            )
            fields = [
                interactions.EmbedField(
                    name="Author",
                    value=f"<@!{author}>",
                    inline=True,
                ),
                interactions.EmbedField(
                    name="Created on",
                    value=f"<t:{created_on}>",
                    inline=True,
                ),
            ]
            embed = interactions.Embed(
                title=f"Tag: {tag_name}",
                color=0x5F85A0,
                footer=footer,
                fields=fields,
            )
            if last_edited_on:
                embed.add_field(
                    name="Last edited on",
                    value=f"<t:{last_edited_on}>",
                    inline=True,
                )
                embed.add_field(
                    name="Last edited by",
                    value=f"<@!{last_edited_by}>",
                    inline=True,
                )
            embed.add_field(
                name="Description",
                value="Please use ``/tag view`` to see the content.",
                inline=False,
            )

            await ctx.send(embeds=embed)

        if sub_command == "delete":
            await ctx.defer(ephemeral=True)

            if not (
                has_permission(
                    int(ctx.author.permissions),
                    Permissions.MANAGE_MESSAGES,
                )
                or has_permission(
                    int(ctx.author.permissions),
                    Permissions.ADMINISTRATOR,
                )
            ):
                return await ctx.send(
                    content="You do not have permission to perform this action.",
                    ephemeral=True,
                )

            guild_id = str(ctx.guild_id)
            db = json.loads(open("./db/tag.json", "r").read())

            if guild_id not in db:
                return await ctx.send(
                    content="This guild does not have any registered tag.",
                    ephemeral=True,
                )

            if tag_name not in db[guild_id]:
                return await ctx.send(content="Tag not found.", ephemeral=True)

            buttons = [
                interactions.ActionRow(
                    components=[
                        interactions.Button(
                            style=interactions.ButtonStyle.SUCCESS,
                            label="Yes",
                            custom_id="yes",
                        ),
                        interactions.Button(
                            style=interactions.ButtonStyle.DANGER,
                            label="No",
                            custom_id="no",
                        ),
                    ]
                )
            ]

            msg = await ctx.send(
                content=f"Do you want to delete tag ``{tag_name}``?",
                components=buttons,
                ephemeral=True,
            )

            res = await self.bot.wait_for_component(
                components=buttons,
                messages=int(msg.id),
                timeout=30,
            )

            if res.custom_id == "yes":
                del db[guild_id][tag_name]
                if len(db[guild_id]) == 0:
                    del db[guild_id]
                with open("./db/tag.json", "w") as f:
                    json.dump(db, f, indent=4)

                await res.edit(
                    f"Tag ``{tag_name}`` deleted.",
                    components=[],
                )

            elif res.custom_id == "no":

                await res.edit("Cancelled.", components=[])

        elif sub_command == "list":
            guild_id = str(ctx.guild_id)
            db = json.loads(open("./db/tag.json", "r").read())

            if guild_id not in db:
                return await ctx.send(
                    content="This guild does not have any registered tag.",
                    ephemeral=True,
                )

            if len(db[guild_id]) == 0:
                return await ctx.send(
                    content="This guild does not have any registered tag.",
                    ephemeral=True,
                )

            desc = []
            for tag in db[guild_id]:
                desc.append(f"``- {tag}``")
            embed = interactions.Embed(
                title="Tags",
                description="\n".join(desc),
            )
            await ctx.send(embeds=embed)

    @interactions.extension_modal(modal="new_tag")
    async def _new_tag(
        self,
        ctx: interactions.CommandContext,
        tag_name: str,
        tag_description: str,
    ):
        guild_id = str(ctx.guild_id)

        db = json.loads(open("./db/tag.json", "r").read())
        if guild_id not in db:
            db[guild_id] = {}
        db[guild_id][tag_name] = {
            "description": tag_description,
            "created_on": round(datetime.datetime.utcnow().timestamp()),
            "author": str(ctx.author.id),
            "last_edited_on": None,
            "last_edited_by": None,
        }
        with open("./db/tag.json", "w") as f:
            json.dump(db, f, indent=4)
        await ctx.send(
            content=f"Tag ``{tag_name}`` created.",
            ephemeral=True,
        )

    @interactions.extension_modal(modal="edit_tag")
    async def _edit_tag(
        self,
        ctx: interactions.CommandContext,
        tag_name: str,
        tag_description: str,
    ):
        guild_id = str(ctx.guild_id)

        db = json.loads(open("./db/tag.json", "r").read())
        db[guild_id][tag_name] = {
            "description": tag_description,
            "created_on": db[guild_id][self.edited_name]["created_on"],
            "author": db[guild_id][self.edited_name]["author"],
            "last_edited_on": round(datetime.datetime.utcnow().timestamp()),
            "last_edited_by": str(ctx.author.id),
        }
        with open("./db/tag.json", "w") as f:
            if tag_name != self.edited_name:
                del db[guild_id][self.edited_name]
            json.dump(db, f, indent=4)

        await ctx.send(
            content=(
                f"Tag ``{self.edited_name}`` edited into ``{tag_name}``"
                if self.edited_name != tag_name
                else f"Tag ``{self.edited_name}`` edited"
            ),
            ephemeral=True,
        )

    @interactions.extension_autocomplete(command="tag", name="tag_name")
    async def _tag_autocomplete(
        self,
        ctx: interactions.CommandContext,
        tag_name: str = "",
    ):
        guild_id = str(ctx.guild_id)
        letters: list = list(tag_name) if tag_name != "" else []
        tags = json.loads(open("./db/tag.json", "r", encoding="utf8").read())
        if guild_id in tags:
            if len(tag_name) == 0:
                await ctx.populate(
                    [
                        interactions.Choice(name=tag[0], value=tag[0])
                        for tag in (
                            list(tags[guild_id].items())[0:24]
                            if len(tags) > 25
                            else list(tags[guild_id].items())
                        )
                    ]
                )
            else:
                choices: list = []
                for tag in tags[guild_id]:
                    focus: str = "".join(letters)
                    if focus.lower() in tag.lower():
                        choices.append(interactions.Choice(name=tag, value=tag))
                await ctx.populate(choices)


def setup(bot):
    Tag(bot)
