import interactions
import os, json, datetime
from interactions.ext import wait_for
from dotenv import load_dotenv
load_dotenv()

scope = int(os.getenv("SCOPE"))



class Tag(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot
		wait_for.setup(bot, add_method=True)


	@interactions.extension_command(
		name="tag",
		description="Tag",
		scope=scope,
		options=[
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="create",
				description="Create a tag"
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
						autocomplete=True
					)
				]
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
						autocomplete=True
					)
				]
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
						autocomplete=True
					)
				]
			),
			interactions.Option(
				type=interactions.OptionType.SUB_COMMAND,
				name="list",
				description="List all tags"
			)
		]
	)
	async def _tag(self, ctx: interactions.CommandContext,
		sub_command: str,
		tag_name: str = None,
	):
		if sub_command == "create":
			await self._create_tag(ctx)
		elif sub_command == "view":
			await self._view_tag(ctx, tag_name)
		elif sub_command == "edit":
			await self._edit_tag(ctx, tag_name)
		elif sub_command == "delete":
			await self._delete_tag(ctx, tag_name)
		elif sub_command == "list":
			await self._list_tag(ctx)


	async def _create_tag(self, ctx: interactions.CommandContext):
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


	async def _view_tag(self, ctx: interactions.CommandContext, tag_name: str):
		guild_id = ctx.guild_id
		tags = json.loads(open("./db/tag.json", "r").read())
		if guild_id in tags:
			if tag_name in tags[guild_id]:
				await ctx.send(content=tags[guild_id][tag_name]["description"])
			else:
				await ctx.send("Tag not found.", ephemeral=True)
		else:
			await ctx.send(f"This guild does not have any registered tag.", ephemeral=True)


	async def _edit_tag(self, ctx: interactions.CommandContext, tag_name: str):
			guild_id = ctx.guild_id
			tags = json.loads(open("./db/tag.json", "r").read())
			if guild_id in tags:
				if tag_name in tags[guild_id]:
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
								value=tags[guild_id][tag_name]["description"],
							),
						],
					)
					await ctx.popup(modal)
				else:
					await ctx.send(f"Tag {tag_name} not found.", ephemeral=True)
			else:
				await ctx.send(f"This guild does not have any registered tag.", ephemeral=True)


	async def _delete_tag(self, ctx: interactions.CommandContext, tag_name: str):
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
			tags = json.loads(open("./db/tag.json", "r").read())
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


	async def _list_tag(self, ctx: interactions.CommandContext):
			guild_id = ctx.guild_id
			tags = json.loads(open("./db/tag.json", "r").read())
			if guild_id in tags:
				embed = interactions.Embed(
					title="Tags",
					description="\n".join(tags[guild_id].keys()),
				)
				await ctx.send(embeds=embed)
			else:
				await ctx.send(f"This guild does not have any registered tag.", ephemeral=True)




	"""
	Models for the commands.
	"""
	@interactions.extension_modal(modal="new_tag")
	async def _new_tag(self, ctx: interactions.CommandContext, tag_name: str, tag_description: str):
		guild_id = ctx.guild_id
		guild_id = str(guild_id)
		with open("./data/tag.json", "r") as f:
			tag1 = json.load(f)
			if guild_id not in tag1:
				guild_add = {
					guild_id: {}
				}
				with open("./db/tag.json", "w") as f:
					json.dump(guild_add, f, indent=4)
		tag = json.loads(open("./db/tag.json", "r").read())
		tag[guild_id][tag_name] = {
			"description": tag_description
		}
		with open("./data/tag.json", "w") as f:
			json.dump(tag, f, indent=4)
		await ctx.send(content=f"Tag ``{tag_name}`` created.", ephemeral=True)


	@interactions.extension_modal(modal="edit_tag")
	async def _edit_tag(self, ctx: interactions.CommandContext, tag_name: str, tag_description: str):
		guild_id = ctx.guild_id
		with open("./db/tag.json", "r") as f:
			tags = json.load(f)
			tags[guild_id][tag_name] = {
				"description": tag_description,
				"created_at": tags[guild_id][tag_name]["created_at"],
				"author": tags[guild_id][tag_name]["author"]
			}
		with open("./db/tag.json", "w") as f:
			json.dump(tags, f, indent=4)
		await ctx.send(f"Tag ``{tag_name}`` edited.", ephemeral=True)




	"""
	Tag autocomplete.
	"""
	@interactions.extension_autocomplete(
		command="tag",
		name="tag_name"
	)
	async def _tag_autocomplete(self, ctx: interactions.CommandContext, tag_name: str = ""):
		guild_id = ctx.guild_id
		letters: list = list(tag_name) if tag_name != "" else []
		tags = json.loads(open("./data/tag.json", "r", encoding="utf8").read())
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
	Tag(bot)