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
	




def setup(bot):
	Logs(bot)