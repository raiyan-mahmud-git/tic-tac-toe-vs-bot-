"""
Pure Python Tic-Tac-Toe Game Engine.

This module encapsulates all game rules, board representations, move validation,
and win/draw detection completely independent of any graphical or user interface.
"""

from typing import List, Optional, Tuple

EMPTY = ""
PLAYER_X = "X"
PLAYER_O = "O"

# Canonical winning combinations across rows, columns, and diagonals (0-indexed).
WINNING_COMBINATIONS: Tuple[Tuple[int, int, int], ...] = (
    (0, 1, 2),  # Top row
    (3, 4, 5),  # Middle row
    (6, 7, 8),  # Bottom row
    (0, 3, 6),  # Left column
    (1, 4, 7),  # Middle column
    (2, 5, 8),  # Right column
    (0, 4, 8),  # Main diagonal
    (2, 4, 6),  # Anti-diagonal
)


class TicTacToeGame:
    """Manages the state and rules for a standard 3x3 Tic-Tac-Toe game."""

    def __init__(self) -> None:
        self.board: List[str] = [EMPTY] * 9
        self.current_player: str = PLAYER_X
        self.winner: Optional[str] = None
        self.winning_line: Optional[Tuple[int, int, int]] = None
        self.is_draw: bool = False
        self.game_over: bool = False

    def reset(self) -> None:
        """Reset the game state to an empty board with Player X to move."""
        self.board = [EMPTY] * 9
        self.current_player = PLAYER_X
        self.winner = None
        self.winning_line = None
        self.is_draw = False
        self.game_over = False

    def is_valid_move(self, index: int) -> bool:
        """Return True if the specified index is currently a legal move."""
        if not (0 <= index < 9):
            return False
        if self.game_over:
            return False
        return self.board[index] == EMPTY

    def make_move(self, index: int) -> bool:
        """
        Execute a move at the given index for the current player.

        Raises:
            ValueError: If the index is out of range, the cell is occupied,
                        or the game is already over.

        Returns:
            bool: True when the move is successfully executed.
        """
        if not (0 <= index < 9):
            raise ValueError(f"Move index {index} is out of bounds (must be 0-8).")
        if self.game_over:
            raise ValueError("Cannot make a move; the game has already concluded.")
        if self.board[index] != EMPTY:
            raise ValueError(f"Cell {index} is already occupied by '{self.board[index]}'.")

        self.board[index] = self.current_player
        self._evaluate_game_state()

        if not self.game_over:
            self._switch_turn()

        return True

    def _switch_turn(self) -> None:
        """Switch the active player between X and O."""
        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X

    def _evaluate_game_state(self) -> None:
        """Check for winning lines or a draw condition."""
        for combo in WINNING_COMBINATIONS:
            a, b, c = combo
            if self.board[a] != EMPTY and self.board[a] == self.board[b] == self.board[c]:
                self.winner = self.board[a]
                self.winning_line = combo
                self.game_over = True
                return

        if all(cell != EMPTY for cell in self.board):
            self.is_draw = True
            self.game_over = True
            self.winner = None
            self.winning_line = None

    def get_available_moves(self) -> List[int]:
        """Return a list of integer indices for unoccupied cells."""
        if self.game_over:
            return []
        return [i for i, cell in enumerate(self.board) if cell == EMPTY]

    def clone(self) -> "TicTacToeGame":
        """Create a deep independent copy of the current game state."""
        cloned = TicTacToeGame()
        cloned.board = list(self.board)
        cloned.current_player = self.current_player
        cloned.winner = self.winner
        cloned.winning_line = self.winning_line
        cloned.is_draw = self.is_draw
        cloned.game_over = self.game_over
        return cloned
