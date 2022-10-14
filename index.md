# Articuno [![Better Uptime Badge](https://betteruptime.com/status-badges/v1/monitor/c1yv.svg)](https://betteruptime.com/?utm_source=status_badge) [![wakatime](https://wakatime.com/badge/github/Articuno-org/Articuno.svg)](https://wakatime.com/badge/github/Jimmy-Blue/Articuno)
A fun Discord Bot, written with interactions.py.

![banner.png](./articuno_banner.png)

[![Invite link](https://img.shields.io/static/v1?label=Articuno&message=Invite-to-server&color=6aa4c1&style=for-the-badge&logo=discord)](https://discord.com/oauth2/authorize?client_id=809084067446259722&permissions=2146958847&scope=bot%20applications.commands)


# Feature

Articuno is a multi-purpose Discord Bot that can do a wide variety of jobs, mostly with fun commands. It has a tag system (text) allows you to store and send multiple tags that suit with your server. Featuring an emoji management system, where you can steal and add emojis from other servers (Nitro or image url), remove and look up for the information about an emoji in your server. There is an image search command (powered by Google Images) allows you to look up for different images. Articuno also has a TTS command allows you to have a sentence spoken by different actors from Uberduck. Beside as a fun bot, Articuno also contains a moderation system with logging and a wide variety of msic commands to enhance your server experience.

## Highlight commands:

- ``/img``: Look up for images from Google Images.

- ``/tag``: A message tag system (view, create, edit, info, delete, list).

- ``/emoji``: An emoji management system (info, steal, add, remove).

- ``/tts``: Get the message spoken by a character.

- ``/mod``: Moderation commands (kick, ban, hackban, unban, timeout, untimeout).

- ``/snipe``: Want to see the most recent deleted message in the chat? /snipe

## Built in message log system and join/leave
Articuno has a built in log system for deleted message, user join/remove.

- For message logs: Name a channel with ``logs``. This will log crucial events, such as ban, timeout, deleted/edited messages, etc.

- For join/leave message: Channel with the name ``welcome-goodbye``. This will send an embed message whenever there is a new user who just recently joined the server or someone who just leave the server.

## Misc commands
Articuno has a good range of miscellaneous commands, such as ``amogus``, ``gay``, ``flip``, ``simpcard``, ``hug``, ``ship``, etc. You can have a look more at the bot command list after adding Articuno to your server.

## For Pokemon

- There is a ``/pokedex`` command so you can look up for information about a Pokemon. What is special about this Pokedex command compared to the others is a featured called auto-complete, so you can look up for information about your Pokemon easier.

- ``/who_is_that_pokemon`` The famous "Who's that Pokemon" game from the franchise.

- ``$<pokemon_name>`` Send a sprite of a Pokemon.

- ``$shiny <pokemon_name>`` Send a shiny sprite of a Pokemon.

# What makes us different?
First and always, API wrapper library. Being developed using Python, many developers will go with [discord.py](https://github.com/Rapptz/discord.py). We think discord.py is a good library, however, it violates the API and does not follow the API guild schema. With all of those reasons, we decided to follow [interactions.py](https://github.com/interactions-py/library), a Python Discord API Wrapper, focusing on interaction based. A wrapper with proper Objects, Classes, and most importantly, interactions.py follows the API guide from Discord, which is a huge pro for the library itself.
