"""
Rock-paper-scissors command.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import random
import asyncio
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_subcommand,
    HybridContext,
)


buttons = [
    interactions.ActionRow(
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
    ),
]

rps_selection = interactions.StringSelectMenu(
    [
        interactions.StringSelectOption(
            label="Rock",
            emoji=interactions.PartialEmoji(name="🪨"),
            value="1",
        ),
        interactions.StringSelectOption(
            label="Paper",
            emoji=interactions.PartialEmoji(name="📃"),
            value="2",
        ),
        interactions.StringSelectOption(
            label="Scissors",
            emoji=interactions.PartialEmoji(name="✂"),
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

    @hybrid_slash_subcommand(
        base="rock_paper_scissors",
        base_description="Play a game of Rock-Paper-Scissors.",
        aliases=["rps"],
        name="ai",
        description="Play against Articuno.",
    )
    async def ai(self, ctx: HybridContext) -> None:
        """Play against Articuno."""

        rps_selection.disabled = False

        msg = await ctx.send(
            content=f"{ctx.user.mention} vs **Articuno**",
            components=rps_selection,
            allowed_mentions={"users": []},
        )

        while True:
            try:

                def _check(_ctx):
                    return int(_ctx.ctx.user.id) == int(ctx.user.id) and int(
                        _ctx.ctx.channel_id
                    ) == int(ctx.channel_id)

                res = await self.client.wait_for_component(
                    components=rps_selection,
                    check=_check,
                    messages=int(msg.id),
                    timeout=15,
                )

                rps_selection.disabled = True

                user_choice = int(res.ctx.values[0])
                bot_choice = int(random.randint(1, 3))
                result = rps_get_winner(user_choice, bot_choice)
                content: list[str] = [
                    f"{res.ctx.user.mention} chose ",
                    f"**{self.choice_convert[user_choice]}**.\n",
                    "**Articuno** chose ",
                    f"**{self.choice_convert[bot_choice]}**.\n",
                ]

                if result is None:
                    content.append("> It's a `TIE`!")
                elif result is True:
                    content.append(f"> {res.ctx.user.mention} `WON`!")
                elif result is False:
                    content.append("> **Articuno** `WON`!")

                await res.ctx.edit_origin(
                    content="".join(content),
                    components=rps_selection,
                    allowed_mentions={"parse": []},
                )
                break

            except asyncio.TimeoutError:
                rps_selection.disabled = True
                try:
                    return await msg.edit(
                        content="Time's up!", components=rps_selection
                    )
                except interactions.client.errors.NotFound:
                    return

    @hybrid_slash_subcommand(
        base="rock_paper_scissors",
        base_description="Play a game of Rock-Paper-Scissors.",
        name="human",
        description="Play against someone else.",
    )
    @interactions.slash_option(
        opt_type=interactions.OptionType.USER,
        name="user",
        description="The user to play against",
        required=True,
    )
    async def human(self, ctx: HybridContext, user: interactions.User) -> None:
        """Play against someone else."""

        if int(ctx.user.id) == int(user.id):
            return await ctx.send(
                "You cannot challenge yourself.", ephemeral=True
            )

        if int(user.id) == int(self.client.user.id):
            return await ctx.send(
                "To challenge me, do ``/rock_paper_scissors ai`` instead.",
                ephemeral=True,
            )

        rps_selection.disabled = False

        accept_deny = [
            interactions.ActionRow(
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
            )
        ]

        msg = await ctx.send(
            content=f"{ctx.user.mention} challenged {user.mention}.",
            components=accept_deny,
            allowed_mentions={"users": [int(user.id)]},
        )

        while True:
            try:
                op = await self.client.wait_for_component(
                    components=accept_deny,
                    messages=int(msg.id),
                    timeout=15,
                )

                if int(op.ctx.user.id) == int(user.id):
                    if op.ctx.custom_id == "accept":
                        _msg = await op.ctx.edit_origin(
                            content=f"{ctx.user.mention} vs {user.mention}",
                            components=rps_selection,
                        )
                        user1 = int(ctx.user.id)
                        user2 = int(user.id)
                        cmp_1 = 0

                        while True:
                            cmp1 = await self.client.wait_for_component(
                                components=rps_selection,
                                messages=int(msg.id),
                                timeout=15,
                            )

                            if (
                                int(cmp1.ctx.user.id) == user1
                                or int(cmp1.ctx.user.id) == user2
                            ):
                                cmp_1 = int(cmp1.ctx.user.id)
                                await cmp1.ctx.edit_origin(
                                    content=f"{_msg.content}\n\n{cmp1.ctx.user.mention} has their option chosen."
                                )
                                choice1 = int(cmp1.ctx.values[0])
                                break

                            else:
                                pass

                        while True:
                            cmp2 = await self.client.wait_for_component(
                                components=rps_selection,
                                messages=int(msg.id),
                                timeout=15,
                            )

                            if int(cmp2.ctx.user.id) in {
                                int(user1),
                                int(user2),
                            } and int(cmp2.ctx.user.id) != int(cmp_1):
                                rps_selection.disabled = True
                                choice2 = int(cmp2.ctx.values[0])
                                break

                            else:
                                pass

                        result = rps_get_winner(choice1, choice2)
                        content: list[str] = [
                            f"{ctx.user.mention} chose ",
                            f"**{self.choice_convert[choice1]}**.\n",
                            f"{user.mention} chose ",
                            f"**{self.choice_convert[choice2]}**.\n",
                        ]
                        allowed_mentions = {}

                        if result is None:
                            content.append("> It is a tie!")
                            allowed_mentions["users"] = []
                        elif result is True:
                            content.append(f"> {ctx.user.mention} won!")
                            allowed_mentions["users"] = [int(ctx.user.id)]
                        elif result is False:
                            content.append(f"> {user.mention} won!")
                            allowed_mentions["users"] = [int(user.id)]

                        await cmp2.ctx.edit_origin(
                            content="".join(content),
                            components=rps_selection,
                            allowed_mentions=allowed_mentions,
                        )
                        break

                    elif op.ctx.custom_id == "deny":
                        await msg.edit(
                            content=f"{user.mention} declined the challenge.",
                            components=[],
                            allowed_mentions={"users": []},
                        )

                        break

                elif (
                    int(op.ctx.user.id) != int(user.id)
                    and int(op.ctx.user.id) == int(ctx.user.id)
                    and op.ctx.custom_id == "deny"
                ):
                    await op.ctx.edit_origin(
                        content=f"{ctx.user.mention} cancelled the challenge.",
                        components=[],
                    )
                    break

                elif (
                    int(op.ctx.user.id) != int(user.id)
                    and int(op.ctx.user.id) == int(ctx.user.id)
                    and op.ctx.custom_id == "accept"
                ):
                    await op.ctx.send(
                        content="You cannot accept the challenge by yourself.",
                        components=[],
                        ephemeral=True,
                    )

                else:
                    pass

            except asyncio.TimeoutError:
                try:
                    return await msg.edit(content="Time's up!", components=[])
                except interactions.client.errors.NotFound:
                    return


def setup(client) -> None:
    """Setup the extension."""
    RPS(client)
    logging.info("Loaded RPS extension.")
