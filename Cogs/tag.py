import interactions
from interactions.ext.enhanced import (
	ext_subcommand_base,
	EnhancedExtension,
	option
)
from interactions.ext import wait_for
import os, json, datetime
from dotenv import load_dotenv
load_dotenv()

scope = int(os.getenv("SCOPE"))





class Tag(EnhancedExtension):
	def __init__(self, bot):
		self.bot = bot
		wait_for.setup(bot, add_method=True)
	

	tag = ext_subcommand_base("tag", scope=scope)

	@tag.subcommand(
		name="create",
		description="Create a tag"
	)
	async def _tag_create(self, ctx: interactions.CommandContext):
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
				)
			]
		)
		await ctx.popup(modal)


	@tag.subcommand(
		name="info",
		description="Information about a tag",
	)
	@option(type=interactions.OptionType.STRING, name="tag_name", autocomplete=True)
	async def _tag_view(self, ctx: interactions.CommandContext, tag_name: str):
		guild_id = ctx.guild_id
		tags = json.loads(open("./data/tag.json", "r").read())
		if guild_id in tags:
			if tag_name in tags[guild_id]:
				author = tags[guild_id][tag_name]["author"]
				description = tags[guild_id][tag_name]["description"]
				if len(description) > 100:
					description = description[:100] + "..."
				else:
					description = description
				created_at = tags[guild_id][tag_name]["created_at"]
				footer = interactions.EmbedFooter(
					text=f"Requested by {ctx.author.user.username}#{ctx.author.user.discriminator}",
					icon_url=f"{ctx.author.user.avatar_url}"
				)
				fields = [
					interactions.EmbedField(name="Author", value=f"<@!{author}>", inline=True),
					interactions.EmbedField(name="Created at", value=f"<t:{created_at}>", inline=True),
					interactions.EmbedField(name="Description", value=description, inline=False)
				]
				embed = interactions.Embed(
					title=f"Tag: {tag_name}",
					color=0x5f85a0,
					footer=footer,
					fields=fields,
				)
				await ctx.send(embeds=embed)
			else:
				await ctx.send("Tag not found.", ephemeral=True)
		else:
			await ctx.send(f"This guild does not have any registered tag.", ephemeral=True)
	

	@tag.subcommand(
		name="view",
		description="View a tags",
	)
	@option(type=interactions.OptionType.STRING, name="tag_name", autocomplete=True)
	async def _tag_view(self, ctx: interactions.CommandContext, tag_name: str):
		guild_id = ctx.guild_id
		tags = json.loads(open("./data/tag.json", "r").read())
		if guild_id in tags:
			if tag_name in tags[guild_id]:
				await ctx.send(content=tags[guild_id][tag_name]["description"])
			else:
				await ctx.send("Tag not found.", ephemeral=True)
		else:
			await ctx.send(f"This guild does not have any registered tag.", ephemeral=True)


	@tag.subcommand(
		name="list",
		description="List all tags",
	)
	async def _tag_list(self, ctx: interactions.CommandContext):
		guild_id = ctx.guild_id
		tags = json.loads(open("./data/tag.json", "r").read())
		if guild_id in tags:
			embed = interactions.Embed(
				title="Tags",
				description="\n".join(tags[guild_id].keys()),
			)
			await ctx.send(embeds=embed)
		else:
			await ctx.send(f"This guild does not have any registered tag.", ephemeral=True)


	@tag.subcommand(
		name="edit",
		description="Edit an existing tag",
	)
	@option(type=interactions.OptionType.STRING, name="tag_name", autocomplete=True)
	async def _tag_edit(self, ctx: interactions.CommandContext, tag_name: str):
		guild_id = ctx.guild_id
		tags = json.loads(open("./data/tag.json", "r").read())
		if guild_id in tags:
			if tag_name in tags[guild_id]:
				modal = interactions.Modal(
					title="Edit tag",
					custom_id="edit_tag",
					components=[
						interactions.TextInput(
							style=interactions.TextStyleType.SHORT,
							label="Name of the tag",
							placeholder="The name of the tag you wish to edit",
							custom_id="tag_name",
							max_length=100,
							value=tag_name,
						),
						interactions.TextInput(
							style=interactions.TextStyleType.PARAGRAPH,
							label="Description of the tag",
							placeholder="The description of the tag you wish to edit.",
							custom_id="tag_description",
							max_length=2000,
							value=tags[guild_id][tag_name]["description"],
						)
					]
				)
				await ctx.popup(modal)
			else:
				await ctx.send(f"Tag {tag_name} not found.", ephemeral=True)
				return
		else:
			await ctx.send(f"This guild does not have any registered tag.", ephemeral=True)
			return


	@tag.subcommand(
		name="delete",
		description="Delete an existing tag",
	)
	@option(type=interactions.OptionType.STRING, name="tag_name", autocomplete=True)
	async def _tag_delete(self, ctx: interactions.CommandContext, tag_name: str):
		guild_id = ctx.guild_id
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
						custom_id="no"
					),
				]
			)
		]
		tags = json.loads(open("./data/tag.json", "r").read())
		if guild_id in tags:
			if tag_name in tags[guild_id]:
				msg = await ctx.send(content=f"Do you want to delete tag ``{tag_name}``?", components=buttons, ephemeral=True)
				res = await self.bot.wait_for_component(components=buttons, messages = int(msg.id))
				buttonsed = [
					interactions.ActionRow(
						components=[
							interactions.Button(
								style=interactions.ButtonStyle.SUCCESS,
								label="Yes",
								custom_id="yes",
								disabled=True
							),
							interactions.Button(
								style=interactions.ButtonStyle.DANGER,
								label="No",
								custom_id="no",
								disabled=True
							),
						]
					)
				]
				if res.custom_id == "yes":
					del tags[guild_id][tag_name]
					if len(tags[guild_id]) == 0:
						del tags[guild_id]
					with open("./data/tag.json", "w") as f:
						json.dump(tags, f, indent=4)
					await res.edit(components=buttonsed)
					await res.send(f"Tag ``{tag_name}`` deleted.", ephemeral=True)
				elif res.custom_id == "no":
					await res.edit(components=buttonsed)
					await res.send("Cancelled.", ephemeral=True)
			else:
				await ctx.send(f"Tag {tag_name} not found.", ephemeral=True)
		else:
			await ctx.send(f"This guild does not have any registered tag.", ephemeral=True)


	tag.finish()




	@interactions.extension_modal(modal="new_tag")
	async def new_tag(self, ctx: interactions.CommandContext, tag_name: str, tag_description: str):
		guild_id = ctx.guild_id
		guild_id = str(guild_id)
		with open("./data/tag.json", "r") as f:
			tag1 = json.load(f)
			if guild_id not in tag1:
				guild_add = {
					guild_id: {}
				}
				with open("./data/tag.json", "w") as f:
					json.dump(guild_add, f, indent=4)
		tag = json.loads(open("./data/tag.json", "r").read())
		tag[guild_id][tag_name] = {
			"description": tag_description,
			"created_at": round(datetime.datetime.utcnow().timestamp()),
			"author": str(ctx.author.id)
		}
		with open("./data/tag.json", "w") as f:
			json.dump(tag, f, indent=4)
		await ctx.send(content=f"Tag ``{tag_name}`` created.", ephemeral=True)


	@interactions.extension_modal(modal="edit_tag")
	async def edit_tag(self, ctx: interactions.CommandContext, tag_name: str, tag_description: str):
		guild_id = ctx.guild_id
		with open("./data/tag.json", "r") as f:
			tags = json.load(f)
			tags[guild_id][tag_name] = {
				"description": tag_description,
				"created_at": tags[guild_id][tag_name]["created_at"],
				"author": tags[guild_id][tag_name]["author"]
			}
		with open("./data/tag.json", "w") as f:
			json.dump(tags, f, indent=4)
		await ctx.send(f"Tag ``{tag_name}`` edited.", ephemeral=True)


	@tag.autocomplete("tag_name")
	async def auto_complete(self, ctx:interactions.CommandContext, tag_name: str = ""):
		guild_id = ctx.guild_id
		letters: list = list(tag_name) if tag_name != "" else []
		tags = json.loads(open("./data/tag.json", "r").read())
		if guild_id in tags:
			if len(tag_name) == 0:
				await ctx.populate([interactions.Choice(name=tag[0], value=tag[0]) for tag in (
					list(tags[guild_id].items())[0:24] if len(tags) > 25 else list(tags[guild_id].items())
				)])
			else:
				choices: list = []
				for tag in tags[guild_id]:
					focus: str = "".join(letters)
					if focus.lower() in tag.lower():
						choices.append(interactions.Choice(name=tag, value=tag))
				await ctx.populate(choices)
		else:
			return






def setup(bot):
	return Tag(bot)
