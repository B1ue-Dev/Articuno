"""
Cache system for guild_count/user_count

(C) 2022 - Jimmy-Blue
"""

import interactions

_sets_guilds: set = set()
__cached__: dict = dict()


class Cache(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    _sets_guilds: set = set()
    __cached__: dict = dict()

    @interactions.extension_listener(name="on_guild_create")
    async def _guild_create(self, guild: interactions.Guild):
        __cached__[int(guild.id)] = []
        for member in guild.members:
            __cached__[int(guild.id)].append(int(member.id))
        _sets_guilds.add(int(guild.id))

    @interactions.extension_listener(name="on_guild_delete")
    async def _guild_remove(self, guild: interactions.Guild):
        del __cached__[int(guild.id)]
        _sets_guilds.remove(int(guild.id))


def setup(bot):
    Cache(bot)