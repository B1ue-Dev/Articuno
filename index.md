[![Invite link](https://img.shields.io/static/v1?label=Articuno&message=Invite-to-server&color=6aa4c1&style=for-the-badge&logo=discord)](https://discord.com/oauth2/authorize?client_id=809084067446259722&permissions=1644972474366&scope=bot%20applications.commands) [![Better Uptime Badge](https://betteruptime.com/status-badges/v1/monitor/c1yv.svg)](https://betteruptime.com/?utm_source=status_badge)


![banner.png](./articuno_banner.png)


> This is a full rewrite from scratch, using [interactions.py](https://github.com/interactions-py/library).


# (Testing) A minimal bot
Instruction:
- Install requirements library: ``pip install -r requirements.txt``
- Put your bot's token in ``./data/config.json``
- Run ``python main.py``

# Testing [replit](https://github.com/Jimmy-Blue/Articuno/tree/replit)
- Fork this repository.
- Create an account on Replit and host on there
- Alternatively, you can self host by following this instruction:
> Install ``python-dotenv``: ``pip install -U python-dotenv``

> Create a ``.env`` file and put your token as:
```TOKEN=<your_token_here>```

> In your main.py file, replace ``os.environ`` with:
```load_dotenv()
bot_token = os.getenv("TOKEN")
```

> Run the bot: ``$ python main.py``

