"""
Tkinter Graphical User Interface for Tic-Tac-Toe.

Features:
- Decoupled architecture communicating with pure Python game engine and AI solver.
- Race-condition safe AI turn scheduling with explicit cancellation on reset.
- Visual highlight of the winning 3-cell combination.
- Scoreboard tracking Human wins, AI wins, and Draws.
- Selectable AI difficulty levels (Unbeatable, Medium, Easy).
- Polished styling with distinct colors for X and O.
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Optional

from game_logic import EMPTY, PLAYER_O, PLAYER_X, TicTacToeGame
from ai import get_ai_move

# UI Timing and Color Palette Constants
AI_DELAY_MS = 300
AUTO_RESTART_DELAY_MS = 1500
COLOR_X = "#1565C0"           # Strong Blue
COLOR_O = "#C62828"           # Strong Red
COLOR_WIN_BG = "#C8E6C9"      # Soft Green highlight for winning line
COLOR_DEFAULT_BG = "#F5F5F5"  # Default button background
COLOR_BOARD_BG = "#B0BEC5"    # Grid border background
COLOR_TEXT_MAIN = "#212121"   # Primary text color
COLOR_TEXT_MUTED = "#757575"  # Muted text for thinking state
COLOR_TEXT_SUBTLE = "#333333" # Score text color
COLOR_WIN_TEXT = "#2E7D32"    # Win banner color
COLOR_DRAW_TEXT = "#E65100"   # Draw banner color

FONT_BUTTON = ("Arial", 22, "bold")
FONT_STATUS = ("Arial", 13, "bold")
FONT_SCORE = ("Arial", 11)


class TicTacToeGUI:
    """Manages the graphical interface and user interactions for Tic-Tac-Toe."""

    def __init__(self, root: Optional[tk.Tk] = None) -> None:
        if root is None:
            self.root = tk.Tk()
            self._owns_root = True
        else:
            self.root = root
            self._owns_root = False

        self.root.title("Tic Tac Toe (AI)")
        self.root.resizable(False, False)

        # Core Engine and State
        self.game = TicTacToeGame()
        self.is_ai_thinking: bool = False
        self._pending_ai_after_id: Optional[str] = None
        self._pending_restart_after_id: Optional[str] = None

        # Scores
        self.scores = {PLAYER_X: 0, PLAYER_O: 0, "draws": 0}

        # Difficulty setting
        self.difficulty_var = tk.StringVar(value="unbeatable")

        # Widget storage
        self.buttons: List[tk.Button] = []
        self.score_label: tk.Label
        self.status_label: tk.Label

        self._build_ui()

    def _build_ui(self) -> None:
        """Create and lay out all window components."""
        self._build_scoreboard()
        self._build_difficulty_selector()
        self._build_board_grid()
        self._build_status_and_actions()

    def _build_scoreboard(self) -> None:
        """Create header displaying current win/loss/draw record."""
        score_frame = tk.Frame(self.root, pady=8, padx=10)
        score_frame.pack(fill=tk.X)

        self.score_label = tk.Label(
            score_frame,
            text=self._get_score_text(),
            font=FONT_SCORE,
            fg=COLOR_TEXT_SUBTLE,
        )
        self.score_label.pack()

    def _build_difficulty_selector(self) -> None:
        """Create combobox for difficulty selection."""
        diff_frame = tk.Frame(self.root, pady=4)
        diff_frame.pack()

        tk.Label(diff_frame, text="Difficulty: ", font=("Arial", 10)).pack(side=tk.LEFT)
        diff_combo = ttk.Combobox(
            diff_frame,
            textvariable=self.difficulty_var,
            values=["unbeatable", "medium", "easy"],
            state="readonly",
            width=12,
        )
        diff_combo.pack(side=tk.LEFT)
        diff_combo.bind("<<ComboboxSelected>>", lambda e: self.reset_game())

    def _build_board_grid(self) -> None:
        """Create 3x3 grid of interactive game buttons."""
        board_frame = tk.Frame(self.root, padx=12, pady=8, bg=COLOR_BOARD_BG)
        board_frame.pack()

        for i in range(9):
            btn = tk.Button(
                board_frame,
                text="",
                width=5,
                height=2,
                font=FONT_BUTTON,
                bg=COLOR_DEFAULT_BG,
                activebackground="#E0E0E0",
                relief=tk.RAISED,
                command=lambda index=i: self.on_cell_clicked(index),
            )
            btn.grid(row=i // 3, column=i % 3, padx=3, pady=3)
            self.buttons.append(btn)

    def _build_status_and_actions(self) -> None:
        """Create status feedback and control buttons."""
        self.status_label = tk.Label(
            self.root,
            text="Your turn (X)",
            font=FONT_STATUS,
            pady=8,
            fg=COLOR_TEXT_MAIN,
        )
        self.status_label.pack()

        action_frame = tk.Frame(self.root, pady=8)
        action_frame.pack()

        restart_btn = tk.Button(
            action_frame,
            text="Restart Game",
            font=("Arial", 11),
            padx=8,
            pady=3,
            command=self.reset_game,
        )
        restart_btn.pack(side=tk.LEFT, padx=6)

        reset_score_btn = tk.Button(
            action_frame,
            text="Reset Scores",
            font=("Arial", 11),
            padx=8,
            pady=3,
            command=self.reset_scores,
        )
        reset_score_btn.pack(side=tk.LEFT, padx=6)

    def _get_score_text(self) -> str:
        return (
            f"You (X): {self.scores[PLAYER_X]}   |   "
            f"AI (O): {self.scores[PLAYER_O]}   |   "
            f"Draws: {self.scores['draws']}"
        )

    def _update_score_display(self) -> None:
        self.score_label.config(text=self._get_score_text())

    def on_cell_clicked(self, index: int) -> None:
        """Handle user clicks on a board cell."""
        if self.is_ai_thinking or not self.game.is_valid_move(index):
            return

        self.game.make_move(index)
        self._update_button_visual(index, PLAYER_X)

        if self.game.game_over:
            self._handle_game_conclusion()
            return

        self.is_ai_thinking = True
        self.status_label.config(text="AI is thinking...", fg=COLOR_TEXT_MUTED)
        self._pending_ai_after_id = self.root.after(AI_DELAY_MS, self._execute_ai_turn)

    def _execute_ai_turn(self) -> None:
        """Run the AI solver and commit the computer's move."""
        self._pending_ai_after_id = None

        if self.game.game_over:
            self.is_ai_thinking = False
            return

        ai_move = get_ai_move(
            self.game,
            difficulty=self.difficulty_var.get(),
            ai_player=PLAYER_O,
        )

        if ai_move is not None and self.game.is_valid_move(ai_move):
            self.game.make_move(ai_move)
            self._update_button_visual(ai_move, PLAYER_O)

        self.is_ai_thinking = False

        if self.game.game_over:
            self._handle_game_conclusion()
        else:
            self.status_label.config(text="Your turn (X)", fg=COLOR_TEXT_MAIN)

    def _update_button_visual(self, index: int, player: str) -> None:
        """Update text and foreground color for a board cell."""
        color = COLOR_X if player == PLAYER_X else COLOR_O
        self.buttons[index].config(
            text=player,
            fg=color,
            state="disabled",
            disabledforeground=color,
        )

    def _handle_game_conclusion(self) -> None:
        """Process win or draw state, highlight winning line, update score, and schedule auto-restart."""
        self._disable_all_buttons()

        if self.game.winner is not None:
            if self.game.winner == PLAYER_X:
                self.status_label.config(text="You win! 🎉 (Auto-restarting...)", fg=COLOR_WIN_TEXT)
                self.scores[PLAYER_X] += 1
            else:
                self.status_label.config(text="AI wins! 🤖 (Auto-restarting...)", fg=COLOR_O)
                self.scores[PLAYER_O] += 1

            if self.game.winning_line:
                for idx in self.game.winning_line:
                    self.buttons[idx].config(bg=COLOR_WIN_BG)

        elif self.game.is_draw:
            self.status_label.config(text="It's a draw! 🤝 (Auto-restarting...)", fg=COLOR_DRAW_TEXT)
            self.scores["draws"] += 1

        self._update_score_display()

        # Schedule automatic restart while keeping cumulative scores intact
        self._pending_restart_after_id = self.root.after(
            AUTO_RESTART_DELAY_MS, self.reset_game
        )

    def _disable_all_buttons(self) -> None:
        """Disable all 9 grid buttons upon game over."""
        for btn in self.buttons:
            btn.config(state="disabled")

    def reset_game(self) -> None:
        """Cancel queued callbacks and reset the board for a fresh game (scores preserved)."""
        if self._pending_restart_after_id is not None:
            self.root.after_cancel(self._pending_restart_after_id)
            self._pending_restart_after_id = None

        if self._pending_ai_after_id is not None:
            self.root.after_cancel(self._pending_ai_after_id)
            self._pending_ai_after_id = None

        self.is_ai_thinking = False
        self.game.reset()

        for btn in self.buttons:
            btn.config(
                text="",
                state="normal",
                bg=COLOR_DEFAULT_BG,
                fg=COLOR_TEXT_MAIN,
            )

        self.status_label.config(text="Your turn (X)", fg=COLOR_TEXT_MAIN)

    def reset_scores(self) -> None:
        """Reset scoreboard tallies to zero."""
        self.scores = {PLAYER_X: 0, PLAYER_O: 0, "draws": 0}
        self._update_score_display()

    def run(self) -> None:
        """Start the Tkinter event loop."""
        self.root.mainloop()
