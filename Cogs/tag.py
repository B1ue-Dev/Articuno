import interactions
from interactions.ext.wait_for import wait_for
import os, json, datetime
from dotenv import load_dotenv
load_dotenv()

scope = int(os.getenv("SCOPE"))



class Tag(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot
		wait_for.setup(bot, add_method=True)

	"""
	Tag create: Create a tag.
	"""

	@interactions.extension_command(
		name="tag_create",
		description="Tag (in development)",
		scope=scope)
	async def tag_create(self, ctx: interactions.CommandContext):
		modal = interactions.Modal(
			title="Create new tag",
			custom_id="new_tag",
			components=[
				interactions.TextInput(
					style=interactions.TextStyleType.SHORT,
					label="Name of the tag",
					placeholder="Placeholder name",
					custom_id="name",
					max_length=100,
				),
				interactions.TextInput(
					style=interactions.TextStyleType.PARAGRAPH,
					label="Description of the tag",
					placeholder="Placeholder description",
					custom_id="description",
					max_length=2000,
				),
			],
		)
		await ctx.popup(modal)

	@interactions.extension_modal(modal="new_tag")
	async def new_tag(self, ctx: interactions.CommandContext, name: str, description: str):
		guild_id = ctx.guild_id
		with open("./data/tag.json", "r") as f:
			tags = json.load(f)
			tags[guild_id][name] = {
				"description": description,
			}
		with open("./data/tag.json", "w") as f:
			json.dump(tags, f, indent=4)
		await ctx.send(f"Tag ``{name}`` created!")



	"""
	Tag view: View a tag.
	"""

	@interactions.extension_command(
		name="tag_view",
		description="View a tag (in development)",
		scope=scope,
		options = [
			interactions.Option(
				type=interactions.OptionType.STRING,
				name="name",
				description="The name of the tag you wish to view.",
				required=True,
				autocomplete=True,)])
	async def tag_view(self, ctx: interactions.CommandContext, name: str):
		guild_id = ctx.guild_id
		tag = json.loads(open("./data/tag.json", "r").read())
		if guild_id in tag:
			if name in tag[guild_id]:
				embed = interactions.Embed(
					title=f"Tag: {name}",
					description=tag[guild_id][name]["description"],
				)
				await ctx.send(embeds=embed)
			else:
				await ctx.send("Tag not found.")




	"""
	Tag edit: Edit a tag.
	"""

	@interactions.extension_command(
		name="tag_edit",
		description="Edit a tag (in development)",
		scope=scope,
		options = [
			interactions.Option(
				type=interactions.OptionType.STRING,
				name="name",
				description="The name of the tag you wish to edit.",
				required=True,
				autocomplete=True,)])
	async def tag_edit(self, ctx: interactions.CommandContext, name: str):
		guild_id = ctx.guild_id
		tag = json.loads(open("./data/tag.json", "r").read())
		if guild_id in tag:
			if name in tag[guild_id]:
				modal = interactions.Modal(
					title=f"Edit tag: {name}",
					custom_id="edit_tag",
					components=[
						interactions.TextInput(
							style=interactions.TextStyleType.SHORT,
							label="Name of the tag",
							placeholder="Placeholder name",
							custom_id="name",
							max_length=100,
							value=name,
						),
						interactions.TextInput(
							style=interactions.TextStyleType.PARAGRAPH,
							label="Description of the tag",
							placeholder="Placeholder description",
							custom_id="description",
							max_length=2000,
							value=tag[guild_id][name]["description"],
						),
					],
				)
				await ctx.popup(modal)
			else:
				await ctx.send("Tag not found.")

	@interactions.extension_modal(modal="edit_tag")
	async def edit_tag(self, ctx: interactions.CommandContext, name: str, description: str):
		guild_id = ctx.guild_id
		with open("./data/tag.json", "r") as f:
			tags = json.load(f)
			tags[guild_id][name] = {
				"description": description,
			}
		with open("./data/tag.json", "w") as f:
			json.dump(tags, f, indent=4)
		await ctx.send(f"Tag ``{name}`` edited!")



	"""
	Tag delete: Delete a tag.
	"""
	@interactions.extension_command(
		name="tag_delete",
		description="Delete a tag (in development)",
		scope=scope,
		options = [
			interactions.Option(
				type=interactions.OptionType.STRING,
				name="name",
				description="The name of the tag you wish to delete.",
				required=True,
				autocomplete=True,)])
	async def tag_delete(self, ctx: interactions.CommandContext, name: str):
		guild_id = ctx.guild_id
		tag = json.loads(open("./data/tag.json", "r").read())
		if guild_id in tag:
			if name in tag[guild_id]:
				res = 
				del tag[guild_id][name]
				with open("./data/tag.json", "w") as f:
					json.dump(tag, f, indent=4)
				await ctx.send(f"Tag ``{name}`` deleted!")
			else:
				await ctx.send("Tag not found.")



	"""
	Tag list: List all tags.
	"""
	@interactions.extension_command(
		name="tag_list",
		description="List all tags (in development)",
		scope=scope)
	async def tag_list(self, ctx: interactions.CommandContext):
		guild_id = ctx.guild_id
		tag = json.loads(open("./data/tag.json", "r").read())
		if guild_id in tag:
			embed = interactions.Embed(
				title="Tags",
				description="\n".join(tag[guild_id].keys()),
			)
			await ctx.send(embeds=embed)
		else:
			await ctx.send("No tags found.")


	"""
	Tag autocomplete.
	"""

	@interactions.extension_autocomplete(
		command=962785667711139880,
		name="name",)
	async def view_tag(self, ctx: interactions.CommandContext, name: str = ""):
		guild_id = ctx.guild_id
		letters: list = list(name) if name != "" else []
		tags = json.loads(open("./data/tag.json", "r").read())
		if guild_id in tags:
			if len(name) == 0:
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

	@interactions.extension_autocomplete(
		command=962785666268266626,
		name="name",)
	async def edit_tag(self, ctx: interactions.CommandContext, name: str = ""):
		guild_id = ctx.guild_id
		letters: list = list(name) if name != "" else []
		tags = json.loads(open("./data/tag.json", "r").read())
		if guild_id in tags:
			if len(name) == 0:
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