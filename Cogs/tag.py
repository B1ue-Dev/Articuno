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


	@interactions.extension_modal(modal="new_tag")
	async def new_tag(self, ctx: interactions.CommandContext, name: str, description: str):
		embed = interactions.Embed(title=name, description=description)
		await ctx.send(embeds=embed)
	





def setup(bot):
	Tag(bot)