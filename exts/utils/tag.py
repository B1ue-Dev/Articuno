"""
This module is for a tag system.

(C) 2022 - Jimmy-Blue
"""

import json
import datetime
import interactions
from interactions.ext.wait_for import wait_for_component
from utils.permission import Permissions, has_permission


class _Tag_Error(Exception):
    """
    A class representing Tag error.

    1001: Tag not found in database.
    1002: This guild does not have any registered tag.
    """

    code: int
    message: str

    __slots__ = ["code", "message"]

    def __init__(self, code: int, message: str = None) -> None:
        self.code = code
        self.message = message

        super().__init__(message)

    def lookup(code: int) -> str:
        """
        Look up the message of the error code.
        :param code: The error code.
        :type code: int
        :return: The error message.
        :rtype: str
        """

        return {
            1001: "Tag not found in database.",
            1002: "This guild does not have any registered tag."
        }


class _Tag:
    """
    A custom class objecting reprenting a tag.

    :ivar str description: The description of the tag.
    :ivar int created_on: The created timestamp of a tag.
    :ivar str author: The tag creator.
    :ivar int last_edited_on: The last edited timestamp of a tag.
    :ivar str last_edited_by: The author of the last edit.
    """
    __slots__ = ["description", "created_on", "author", "last_edited_on", "last_edited_by"]

    name: str
    description: str
    created_on: int
    author: str
    last_edited_on: int
    last_edited_by: int

    def __init__(self, **kwargs) -> None:
        self.description = kwargs.get("description", None)
        self.created_on = kwargs.get("created_on", None)
        self.author = kwargs.get("author", None)
        self.last_edited_on = kwargs.get("last_edited_on", None)
        self.last_edited_by = kwargs.get("last_edited_by", None)

    def get_tag(self, guild_id: str, tag_name: str) -> "_Tag":
        """
        Returns the Tag object of a tag.

        :param guild_id: The ID of the guild.
        :type guild_id: int
        :param tag_name: The name of the tag.
        :type tag_name: str
        :return: The Tag object of the tag.
        :rtype: _Tag
        """
        db = json.loads(open("./db/tag.json", "r").read())
        if guild_id not in db:
            raise _Tag_Error(code=1002, message="This guild does not have any registered tag.")

        if tag_name not in db[guild_id]:
            raise _Tag_Error(code=1001, message="Tag not found in database.")

        return _Tag(
            name=tag_name,
            description=db[guild_id][tag_name]["description"],
            created_on=db[guild_id][tag_name]["created_on"],
            author=db[guild_id][tag_name]["author"],
            last_edited_on=db[guild_id][tag_name]["last_edited_on"],
            last_edited_by=db[guild_id][tag_name]["last_edited_by"]
        )


class Tag(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
        self.edited_name = None

    @interactions.extension_command(
        name="tag",
        description="Tag system",
        dm_permission=False,
    )
    async def _tag(self, *args, **kwargs):
        ...

    @_tag.subcommand(name="create")
    async def _tag_create(self, ctx: interactions.CommandContext):
        """Creates a new tag."""
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

    @_tag.subcommand(name="view")
    @interactions.option("The name of the tag", autocomplete=True)
    async def _tag_view(self, ctx: interactions.CommandContext, tag_name: str):
        """Views a tag."""

        try:
            await ctx.send(_Tag().get_tag(str(ctx.guild_id), tag_name).description)
        except _Tag_Error as e:
            await ctx.send(e.lookup(e.code), ephemeral=True)

    @_tag.subcommand(name="edit")
    @interactions.option("The name of the tag", autocomplete=True)
    async def _tag_edit(self, ctx: interactions.CommandContext, tag_name: str):
        """Edits a tag."""

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

    @_tag.subcommand(name="info")
    @interactions.option("The name of the tag", autocomplete=True)
    async def _tag_info(self, ctx: interactions.CommandContext, tag_name: str):
        """Shows the information about a tag."""

        tag = _Tag().get_tag(str(ctx.guild_id), tag_name)

        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
            icon_url=f"{ctx.author.user.avatar_url}",
        )
        fields = [
            interactions.EmbedField(
                name="Author",
                value=f"<@!{tag.author}>",
                inline=True,
            ),
            interactions.EmbedField(
                name="Created on",
                value=f"<t:{tag.created_on}>",
                inline=True,
            ),
        ]
        embed = interactions.Embed(
            title=f"Tag: {tag_name}",
            color=0x5F85A0,
            footer=footer,
            fields=fields,
        )
        if tag.last_edited_on:
            embed.add_field(
                name="Last edited on",
                value=f"<t:{tag.last_edited_on}>",
                inline=True,
            )
            embed.add_field(
                name="Last edited by",
                value=f"<@!{tag.last_edited_by}>",
                inline=True,
            )
        embed.add_field(
            name="Description",
            value="Please use ``/tag view`` to see the content.",
            inline=False,
        )

        await ctx.send(embeds=embed)

    @_tag.subcommand(name="delete")
    @interactions.option("The name of the tag", autocomplete=True)
    async def _tag_delete(self, ctx: interactions.CommandContext, tag_name: str):
        """Deletes a tag."""

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

        res = await wait_for_component(
            self.client,
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

    @_tag.subcommand(name="list")
    async def _tag_list(self, ctx: interactions.CommandContext):
        """Lists all tag within the server."""

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
                f"Tag ``{self.edited_name}`` edited into ``{tag_name}``."
                if self.edited_name != tag_name
                else f"Tag ``{self.edited_name}`` edited."
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
