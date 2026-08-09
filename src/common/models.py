from typing import Annotated
from beanie import Document, Indexed

from datetime import datetime

__all__ = (
    "tags",
    "hangman_saves",
    "wtp_easy_saves",
    "wtp_hard_saves",
)


# Tag save model
class tags(Document):
    guild_id: str
    tags: dict


# Hangman saves model
class hangman_saves(Document):
    user_id: Annotated[int, Indexed(int)]
    user_name: Annotated[str, Indexed(str)]
    highest_point: Annotated[int, Indexed(int)]
    history: list


# WTP (Who's that Pokemon) Easy mode model
class wtp_easy_saves(Document):
    user_id: Annotated[int, Indexed(int)]
    user_name: Annotated[str, Indexed(str)]
    points: Annotated[int, Indexed(int)]
    history: list


# WTP Hard mode model
class wtp_hard_saves(Document):
    user_id: Annotated[int, Indexed(int)]
    user_name: Annotated[str, Indexed(str)]
    points: Annotated[int, Indexed(int)]
    history: list


# Count command use for Articuno
class usage(Document):
    """
    A class for MongoDB Document representing command usage.
    """

    command_name: Annotated[str, Indexed(str)]
    """The name of the command run."""
    timestamp: Annotated[datetime, Indexed(datetime)]
    """The timestamp when the command was run."""
    user_id: Annotated[int, Indexed(int)]
    """The ID of the user who ran the command."""
