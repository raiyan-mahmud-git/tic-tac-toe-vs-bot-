"""
Integration tests for TicTacToeGUI.
"""

import unittest
import tkinter as tk
from gui import TicTacToeGUI
from game_logic import PLAYER_O, PLAYER_X


class TestTicTacToeGUI(unittest.TestCase):
    """Test GUI interactions, widget states, and race condition prevention."""

    def setUp(self) -> None:
        self.root = tk.Tk()
        # Withdraw the window so it doesn't pop up during automated tests
        self.root.withdraw()
        self.app = TicTacToeGUI(root=self.root)

    def tearDown(self) -> None:
        # Clean up scheduled timers and destroy window
        if self.app._pending_ai_after_id:
            self.root.after_cancel(self.app._pending_ai_after_id)
        if self.app._pending_restart_after_id:
            self.root.after_cancel(self.app._pending_restart_after_id)
        self.root.destroy()

    def test_ui_initialization(self) -> None:
        """Verify 9 buttons are created in normal state."""
        self.assertEqual(len(self.app.buttons), 9)
        for btn in self.app.buttons:
            self.assertEqual(btn.cget("text"), "")
            self.assertEqual(btn.cget("state"), "normal")
        self.assertEqual(self.app.scores[PLAYER_X], 0)
        self.assertEqual(self.app.scores[PLAYER_O], 0)
        self.assertEqual(self.app.scores["draws"], 0)

    def test_cell_click_updates_button_and_sets_thinking(self) -> None:
        """Clicking cell 0 should place X, disable button, and set thinking flag."""
        self.app.on_cell_clicked(0)
        self.assertEqual(self.app.buttons[0].cget("text"), "X")
        self.assertEqual(self.app.buttons[0].cget("state"), "disabled")
        self.assertTrue(self.app.is_ai_thinking)
        self.assertIsNotNone(self.app._pending_ai_after_id)

    def test_double_click_race_condition_blocked(self) -> None:
        """Clicking another cell while AI is thinking must be ignored."""
        self.app.on_cell_clicked(0)
        # Attempt second click while thinking is True
        self.app.on_cell_clicked(1)
        # Cell 1 must remain empty
        self.assertEqual(self.app.buttons[1].cget("text"), "")
        self.assertEqual(self.app.buttons[1].cget("state"), "normal")

    def test_reset_cancels_pending_ai_turn(self) -> None:
        """Resetting during AI thinking should cancel the pending after callback."""
        self.app.on_cell_clicked(0)
        self.assertIsNotNone(self.app._pending_ai_after_id)

        self.app.reset_game()
        self.assertIsNone(self.app._pending_ai_after_id)
        self.assertFalse(self.app.is_ai_thinking)
        self.assertEqual(self.app.buttons[0].cget("text"), "")
        self.assertEqual(self.app.buttons[0].cget("state"), "normal")

    def test_ai_execution(self) -> None:
        """Simulate execution of AI turn."""
        self.app.on_cell_clicked(0)
        # Manually trigger the scheduled AI callback
        self.app._execute_ai_turn()

        # An 'O' should have been placed on the board
        o_count = sum(1 for btn in self.app.buttons if btn.cget("text") == "O")
        self.assertEqual(o_count, 1)
        self.assertFalse(self.app.is_ai_thinking)

    def test_auto_restart_scheduled_on_game_conclusion_and_preserves_scores(self) -> None:
        """Game conclusion schedules auto-restart and preserves cumulative scores."""
        # Force a winning condition for Player X (cells 0, 1, 2)
        self.app.game.board = ["X", "X", "", "O", "O", "", "", "", ""]
        self.app.on_cell_clicked(2)  # Winning move for X

        self.assertTrue(self.app.game.game_over)
        self.assertEqual(self.app.scores[PLAYER_X], 1)
        self.assertIsNotNone(self.app._pending_restart_after_id)

        # Trigger the scheduled reset
        self.app.reset_game()

        # Board is cleared, but score remains 1
        self.assertEqual(self.app.scores[PLAYER_X], 1)
        self.assertEqual(self.app.buttons[0].cget("text"), "")
        self.assertEqual(self.app.buttons[0].cget("state"), "normal")
        self.assertFalse(self.app.game.game_over)

    def test_reset_scores_clears_scoreboard(self) -> None:
        """Reset Scores button resets tallies to 0."""
        self.app.scores[PLAYER_X] = 3
        self.app.scores[PLAYER_O] = 2
        self.app.scores["draws"] = 1
        self.app.reset_scores()

        self.assertEqual(self.app.scores[PLAYER_X], 0)
        self.assertEqual(self.app.scores[PLAYER_O], 0)
        self.assertEqual(self.app.scores["draws"], 0)


if __name__ == "__main__":
    unittest.main()
