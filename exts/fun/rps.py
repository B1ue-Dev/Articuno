"""
Rock-paper-scissors command.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import random
import asyncio
import pprint
import interactions
from interactions.ext.wait_for import wait_for_component


buttons = [
    interactions.ActionRow(
        components=[
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="◄",
                custom_id="previous",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label="►",
                custom_id="next",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label="■",
                custom_id="stop",
            ),
        ],
    ),
]

rps_selection = interactions.SelectMenu(
    options=[
        interactions.SelectOption(
            label="Rock",
            emoji=interactions.Emoji(name="🪨"),
            value="1",
        ),
        interactions.SelectOption(
            label="Paper",
            emoji=interactions.Emoji(name="📃"),
            value="2",
        ),
        interactions.SelectOption(
            label="Scissors",
            emoji=interactions.Emoji(name="✂"),
            value="3",
        ),
    ],
    placeholder="Choose your option",
    custom_id="rps_selection",
    min_values=1,
    max_values=1,
)


def rps_get_winner(a_choice, b_choice):
    """
    Decide if the author is the winner in a Rock-Paper-Scissors match.

    :param a_choice: 1st choice. ["1", "2", "3"].
    :type a_choice: str
    :param b_choice: 2nd choice ["1", "2", "3"].
    :type b_choice: str
    :return: String with whether the author won, tied or lost.
    :rtype: bool | None
    """

    if a_choice == b_choice:
        return None

    if (a_choice - b_choice) % 3 == 1:
        return True

    if (a_choice - b_choice) % 3 == 2:
        return False


class RPS(interactions.Extension):
    """Extension for /rock_paper_scissors command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.choice_convert: dict = {1: "Rock", 2: "Paper", 3: "Scissors"}

    @interactions.extension_command(
        name="rock_paper_scissors",
        description="Play a game of Rock-Paper-Scissors.",
    )
    async def rock_paper_scissors(self, *args, **kwargs):
        """Play a game of Rock-Paper-Scissors."""
        ...

    @rock_paper_scissors.subcommand(
        name="ai",
        description="Play against Articuno.",
    )
    async def rock_paper_scissors_ai(self, ctx: interactions.CommandContext):
        """Play against Articuno."""

        rps_selection.disabled = False

        msg = await ctx.send(
            content=f"{ctx.user.mention} vs **Articuno**",
            components=rps_selection,
            allowed_mentions={"users": []},
        )

        while True:
            try:
                res = await wait_for_component(
                    self.client,
                    components=rps_selection,
                    messages=int(ctx.message.id),
                    timeout=15,
                )

                if int(res.user.id) == int(ctx.user.id):
                    rps_selection.disabled = True

                    user_choice = int(res.data.values[0])
                    bot_choice = int(random.randint(1, 3))

                    result = rps_get_winner(user_choice, bot_choice)

                    if result is None:
                        await res.edit(
                            content="".join(
                                [
                                    f"{res.user.mention} chose **{self.choice_convert[user_choice]}**.\n",
                                    f"**Articuno** chose **{self.choice_convert[bot_choice]}**.\n",
                                    "> It's a `TIE`!",
                                ]
                            ),
                            components=rps_selection,
                            allowed_mentions={"parse": []},
                        )

                    elif result is True:
                        await res.edit(
                            content="".join(
                                [
                                    f"{res.user.mention} chose **{self.choice_convert[user_choice]}**.\n",
                                    f"**Articuno** chose **{self.choice_convert[bot_choice]}**.\n",
                                    f"> {res.user.mention} `WON`!",
                                ]
                            ),
                            components=rps_selection,
                            allowed_mentions={"parse": []},
                        )

                    elif result is False:
                        await res.edit(
                            content="".join(
                                [
                                    f"{res.user.mention} chose **{self.choice_convert[user_choice]}**.\n",
                                    f"**Articuno** chose **{self.choice_convert[bot_choice]}**.\n",
                                    "> **Articuno** `WON`!",
                                ]
                            ),
                            components=rps_selection,
                            allowed_mentions={"parse": []},
                        )
                    break

                else:
                    pass

            except asyncio.TimeoutError:
                rps_selection.disabled = True
                await msg.edit(content="Time's up!", components=rps_selection)
                break

    @rock_paper_scissors.subcommand(
        name="human",
        description="Play against someone else.",
    )
    @interactions.option(
        type=interactions.OptionType.USER,
        name="user",
        description="The user to play against",
    )
    async def rock_paper_scissors_human(
        self, ctx: interactions.CommandContext, user: interactions.User
    ):
        """Play against someone else."""

        # if int(ctx.user.id) == int(user.id):
        #     return await ctx.send("You cannot challenge yourself.", ephemeral=True)

        if int(user.id) == int(self.client.me.id):
            return await ctx.send(
                "To challenge me, do ``/rock_paper_scissors ai`` instead.",
                ephemeral=True,
            )

        rps_selection.disabled = False

        accept_deny = [
            interactions.ActionRow(
                components=[
                    interactions.Button(
                        style=interactions.ButtonStyle.SUCCESS,
                        label="Accept",
                        custom_id="accept",
                    ),
                    interactions.Button(
                        style=interactions.ButtonStyle.DANGER,
                        label="Deny",
                        custom_id="deny",
                    ),
                ]
            )
        ]

        msg = await ctx.send(
            content=f"{ctx.user.mention} challenged {user.mention}.",
            components=accept_deny,
            allowed_mentions={"users": [int(user.id)]},
        )

        while True:
            try:
                op: interactions.ComponentContext = await wait_for_component(
                    self.client,
                    components=accept_deny,
                    messages=int(ctx.message.id),
                    timeout=15,
                )

                if int(op.user.id) == int(user.id):
                    if op.custom_id == "accept":

                        await op.edit(
                            content=f"{ctx.user.mention} vs {user.mention}",
                            components=rps_selection,
                        )
                        user1 = int(ctx.user.id)
                        user2 = int(user.id)
                        cmp_1 = 0

                        while True:
                            cmp1: interactions.ComponentContext = (
                                await wait_for_component(
                                    self.client,
                                    components=rps_selection,
                                    messages=int(ctx.message.id),
                                    timeout=15,
                                )
                            )

                            if int(cmp1.user.id) == user1 or int(cmp1.user.id) == user2:
                                cmp_1 = int(cmp1.user.id)
                                await cmp1.edit(
                                    content=f"{cmp1.message.content}\n\n{cmp1.user.mention} has their option chosen."
                                )
                                choice1 = int(cmp1.data.values[0])
                                break

                            else:
                                pass

                        while True:
                            cmp2: interactions.ComponentContext = (
                                await wait_for_component(
                                    self.client,
                                    components=rps_selection,
                                    messages=int(ctx.message.id),
                                    timeout=15,
                                )
                            )

                            if int(cmp2.user.id) in {int(user1), int(user2)} and int(
                                cmp2.user.id
                            ) != int(cmp_1):
                                rps_selection.disabled = True
                                choice2 = int(cmp2.data.values[0])
                                break

                            else:
                                pass

                        result = rps_get_winner(choice1, choice2)

                        if result is None:
                            await cmp2.edit(
                                content="".join(
                                    [
                                        f"{ctx.user.mention} chose **{self.choice_convert[choice1]}**.\n"
                                        f"{user.mention} chose **{self.choice_convert[choice2]}**.\n"
                                        "> It is a tie!",
                                    ]
                                ),
                                components=rps_selection,
                                allowed_mentions={"users": []},
                            )

                        elif result is True:
                            await cmp2.edit(
                                content="".join(
                                    [
                                        f"{ctx.user.mention} chose **{self.choice_convert[choice1]}**.\n",
                                        f"{user.mention} chose **{self.choice_convert[choice2]}**.\n",
                                        f"> {ctx.user.mention} won!",
                                    ],
                                ),
                                components=rps_selection,
                                allowed_mentions={"users": [int(ctx.user.id)]},
                            )

                        elif result is False:
                            await cmp2.edit(
                                content="".join(
                                    [
                                        f"{ctx.user.mention} chose **{self.choice_convert[choice1]}**.\n",
                                        f"{user.mention} chose **{self.choice_convert[choice2]}**.\n",
                                        f"> {user.mention} won!",
                                    ]
                                ),
                                components=rps_selection,
                                allowed_mentions={"users": [int(user.id)]},
                            )

                        break

                    elif op.custom_id == "deny":
                        await msg.edit(
                            content=f"{user.mention} declined the challenge.",
                            components=[],
                            allowed_mentions={"users": []},
                        )

                        break

                elif (
                    int(op.user.id) != int(user.id)
                    and int(op.user.id) == int(ctx.user.id)
                    and op.custom_id == "deny"
                ):
                    await op.edit(
                        f"{ctx.user.mention} cancelled the challenge.", components=[]
                    )
                    break

                elif (
                    int(op.user.id) != int(user.id)
                    and int(op.user.id) == int(ctx.user.id)
                    and op.custom_id == "accept"
                ):
                    await op.send(
                        "You cannot accept the challenge by yourself.",
                        components=[],
                        ephemeral=True,
                    )

                else:
                    pass

            except asyncio.TimeoutError:
                await msg.edit(content="Time's up!", components=[])
                break


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    RPS(client)
    logging.debug("""[%s] Loaded RPS extension.""", log_time)
