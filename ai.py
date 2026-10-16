"""
AI Solver for Tic-Tac-Toe.

Implements an unbeatable Minimax algorithm with depth-aware scoring,
ensuring the AI always chooses the fastest path to victory and the longest
defense against defeat. Also provides configurable difficulty modes.
"""

import random
from typing import List, Optional
from game_logic import EMPTY, PLAYER_O, PLAYER_X, TicTacToeGame

CENTER_CELL = 4


def _terminal_score(
    game: TicTacToeGame,
    depth: int,
    ai_player: str,
    human_player: str,
) -> Optional[int]:
    """Return the terminal score if the game has ended, otherwise None."""
    if game.winner == ai_player:
        return 10 - depth
    if game.winner == human_player:
        return depth - 10
    if game.is_draw:
        return 0
    return None


def minimax(
    game: TicTacToeGame,
    depth: int,
    is_maximizing: bool,
    ai_player: str,
    human_player: str,
) -> int:
    """
    Minimax recursive evaluation with depth penalty.

    A win closer to the root earns a higher score; an earlier loss receives
    a steeper penalty.
    """
    terminal = _terminal_score(game, depth, ai_player, human_player)
    if terminal is not None:
        return terminal

    target_player = ai_player if is_maximizing else human_player
    best_score = -float("inf") if is_maximizing else float("inf")

    for move in game.get_available_moves():
        game.board[move] = target_player
        game._evaluate_game_state()

        score = minimax(game, depth + 1, not is_maximizing, ai_player, human_player)

        # Undo move
        game.board[move] = EMPTY
        game.winner = None
        game.winning_line = None
        game.is_draw = False
        game.game_over = False

        if is_maximizing:
            best_score = max(best_score, score)
        else:
            best_score = min(best_score, score)

    return int(best_score)


def find_best_move(game: TicTacToeGame, ai_player: str = PLAYER_O) -> Optional[int]:
    """
    Determine the optimal move using depth-weighted Minimax.
    """
    available_moves = game.get_available_moves()
    if not available_moves:
        return None

    if len(available_moves) == 9:
        return CENTER_CELL

    human_player = PLAYER_X if ai_player == PLAYER_O else PLAYER_O
    best_score = -float("inf")
    best_moves: List[int] = []

    for move in available_moves:
        game.board[move] = ai_player
        game._evaluate_game_state()

        score = minimax(game, 0, False, ai_player, human_player)

        # Undo move
        game.board[move] = EMPTY
        game.winner = None
        game.winning_line = None
        game.is_draw = False
        game.game_over = False

        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    if CENTER_CELL in best_moves:
        return CENTER_CELL

    return random.choice(best_moves)


def _find_immediate_winning_move(game: TicTacToeGame, player: str) -> Optional[int]:
    """Check if placing a piece at any available position completes a win."""
    for move in game.get_available_moves():
        game.board[move] = player
        game._evaluate_game_state()
        has_won = game.winner == player
        # Undo move
        game.board[move] = EMPTY
        game.winner = None
        game.winning_line = None
        game.is_draw = False
        game.game_over = False
        if has_won:
            return move
    return None


def _get_medium_move(
    game: TicTacToeGame,
    available_moves: List[int],
    ai_player: str,
) -> int:
    """Tactical heuristic for medium difficulty."""
    human_player = PLAYER_X if ai_player == PLAYER_O else PLAYER_O

    # 1. Immediate win
    win_move = _find_immediate_winning_move(game, ai_player)
    if win_move is not None:
        return win_move

    # 2. Block opponent's win
    block_move = _find_immediate_winning_move(game, human_player)
    if block_move is not None:
        return block_move

    # 3. Mix optimal play with randomness
    if random.random() < 0.6:
        best = find_best_move(game, ai_player)
        if best is not None:
            return best

    return random.choice(available_moves)


def get_ai_move(
    game: TicTacToeGame,
    difficulty: str = "unbeatable",
    ai_player: str = PLAYER_O,
) -> Optional[int]:
    """
    Get an AI move based on difficulty: 'easy', 'medium', or 'unbeatable'.
    """
    available_moves = game.get_available_moves()
    if not available_moves:
        return None

    mode = difficulty.lower()
    if mode == "easy":
        return random.choice(available_moves)
    if mode == "medium":
        return _get_medium_move(game, available_moves, ai_player)

    return find_best_move(game, ai_player)
