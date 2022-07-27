"""
A custom cache system.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import interactions


class Storage:
    """A class representing a storage. This is used to store data as dicts, lists."""

    _guilds = list() # Format: [guild1, guild2, ...]
    _guild = dict() # Format: {guild1: [user1, user2, ...], guild2: [user1, user2, ...], ...}
    _logs = dict() # Format: {guild1: channel1, guild2: channel2, ...}
    _welcome_goodbye = dict() # Format: {guild1: channel1, guild2: channel2, ...}
    _special_guilds = dict() # Format: {Guild: [User, User, ...], Guild: [User, User, ...], ...}
    _emojis = dict()

    def add_guild(self, guild_id: str):
        """
        Add a new guild to the storage.

        :param guild_id: The guild id
        :type guild_id: str
        """

        self._guilds.append(str(guild_id))
        self._guild[str(guild_id)] = []

    def remove_guild(self, guild_id: str):
        """
        Remove a guild from the storage.

        :param guild_id: The guild id
        :type guild_id: str
        """

        self._guilds.remove(str(guild_id))
        self._guild.pop(str(guild_id))
        self._logs.pop(str(guild_id))

    def get_all_guilds(self):
        """Return the list of all guilds."""
        return self._guilds

    def get_guild(self, guild_id: str):
        """
        Return the list of all users in a guild.

        :param guild_id: The guild id
        :type guild_id: str
        """

        return self._guild[str(guild_id)]

    def get_all_guild_members(self, guild_id: str):
        """
        Return the list of all users in a guild.

        :param guild_id: The guild id
        :type guild_id: str
        """

        return self._guild[str(guild_id)]

    def get_all_users(self):
        """Return the number of all users."""
        count = 0
        for guild in self._guild:
            for user in guild:
                count += 1
        return count

    def add_user(self, guild_id: str, user_id: str):
        """
        Add a new user to the storage.

        :param guild_id: The guild id
        :type guild_id: str
        :param user_id: The user id
        :type user_id: str
        """

        self._guild[str(guild_id)].append(str(user_id))

    def remove_user(self, guild_id: str, user_id: str):
        """
        Remove a user from the storage.

        :param guild_id: The guild id
        :type guild_id: str
        :param user_id: The user id
        :type user_id: str
        """

        self._guild[str(guild_id)].remove(str(user_id))

    def add_logs(self, guild_id: str, channel_id: str):
        """
        Add a new log channel id to the storage.

        :param guild_id: The guild id
        :type guild_id: str
        :param channel_id: The channel id
        :type channel_id: str
        """

        self._logs[str(guild_id)] = str(channel_id)
        self._logs[str(guild_id)] = str(channel_id)

    def get_all_logs(self):
        """Return the list of all logs."""
        return self._logs

    def add_welcome_goodbye(self, guild_id: str, channel_id: str):
        """
        Add a new welcome goodbye channel id to the storage.

        :param guild_id: The guild id
        :type guild_id: str
        :param channel_id: The channel id
        :type channel_id: str
        """

        self._welcome_goodbye[str(guild_id)] = str(channel_id)

    def add_emoji(self, guild_id: str, emoji_id: str):
        """
        Add a new emoji id to the storage.

        :param guild_id: The guild id
        :type guild_id: str
        :param emoji_id: The emoji id
        :type emoji_id: str
        """

        self._emojis[str(guild_id)] = str(emoji_id)


class Cache(interactions.Extension):
    """A class representing cache."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.storage = Storage()

    @interactions.extension_listener(name="on_guild_create")
    async def _guild_create(self, guild: interactions.Guild):
        self.storage.add_guild(str(guild.id))
        self.storage._special_guilds[guild] = []
        for member in guild.members:
            self.storage._guild[str(guild.id)].append(str(member.id))
            self.storage._special_guilds[guild].append(member.user)

    @interactions.extension_listener(name="on_guild_delete")
    async def _guild_delete(self, guild: interactions.Guild):
        self.storage.remove_guild(str(guild.id))
        self.storage._special_guilds.pop(guild)

    @interactions.extension_listener(name="on_channel_create")
    async def _channel_create(self, channel: interactions.Channel):
        guild_id = str(channel.guild_id)
        if (
            channel.name == "logs"
            and guild_id not in self.storage._guilds
            or self.storage._guild[guild_id] == None
        ):
            self.storage.add_logs(guild_id, str(channel.id))

        elif (
            channel.name == "welcome-goodbye"
            and guild_id not in self.storage._guilds
            or self.storage._guild[guild_id] == None
        ):
            print("welcome-goodbye created")
            self.storage.add_welcome_goodbye(guild_id, str(channel.id))

    @interactions.extension_listener(name="on_channel_update")
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
    log_time = (
        datetime.datetime.now() + datetime.timedelta(hours=7)
    ).strftime("%d/%m/%Y %H:%M:%S")
    Cache(client)
    logging.debug("""[%s] Loaded Cache extension.""", log_time)
    print(f"[{log_time}] Loaded Cache extension.")
