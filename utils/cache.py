"""
A custom cache system.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import interactions


class Storage:
    """A class representing a storage. This is used to store data as dicts, lists."""

    _guilds = (
        list()
    )  # Format: {guild1: [user1, user2, ...], guild2: [user1, user2, ...], ...}
    _logs = dict()  # Format: {guild1: channel1, guild2: channel2, ...}
    _welcome_goodbye = dict()  # Format: {guild1: channel1, guild2: channel2, ...}

    def add_guild(self, guild: interactions.Guild):
        """Add a new guild to the storage."""
        self._guilds.append(guild)

    def remove_guild(self, guild: interactions.Guild):
        """Remove a guild from the storage."""

        self._guilds.remove(guild)

    def get_all_guilds(self) -> interactions.Guild:
        """Return the list of all guilds."""
        return self._guilds

    def get_all_users(self) -> int:
        """Return the number of all users."""
        count = 0
        for guild in self._guilds:
            count += guild.member_count
        return count

    def add_logs(self, guild_id: str, channel_id: str):
        """Add a new log channel id to the storage."""
        self._logs[str(guild_id)] = str(channel_id)

    def add_welcome_goodbye(self, guild_id: str, channel_id: str):
        """Add a new welcome goodbye channel id to the storage."""
        self._welcome_goodbye[str(guild_id)] = str(channel_id)


class Cache(interactions.Extension):
    """A class representing cache."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.storage = Storage()

    @interactions.extension_listener(name="on_guild_create")
    async def on_guild_create(self, guild: interactions.Guild):
        """Add guild to cache."""

        self.storage.add_guild(guild)

    @interactions.extension_listener(name="on_guild_delete")
    async def on_guild_delete(self, guild: interactions.Guild):
        """Remove guild from cache."""

        self.storage.remove_guild(guild)

    @interactions.extension_listener(name="on_channel_create")
    async def _channel_create(self, channel: interactions.Channel):
        guild_id = str(channel.guild_id)
        if (
            channel.name == "logs"
            and guild_id not in self.storage._logs
            or self.storage._logs[guild_id] == None
        ):
            self.storage.add_logs(guild_id, str(channel.id))

        elif (
            channel.name == "welcome-goodbye"
            and guild_id not in self.storage._welcome_goodbye
            or self.storage._welcome_goodbye[guild_id] == None
        ):
            print("welcome-goodbye created")
            self.storage.add_welcome_goodbye(guild_id, str(channel.id))

    @interactions.extension_listener(name="on_raw_channel_update")
    async def _channel_update(self, channel: interactions.Channel):
        guild_id = str(channel.guild_id)
        if guild_id in self.storage._logs:
            _cache_channel_id = self.storage._logs[guild_id]

            if (
                str(channel.id) == _cache_channel_id
                and channel.type != interactions.ChannelType.GUILD_TEXT
                or channel.name != "logs"
            ):
                self.storage._logs[guild_id] = None

            elif (
                channel.name == "logs"
                and channel.type == interactions.ChannelType.GUILD_TEXT
            ):
                self.storage._logs[guild_id] = str(channel.id)

        elif guild_id in self.storage._welcome_goodbye:
            _cache_channel_id = self.storage._welcome_goodbye[guild_id]

            if (
                str(channel.id) == _cache_channel_id
                and channel.type != interactions.ChannelType.GUILD_TEXT
                or channel.name != "welcome-goodbye"
            ):
                self.storage._welcome_goodbye[guild_id] = None

            elif (
                channel.name == "welcome-goodbye"
                and channel.type == interactions.ChannelType.GUILD_TEXT
            ):
                self.storage._welcome_goodbye[guild_id] = str(channel.id)

    @interactions.extension_listener(name="on_channel_delete")
    async def _channel_delete(self, channel: interactions.Channel):
        guild_id = str(channel.guild_id)
        if guild_id in self.storage._logs:
            if self.storage._logs[guild_id] == str(channel.id):
                self.storage._logs[guild_id] = None

        elif guild_id in self.storage._welcome_goodbye:
            if self.storage._welcome_goodbye[guild_id] == str(channel.id):
                self.storage._welcome_goodbye[guild_id] = None


def setup(client):
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Cache(client)
    logging.debug("""[%s] Loaded Cache extension.""", log_time)
    print(f"[{log_time}] Loaded Cache extension.")
