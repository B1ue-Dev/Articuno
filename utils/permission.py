# from: https://github.com/CommandMC/EpicFreeGamesBot/blob/main/epicfreegamesbot/permissions.py # noqa
from enum import Enum
from typing import Union


# https://discord.com/developers/docs/topics/permissions#permissions-bitwise-permission-flags
class Permissions(Enum):
    """A class representing Permission."""

    CREATE_INSTANT_INVITE = 0
    KICK_MEMBERS = 1
    BAN_MEMBERS = 2
    ADMINISTRATOR = 3
    MANAGE_CHANNELS = 4
    MANAGE_GUILD = 5
    ADD_REACTIONS = 6
    VIEW_AUDIT_LOG = 7
    PRIORITY_SPEAKER = 8
    STREAM = 9
    VIEW_CHANNEL = 10
    SEND_MESSAGES = 11
    SEND_TTS_MESSAGES = 12
    MANAGE_MESSAGES = 13
    EMBED_LINKS = 14
    ATTACH_FILES = 15
    READ_MESSAGE_HISTORY = 16
    MENTION_EVERYONE = 17
    USE_EXTERNAL_EMOJIS = 18
    VIEW_GUILD_INSIGHTS = 19
    CONNECT = 20
    SPEAK = 21
    MUTE_MEMBERS = 22
    DEAFEN_MEMBERS = 23
    MOVE_MEMBERS = 24
    USE_VAD = 25
    CHANGE_NICKNAME = 26
    MANAGE_NICKNAMES = 27
    MANAGE_ROLES = 28
    MANAGE_WEBHOOKS = 29
    MANAGE_EMOJIS_AND_STICKERS = 30
    USE_APPLICATION_COMMANDS = 31
    REQUEST_TO_SPEAK = 32
    MANAGE_EVENTS = 33
    MANAGE_THREADS = 34
    CREATE_PUBLIC_THREADS = 35
    CREATE_PRIVATE_THREADS = 36
    USE_EXTERNAL_STICKERS = 37
    SEND_MESSAGES_IN_THREADS = 38
    START_EMBEDDED_ACTIVITIES = 39
    MODERATE_MEMBERS = 40


# https://discord.com/developers/docs/topics/permissions#permissions
def has_permission(
    permission_val: int, permission: Union[Permissions, int]
) -> bool:
    """Check if the user's permission value is equal to the given permission for an action.

    :param permission_val: The user permission value.
    :type permission_val: int
    :param permission: The permission that will be used to compare.
    :type permission: Permission
    :return: True if user has permission, False if not.
    :rtype: bool
    """

    if isinstance(permission, Permissions):
        permission = permission.value

    return permission_val & (1 << permission) == 1 << permission
