"""
Tag system.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import json
import datetime
import interactions
from interactions.ext.paginators import Paginator
from utils.permission import Permissions, has_permission


class Tag_Error(Exception):
    """
    A class representing Tag error.

    1001: Tag not found in database.
    1002: This guild does not have any registered tag.
    """

    code: int
    """The code of the error."""
    message: str
    """The message of the error."""

    __slots__ = ["code", "message"]

    def __init__(self, code: int, message: str = None) -> None:
        self.code = code
        self.message = message

        super().__init__(message)

    def lookup(self, code: int) -> str:
        """
        Look up the message of the error code.
        :param code: The error code.
        :type code: int
        :return: The error message.
        :rtype: str
        """

        error_code: dict = {
            1001: "Tag not found in database.",
            1002: "This guild does not have any registered tag.",
        }
        return error_code.get(code)


class _Tag:
    """
    A custom class objecting reprenting a tag.
    """

    __slots__ = [
        "description",
        "created_on",
        "author",
        "last_edited_on",
        "last_edited_by",
    ]

    name: str
    """The name of the tag."""
    description: str
    """The description of the tag."""
    created_on: int
    """The created timestamp of a tag."""
    author: str
    """The name of tag creator."""
    last_edited_on: int
    """The last edited timestamp of a tag."""
    last_edited_by: int
    """The ID of the author from the last edit."""

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
            raise Tag_Error(
                code=1002,
                message="This guild does not have any registered tag.",
            )

        if tag_name not in db[guild_id]:
            raise Tag_Error(code=1001, message="Tag not found in database.")

        return _Tag(
            name=tag_name,
            description=db[guild_id][tag_name]["description"],
            created_on=db[guild_id][tag_name]["created_on"],
            author=db[guild_id][tag_name]["author"],
            last_edited_on=db[guild_id][tag_name]["last_edited_on"],
            last_edited_by=db[guild_id][tag_name]["last_edited_by"],
        )


class Tag(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
        self.edited_name = None

    @interactions.slash_command(
        name="tag",
        description="Handle all tag aspects.",
        dm_permission=False,
    )
    async def tag(self, ctx: interactions.SlashContext) -> None:
        """Handle all tag aspects."""
        ...

    @tag.subcommand()
    async def create(self, ctx: interactions.SlashContext) -> None:
        """Creates a new tag."""
        if not (
            has_permission(
                int(ctx.author.guild_permissions),
                Permissions.MANAGE_MESSAGES,
            )
            or has_permission(
                int(ctx.author.guild_permissions),
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
        )
        modal.add_components(
            [
                interactions.ShortText(
                    label="Name of the tag",
                    placeholder="The name of the tag you wish to create",
                    custom_id="tag_name",
                    max_length=100,
                ),
                interactions.ParagraphText(
                    label="Description of the tag",
                    placeholder="The description of the tag you wish to create.",
                    custom_id="tag_description",
                    max_length=2000,
                ),
            ],
        )

        await ctx.send_modal(modal)

    @tag.subcommand()
    @interactions.slash_option(
        name="tag_name",
        description="The name of the tag",
        opt_type=interactions.OptionType.STRING,
        required=True,
        autocomplete=True,
    )
    async def view(
        self, ctx: interactions.SlashContext, tag_name: str
    ) -> None:
        """Views a tag."""

        try:
            await ctx.send(
                _Tag().get_tag(str(ctx.guild.id), tag_name).description
            )
        except Tag_Error as e:
            await ctx.send(e.lookup(e.code), ephemeral=True)

    @tag.subcommand()
    @interactions.slash_option(
        name="tag_name",
        description="The name of the tag",
        opt_type=interactions.OptionType.STRING,
        required=True,
        autocomplete=True,
    )
    async def edit(
        self, ctx: interactions.SlashContext, tag_name: str
    ) -> None:
        """Edits a tag."""

        if not (
            has_permission(
                int(ctx.author.guild_permissions),
                Permissions.MANAGE_MESSAGES,
            )
            or has_permission(
                int(ctx.author.guild_permissions),
                Permissions.ADMINISTRATOR,
            )
        ):
            return await ctx.send(
                content="You do not have permission to perform this action.",
                ephemeral=True,
            )

        guild_id = str(ctx.guild.id)
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
            interactions.InputText(
                style=interactions.TextStyles.SHORT,
                label="Name of the tag",
                placeholder="The name of the tag you want to edit.",
                custom_id="tag_name",
                max_length=100,
                value=tag_name,
            ),
            interactions.InputText(
                style=interactions.TextStyles.PARAGRAPH,
                label="Description of the tag",
                placeholder="The description of the tag you want to edit.",
                custom_id="tag_description",
                max_length=2000,
                value=db[guild_id][tag_name]["description"],
            ),
            title=f"Edit tag: {tag_name}",
            custom_id="edit_tag",
        )

        await ctx.send_modal(modal)

    @tag.subcommand()
    @interactions.slash_option(
        name="tag_name",
        description="The name of the tag",
        opt_type=interactions.OptionType.STRING,
        required=True,
        autocomplete=True,
    )
    async def info(
        self, ctx: interactions.SlashContext, tag_name: str
    ) -> None:
        """Shows the information about a tag."""

        tag = _Tag().get_tag(str(ctx.guild.id), tag_name)

        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.author.username}#{ctx.author.discriminator}",
            icon_url=f"{ctx.author.avatar.url}",
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

    @tag.subcommand()
    @interactions.slash_option(
        name="tag_name",
        description="The name of the tag",
        opt_type=interactions.OptionType.STRING,
        required=True,
        autocomplete=True,
    )
    async def delete(
        self, ctx: interactions.SlashContext, tag_name: str
    ) -> None:
        """Deletes a tag."""

        await ctx.defer(ephemeral=True)

        if not (
            has_permission(
                int(ctx.author.guild_permissions),
                Permissions.MANAGE_MESSAGES,
            )
            or has_permission(
                int(ctx.author.guild_permissions),
                Permissions.ADMINISTRATOR,
            )
        ):
            return await ctx.send(
                content="You do not have permission to perform this action.",
                ephemeral=True,
            )

        guild_id = str(ctx.guild.id)
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
            )
        ]

        msg = await ctx.send(
            content=f"Do you want to delete tag ``{tag_name}``?",
            components=buttons,
            ephemeral=True,
        )

        res = await self.client.wait_for_component(
            components=buttons,
            messages=int(msg.id),
            timeout=30,
        )

        if res.ctx.custom_id == "yes":
            del db[guild_id][tag_name]
            if len(db[guild_id]) == 0:
                del db[guild_id]
            with open("./db/tag.json", "w") as f:
                json.dump(db, f, indent=4)

            await res.ctx.edit_origin(
                content=f"Tag ``{tag_name}`` deleted.",
                components=[],
            )

        elif res.ctx.custom_id == "no":
            await res.ctx.edit_origin(content="Cancelled.", components=[])

    @tag.subcommand()
    async def list(self, ctx: interactions.SlashContext) -> None:
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

        tag_list = [f"` {i+1} ` {tag}" for i, tag in enumerate(db[guild_id])]
        chunks = [tag_list[x : x + 9] for x in range(0, len(tag_list), 9)]
        embeds = [
            interactions.Embed(
                title="Tag list for ",
                fields=[
                    interactions.EmbedField(name="Name", value="\n".join(x))
                ],
            )
            for x in chunks
        ]

        if len(embeds) == 1:
            return await ctx.send(embeds=embeds)

        pag = Paginator.create_from_embeds(self.client, *embeds, timeout=30)
        pag.show_select_menu = True
        await pag.send(ctx)

    @interactions.modal_callback("new_tag")
    async def new_tag(
        self,
        ctx: interactions.ModalContext,
        tag_name: str,
        tag_description: str,
    ) -> None:
        """Modal callback for creating a new tag."""

        guild_id = str(ctx.guild_id)

        db = json.loads(open("./db/tag.json", "r").read())
        if guild_id not in db:
            db[guild_id] = {}
        db[guild_id][tag_name] = {
            "description": tag_description,
            "created_on": round(datetime.datetime.now().timestamp()),
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

    @interactions.modal_callback("edit_tag")
    async def edit_tag(
        self,
        ctx: interactions.ModalContext,
        tag_name: str,
        tag_description: str,
    ) -> None:
        """Modal callback for editing an existing tag."""

        guild_id = str(ctx.guild.id)

        db = json.loads(open("./db/tag.json", "r").read())
        db[guild_id][tag_name] = {
            "description": tag_description,
            "created_on": db[guild_id][self.edited_name]["created_on"],
            "author": db[guild_id][self.edited_name]["author"],
            "last_edited_on": round(datetime.datetime.now().timestamp()),
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

    @interactions.global_autocomplete("tag_name")
    async def tag_autocomplete(
        self,
        ctx: interactions.AutocompleteContext,
        tag_name: str = "",
    ) -> None:
        """Autcomplete for tag commands."""

        guild_id = str(ctx.guild_id)
        letters: list = list(tag_name) if tag_name != "" else []
        tags = json.loads(open("./db/tag.json", "r", encoding="utf8").read())
        if guild_id in tags:
            if len(tag_name) == 0:
                await ctx.send(
                    [
                        {"name": tag[0], "value": tag[0]}
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
                        choices.append({"name": tag, "value": tag})
                await ctx.send(choices)


def setup(client) -> None:
    """Setup the extension."""
    Tag(client)
    logging.info("Loaded Tag extension.")
