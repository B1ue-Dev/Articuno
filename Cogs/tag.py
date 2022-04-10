import interactions
import os, json, datetime
from dotenv import load_dotenv
load_dotenv()

scope = int(os.getenv("SCOPE"))



class Tag(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot

	@interactions.extension_command(
		name="tag",
		description="Tag (in development)",
		scope=scope
	)
	async def create_tag(self, ctx: interactions.CommandContext):
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
				autocomplete=True,
			)
		]
	)
	async def view_tag(self, ctx: interactions.CommandContext, name: str):
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


	@interactions.extension_modal(modal="new_tag")
	async def new_tag(self, ctx: interactions.CommandContext, name: str, description: str):
		with open("./data/tag.json", "r") as f:
			tags = json.load(f)
			tags[name] = {
				"description": description,
			}
		with open("./data/tag.json", "w") as f:
			json.dump(tags, f, indent=4)
		await ctx.send(f"Tag ``{name}`` created!")

	@interactions.extension_autocomplete(
		command=962728252584108092,
		name="name",
	)
	async def tag_view(self, ctx: interactions.CommandContext, name: str = ""):
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