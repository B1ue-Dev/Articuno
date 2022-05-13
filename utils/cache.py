import interactions
from interactions import extension_listener as listener

_sets_guilds: set = set()
__cached__: dict = dict()





class Cache(interactions.Extension):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot = bot

	"""
	Cache system for guild_count/user_count
	"""

	_sets_guilds: set = set()
	__cached__: dict = dict()

	@listener(name="on_guild_create")
	async def _guild_create(self, guild: interactions.Guild):
		__cached__[int(guild.id)] = []
		for member in guild.members:
			__cached__[int(guild.id)].append(int(member.id))
		_sets_guilds.add(int(guild.id))

	@listener(name="on_guild_delete")
	async def _guild_remove(self, guild: interactions.Guild):
		del __cached__[int(guild.id)]
		_sets_guilds.remove(int(guild.id))






def setup(bot):
	Cache(bot)