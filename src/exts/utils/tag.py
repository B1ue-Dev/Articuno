"""
Tag system.

(C) 2022-2023 - B1ue-Dev
"""

import asyncio
import logging
from datetime import datetime, timezone
from beanie import PydanticObjectId
import interactions
from interactions.ext.paginators import Paginator
from src.common.utils import Permissions, has_permission
from src.common.utils import tags


def get_utc_time() -> datetime:
    """Returns latest UTC time."""

    utc_time = datetime.now(tz=timezone.utc)
    return utc_time


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

    @tag.subcommand(
        sub_cmd_name="create", sub_cmd_description="Creates a new tag."
    )
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

    @tag.subcommand(
        sub_cmd_name="view",
        sub_cmd_description="Views a tag.",
    )
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

        await ctx.defer()

        guild_id = str(ctx.guild_id)

        if not await tags.find_one(tags.guild_id == guild_id).exists():
            return await ctx.send("This server does not have any tag.")

        if guild_tags := await tags.get(
            PydanticObjectId(
                (await tags.find_one(tags.guild_id == guild_id)).id
            )
        ):
            if guild_tags.tags.get(tag_name, None):
                await ctx.send(guild_tags.tags[tag_name]["description"])
            else:
                return await ctx.send("Tag not found.")

    @tag.subcommand(
        sub_cmd_name="edit",
        sub_cmd_description="Edits a tag.",
    )
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
            )

        guild_id = str(ctx.guild.id)
        if not await tags.find_one(tags.guild_id == guild_id).exists():
            return await ctx.send("This server does not have any tag.")

        if guild_tags := await tags.get(
            PydanticObjectId(
                (await tags.find_one(tags.guild_id == guild_id)).id
            )
        ):
            if not guild_tags.tags.get(tag_name, None):
                return await ctx.send("Tag not found.")

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
                value=guild_tags.tags[tag_name]["description"],
            ),
            title=f"Edit tag: {tag_name}",
            custom_id="edit_tag",
        )

        await ctx.send_modal(modal)

    @tag.subcommand(
        sub_cmd_name="info",
        sub_cmd_description="Shows the information about a tag.",
    )
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

        await ctx.defer()
        guild_id = str(ctx.guild_id)

        if not await tags.find_one(tags.guild_id == guild_id).exists():
            return await ctx.send("This server does not have any tag.")

        if guild_tags := await tags.get(
            PydanticObjectId(
                (await tags.find_one(tags.guild_id == guild_id)).id
            )
        ):
            if guild_tags.tags.get(tag_name, None):
                footer = interactions.EmbedFooter(
                    text=f"Requested by {ctx.author.username}#{ctx.author.discriminator}",
                    icon_url=f"{ctx.author.avatar.url}",
                )
                fields = [
                    interactions.EmbedField(
                        name="Author",
                        value=f"""<@{guild_tags.tags[tag_name]["author"]}>""",
                        inline=True,
                    ),
                    interactions.EmbedField(
                        name="Created on",
                        value=f"""<t:{guild_tags.tags[tag_name]["created_on"]}>""",
                        inline=True,
                    ),
                ]
                embed = interactions.Embed(
                    title=f"Tag: {tag_name}",
                    color=0x5F85A0,
                    footer=footer,
                    fields=fields,
                )
                if guild_tags.tags[tag_name]["last_edited_on"]:
                    embed.add_field(
                        name="Last edited on",
                        value=f"""<t:{guild_tags.tags[tag_name]["last_edited_on"]}>""",
                        inline=True,
                    )
                    embed.add_field(
                        name="Last edited by",
                        value=f"""<@!{guild_tags.tags[tag_name]["last_edited_by"]}>""",
                        inline=True,
                    )
                embed.add_field(
                    name="Description",
                    value="Please use ``/tag view`` to see the content.",
                    inline=False,
                )

                await ctx.send(embeds=embed)

            else:
                return await ctx.send("Tag not found.")

    @tag.subcommand(
        sub_cmd_name="delete", sub_cmd_description="Deletes a tag."
    )
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

        await ctx.defer()

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
            )

        guild_id = str(ctx.guild.id)

        if not await tags.find_one(tags.guild_id == guild_id).exists():
            return await ctx.send("This server does not have any tag.")

        if guild_tags := await tags.get(
            PydanticObjectId(
                (await tags.find_one(tags.guild_id == guild_id)).id
            )
        ):
            if not guild_tags.tags.get(tag_name, None):
                return await ctx.send("Tag not found.")

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
        )

        try:

            def _check(_ctx):
                return int(_ctx.ctx.user.id) == int(ctx.user.id) and int(
                    _ctx.ctx.channel_id
                ) == int(ctx.channel_id)

            res = await self.client.wait_for_component(
                components=buttons,
                messages=int(msg.id),
                check=_check,
                timeout=30,
            )

            if res.ctx.custom_id == "yes":
                guild_tags = await tags.get(
                    PydanticObjectId(
                        (await tags.find_one(tags.guild_id == guild_id)).id
                    )
                )
                del guild_tags.tags[tag_name]
                if len(guild_tags.tags) == 0:
                    await guild_tags.delete()
                else:
                    await guild_tags.save()

                await res.ctx.edit_origin(
                    content=f"Tag `{tag_name}` deleted.",
                    components=[],
                )

            elif res.ctx.custom_id == "no":
                await res.ctx.edit_origin(content="Cancelled.", components=[])

        except asyncio.TimeoutError:
            try:
                return await msg.edit(
                    content="Operation cancelled because of no response.",
                    components=[],
                )
            except interactions.client.errors.NotFound:
                return

    @tag.subcommand(
        sub_cmd_name="list",
        sub_cmd_description="Lists all tag within the server.",
    )
    async def list(self, ctx: interactions.SlashContext) -> None:
        """Lists all tag within the server."""

        guild_id = str(ctx.guild_id)
        if not await tags.find_one(tags.guild_id == guild_id).exists():
            return await ctx.send("This server does not have any tag.")

        guild_tags = await tags.get(
            PydanticObjectId(
                (await tags.find_one(tags.guild_id == guild_id)).id
            )
        )

        tag_list = [
            f"` {i+1} ` {tag}" for i, tag in enumerate(guild_tags.tags)
        ]
        chunks = [tag_list[x : x + 9] for x in range(0, len(tag_list), 9)]
        embeds = [
            interactions.Embed(
                title=f"Tag list for {ctx.guild.name}",
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

        if not await tags.find_one(tags.guild_id == guild_id).exists():
            await tags(
                guild_id=guild_id,
                tags={},
            ).save()

        guild_tags = await tags.get(
            PydanticObjectId(
                (await tags.find_one(tags.guild_id == guild_id)).id
            )
        )
        guild_tags.tags.update(
            {
                tag_name: {
                    "description": tag_description,
                    "created_on": round(get_utc_time().timestamp()),
                    "author": str(ctx.author.id),
                    "last_edited_on": None,
                    "last_edited_by": None,
                }
            }
        )
        await guild_tags.save()

        await ctx.send(
            content=f"Tag ``{tag_name}`` created.",
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

        guild_tags = await tags.get(
            PydanticObjectId(
                (await tags.find_one(tags.guild_id == guild_id)).id
            )
        )
        guild_tags.tags[tag_name] = {
            "description": tag_description,
            "created_on": guild_tags.tags[self.edited_name]["created_on"],
            "author": guild_tags.tags[self.edited_name]["author"],
            "last_edited_on": round(get_utc_time().timestamp()),
            "last_edited_by": str(ctx.author.id),
        }
        if tag_name != self.edited_name:
            del guild_tags.tags[self.edited_name]
        await guild_tags.save()

        await ctx.send(
            content=(
                f"Tag ``{self.edited_name}`` edited into ``{tag_name}``."
                if self.edited_name != tag_name
                else f"Tag ``{self.edited_name}`` edited."
            ),
        )

    @interactions.global_autocomplete("tag_name")
    async def tag_autocomplete(
        self,
        ctx: interactions.AutocompleteContext,
    ) -> None:
        """Autcomplete for tag commands."""

        guild_id = str(ctx.guild_id)

        if await tags.find_one(tags.guild_id == guild_id).exists():
            guild_tags = await tags.get(
                PydanticObjectId(
                    (await tags.find_one(tags.guild_id == guild_id)).id
                )
            )

            if tag_name := ctx.kwargs.get("tag_name"):
                letters: list = list(tag_name) if tag_name != "" else []
                choices: list = []
                for tag in guild_tags.tags:
                    focus: str = "".join(letters)
                    if focus.lower() in tag.lower():
                        choices.append({"name": tag, "value": tag})
                await ctx.send(choices)

            else:
                await ctx.send(
                    [
                        {"name": tag[0], "value": tag[0]}
                        for tag in (
                            list(guild_tags.tags.items())[0:24]
                            if len(guild_tags.tags) > 25
                            else list(guild_tags.tags.items())
                        )
                    ]
                )


def setup(client) -> None:
    """Setup the extension."""
    Tag(client)
    logging.info("Loaded Tag extension.")
