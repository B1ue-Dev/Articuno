"""
This module is used to handle auto moderation actions.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import re
import interactions


class Automod(interactions.Extension):
    """Extension for Automod actions (mostly for my own server)."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_listener(name="on_message_create")
    async def _message_create(self, message: interactions.Message):
        message_content = str(message.content.lower())
        if message.guild_id is not None and int(message.guild_id) == 859030372783751168:

            # If someone sends an invite link
            discord_invite = r"(?:(?:discord.?(?:gg|io|me|li)|discord(?:app)?.?com[/\\]{1,}(?:invite))(?:[\S]+)?[/\\]{1,}([^\s/]+?)(?=\b))|discord://-/invite/([^\s/]+?)(?=\b)"
            if re.search(discord_invite, message_content):
                channel = await message.get_channel()
                await message.delete()
                await channel.send(
                    f"{message.author.mention}, your message was deleted because it contained an unauthorized invite link."
                )
                return

            # If someone mentions the bot
            if (
                f"@{self.client.me.id}" in message_content
                or f"<@{self.client.me.id}>" in message_content
            ):
                channel = await message.get_channel()
                embed = interactions.Embed(
                    title="It seems like you mentioned me",
                    description=f"I could not help much but noticed you mentioned me. You can type ``/`` and choose **{self.client.me.name}** to see a list of available commands.",
                    color=0x6AA4C1,
                )
                await channel.send(embeds=embed)

        else:
            # If someone mentions the bot
            if (
                f"@{self.client.me.id}" in message_content
                or f"<@{self.client.me.id}>" in message_content
            ):
                channel = await message.get_channel()
                embed = interactions.Embed(
                    title="It seems like you mentioned me",
                    description=f"I could not help much but noticed you mentioned me. You can type ``/`` and choose **{self.client.me.name}** to see a list of available commands.",
                    color=0x6AA4C1,
                )
                await channel.send(embeds=embed)


def setup(client) -> None:
    """Loads the Automod extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Automod(client)
    logging.debug("""[%s] Loaded Automod extension.""", log_time)
