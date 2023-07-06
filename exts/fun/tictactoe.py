import logging
import asyncio
import enum
import random
import copy
import math
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_subcommand,
    HybridContext,
)


class GameState(enum.IntEnum):
    empty = 0
    player = -1
    ai = +1


def render_board(board: list, disable=False) -> list:
    """
    Converts the test_board into a visual representation using discord components
    :param board: The game test_board
    :param disable: Disable the buttons on the test_board
    :return: List[action-rows]
    """

    buttons = []
    for i in range(3):
        for x in range(3):
            if board[i][x] == GameState.empty:
                style = interactions.ButtonStyle.GRAY
            elif board[i][x] == GameState.player:
                style = interactions.ButtonStyle.PRIMARY
            else:
                style = interactions.ButtonStyle.RED
            buttons.append(
                interactions.Button(
                    style=style,
                    label="‎",
                    custom_id=f"tic_tac_toe_button||{i},{x}",
                    disabled=disable,
                )
            )
    return interactions.spread_to_rows(*buttons, max_in_row=3)


def board_state(components: list) -> list[list]:
    """
    Extrapolate the current state of the game based on the components of a message
    :param components: The components object from a message
    :return: The test_board state
    :rtype: list[list]
    """

    board = copy.deepcopy(BoardTemplate)
    for i in range(3):
        for x in range(3):
            button = components[i].components[x]
            if button.style == 2:
                board[i][x] = GameState.empty
            elif button.style == 1:
                board[i][x] = GameState.player
            elif button.style == 4:
                board[i][x] = GameState.ai
    return board


def win_state(board: list, player: GameState) -> bool:
    """
    Determines if the specified player has won
    :param board: The game test_board
    :param player: The player to check for
    :return: bool, have they won
    """
    win_states = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    if [player, player, player] in win_states:
        return True
    return False


def get_possible_positions(board: list) -> list[list[int]]:
    """
    Determines all the possible positions in the current game state
    :param board: The game test_board
    :return: A list of possible positions
    """

    possible_positions = []
    for i in range(3):
        for x in range(3):
            if board[i][x] == GameState.empty:
                possible_positions.append([i, x])
    return possible_positions


def evaluate(board):
    if win_state(board, GameState.ai):
        score = +1
    elif win_state(board, GameState.player):
        score = -1
    else:
        score = 0
    return score


def min_max(test_board: list, depth: int, player: GameState):
    if player == GameState.ai:
        best = [-1, -1, -math.inf]
    else:
        best = [-1, -1, +math.inf]

    if (
        depth == 0
        or win_state(test_board, GameState.player)
        or win_state(test_board, GameState.ai)
    ):
        score = evaluate(test_board)
        return [-1, -1, score]

    for cell in get_possible_positions(test_board):
        x, y = cell[0], cell[1]
        test_board[x][y] = player
        score = min_max(test_board, depth - 1, -player)
        test_board[x][y] = GameState.empty
        score[0], score[1] = x, y

        if player == GameState.ai:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score
    return best


BoardTemplate = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


class TicTacToe(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @hybrid_slash_subcommand(
        base="tictactoe",
        base_description="TicTacToe command.",
        aliases=["ttt", "tic", "tac", "toe"],
        name="easy",
        description="Play TicTacToe in easy mode.",
    )
    async def ttt_easy(self, ctx: HybridContext) -> None:
        """Play TicTacToe in easy mode."""

        await ctx.send(
            content=f"{ctx.author.mention}'s tic tac toe game (easy mode)",
            components=render_board(copy.deepcopy(BoardTemplate)),
        )

    @hybrid_slash_subcommand(
        base="tictactoe",
        base_description="TicTacToe command.",
        name="hard",
        description="Play TicTacToe in hard mode.",
    )
    async def ttt_hard(self, ctx: HybridContext) -> None:
        """Play TicTacToe in hard mode."""

        await ctx.send(
            content=f"{ctx.author.mention}'s tic tac toe game (hard mode)",
            components=render_board(copy.deepcopy(BoardTemplate)),
        )

    @interactions.component_callback(
        interactions.get_components_ids(
            render_board(board=copy.deepcopy(BoardTemplate))
        )
    )
    async def process_turn(self, ctx: interactions.ComponentContext) -> None:
        await ctx.defer(edit_origin=True)
        try:
            async for user in ctx.message.mention_users:
                if ctx.author.id != user.id:
                    return
        except Exception as ex:
            print(ex)
            breakpoint()
            return

        button_pos = (ctx.custom_id.split("||")[-1]).split(",")
        button_pos = [int(button_pos[0]), int(button_pos[1])]
        components = ctx.message.components

        board = board_state(components)

        # Easy mode
        # Articuno will get all possible moves, and use the random
        # module to get a position.
        if ctx.message.content.find("easy mode") != -1:
            print("Easy")
            if board[button_pos[0]][button_pos[1]] == GameState.empty:
                board[button_pos[0]][button_pos[1]] = GameState.player
                if not win_state(board, GameState.player):
                    if len(get_possible_positions(board)) != 0:
                        ai_pos = random.choice(get_possible_positions(board))
                        x, y = ai_pos[0], ai_pos[1]
                        board[x][y] = GameState.ai
            else:
                return

        # Hard mode
        # Articuno will use minimax to make sure that the game will
        # never be a win for the player.
        elif ctx.message.content.find("hard mode") != -1:
            print("Hard")
            if board[button_pos[0]][button_pos[1]] == GameState.empty:
                board[button_pos[0]][button_pos[1]] = GameState.player
                if not win_state(board, GameState.player):
                    possible_positions = get_possible_positions(board)
                    # ai pos
                    if len(possible_positions) != 0:
                        depth = len(possible_positions)

                        move = await asyncio.to_thread(
                            min_max,
                            copy.deepcopy(board),
                            min(random.choice([4, 6]), depth),
                            GameState.ai,
                        )
                        x, y = move[0], move[1]
                        board[x][y] = GameState.ai
            else:
                return

        if win_state(board, GameState.player):
            winner = ctx.author.mention
        elif win_state(board, GameState.ai):
            winner = self.bot.user.mention
        elif len(get_possible_positions(board)) == 0:
            winner = "Nobody"
        else:
            winner = None

        content = f"{ctx.author.mention}'s tic tac toe game " + (
            "(easy mode)"
            if ctx.message.content.find("easy mode") != -1
            else "(hard mode)"
        )

        await ctx.edit_origin(
            content=content
            if not winner
            else f"{winner} has won! "
            + (
                "(easy mode)"
                if ctx.message.content.find("easy mode") != -1
                else "(hard mode)"
            ),
            components=render_board(board, disable=winner is not None),
        )


def setup(client) -> None:
    """Setup the extension."""
    TicTacToe(client)
    logging.info("Loaded TicTacToe extension.")
