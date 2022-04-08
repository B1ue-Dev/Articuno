import interactions
from interactions import extension_listener as listener


class Logs(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot
	

	@listener(name="on_message_create")
	async def message_create(self, message: interactions.Message):
		channel = await message.get_channel()
		if message.content == "$ping":
			await channel.send("Pong!")
	

	@listener(name="on_message_delete")
	async def message_delete(self, message: interactions.Message):
		guild = await message.get_guild()
		channel = await message.get_channel()
		channels = await guild.get_all_channels()
		logs = [ch._json for ch in await guild.get_all_channels() if int(ch.name) == "logs"]
		await channel.send(f"```{logs}```")




def setup(bot):
	Logs(bot)