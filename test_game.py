"""
Unit tests for the Tic-Tac-Toe Game Engine and AI Solver.

Tests all winning combinations, draw conditions, move validations, turn transitions,
reset integrity, and AI optimality.
"""

import unittest
from game_logic import (
    EMPTY,
    PLAYER_O,
    PLAYER_X,
    WINNING_COMBINATIONS,
    TicTacToeGame,
)
from ai import find_best_move, get_ai_move, minimax


class TestTicTacToeGame(unittest.TestCase):
    """Test suite for TicTacToeGame core rules and state management."""

    def setUp(self) -> None:
        self.game = TicTacToeGame()

    def test_initial_state(self) -> None:
        """Verify the board starts empty and Player X is first to move."""
        self.assertEqual(self.game.board, [EMPTY] * 9)
        self.assertEqual(self.game.current_player, PLAYER_X)
        self.assertIsNone(self.game.winner)
        self.assertIsNone(self.game.winning_line)
        self.assertFalse(self.game.is_draw)
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.get_available_moves(), list(range(9)))

    def test_turn_switching(self) -> None:
        """Verify player turns alternate correctly on valid moves."""
        self.assertEqual(self.game.current_player, PLAYER_X)
        self.game.make_move(0)
        self.assertEqual(self.game.current_player, PLAYER_O)
        self.game.make_move(1)
        self.assertEqual(self.game.current_player, PLAYER_X)

    def test_occupied_cell_move_rejected(self) -> None:
        """Verify that playing in an already occupied cell raises ValueError."""
        self.game.make_move(4)
        self.assertFalse(self.game.is_valid_move(4))
        with self.assertRaises(ValueError) as ctx:
            self.game.make_move(4)
        self.assertIn("already occupied", str(ctx.exception))

    def test_out_of_bounds_move_rejected(self) -> None:
        """Verify that indices outside 0-8 are rejected."""
        self.assertFalse(self.game.is_valid_move(-1))
        self.assertFalse(self.game.is_valid_move(9))
        with self.assertRaises(ValueError):
            self.game.make_move(-1)
        with self.assertRaises(ValueError):
            self.game.make_move(9)

    def test_move_after_game_over_rejected(self) -> None:
        """Verify that no moves can be made once a game has ended."""
        # X wins on top row: 0, 1, 2
        # Moves: X:0, O:3, X:1, O:4, X:2 (win)
        moves = [0, 3, 1, 4, 2]
        for m in moves:
            self.game.make_move(m)

        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, PLAYER_X)
        self.assertFalse(self.game.is_valid_move(5))

        with self.assertRaises(ValueError) as ctx:
            self.game.make_move(5)
        self.assertIn("already concluded", str(ctx.exception))

    def test_all_eight_winning_lines_player_x(self) -> None:
        """Test all 8 winning lines for Player X."""
        for combo in WINNING_COMBINATIONS:
            with self.subTest(combo=combo):
                game = TicTacToeGame()
                # Find two non-interfering cells for O
                non_combo = [i for i in range(9) if i not in combo]
                # X moves to combo[0], O moves to non_combo[0]
                game.make_move(combo[0])
                game.make_move(non_combo[0])
                # X moves to combo[1], O moves to non_combo[1]
                game.make_move(combo[1])
                game.make_move(non_combo[1])
                # X moves to combo[2] (winning move)
                game.make_move(combo[2])

                self.assertTrue(game.game_over)
                self.assertEqual(game.winner, PLAYER_X)
                self.assertEqual(game.winning_line, combo)
                self.assertFalse(game.is_draw)

    def test_all_eight_winning_lines_player_o(self) -> None:
        """Test all 8 winning lines for Player O."""
        import itertools

        for combo in WINNING_COMBINATIONS:
            with self.subTest(combo=combo):
                game = TicTacToeGame()
                non_combo = [i for i in range(9) if i not in combo]

                # Select 3 cells for X that do NOT form a winning line
                x_moves = None
                for triplet in itertools.combinations(non_combo, 3):
                    triplet_set = set(triplet)
                    if not any(set(w).issubset(triplet_set) for w in WINNING_COMBINATIONS):
                        x_moves = list(triplet)
                        break

                self.assertIsNotNone(x_moves, f"Could not find non-winning moves for X with combo {combo}")

                # X: x_moves[0], O: combo[0]
                game.make_move(x_moves[0])
                game.make_move(combo[0])
                # X: x_moves[1], O: combo[1]
                game.make_move(x_moves[1])
                game.make_move(combo[1])
                # X: x_moves[2], O: combo[2] (winning move for O)
                game.make_move(x_moves[2])
                game.make_move(combo[2])

                self.assertTrue(game.game_over)
                self.assertEqual(game.winner, PLAYER_O)
                self.assertEqual(game.winning_line, combo)
                self.assertFalse(game.is_draw)

    def test_draw_condition(self) -> None:
        """Verify full board draw without a winner."""
        # Board layout for draw:
        # X O X
        # X O O
        # O X X
        moves = [0, 1, 2, 4, 3, 5, 7, 6, 8]
        for m in moves:
            self.game.make_move(m)

        self.assertTrue(self.game.game_over)
        self.assertTrue(self.game.is_draw)
        self.assertIsNone(self.game.winner)
        self.assertIsNone(self.game.winning_line)
        self.assertEqual(self.game.get_available_moves(), [])

    def test_reset_functionality(self) -> None:
        """Verify reset restores the board, active player, and flags."""
        self.game.make_move(0)
        self.game.make_move(1)
        self.game.make_move(4)
        self.game.reset()

        self.assertEqual(self.game.board, [EMPTY] * 9)
        self.assertEqual(self.game.current_player, PLAYER_X)
        self.assertIsNone(self.game.winner)
        self.assertIsNone(self.game.winning_line)
        self.assertFalse(self.game.is_draw)
        self.assertFalse(self.game.game_over)
        self.assertEqual(len(self.game.get_available_moves()), 9)

    def test_clone_creates_isolated_copy(self) -> None:
        """Verify cloned game does not affect original state upon mutation."""
        self.game.make_move(4)
        cloned = self.game.clone()

        cloned.make_move(0)
        self.assertEqual(cloned.board[0], PLAYER_O)
        self.assertEqual(self.game.board[0], EMPTY)


class TestTicTacToeAI(unittest.TestCase):
    """Test suite for Minimax AI solver and difficulty heuristics."""

    def test_ai_takes_immediate_winning_move(self) -> None:
        """AI (O) must immediately complete a winning line when available."""
        game = TicTacToeGame()
        # O has 0 and 1; cell 2 is winning move
        game.board = [
            PLAYER_O, PLAYER_O, EMPTY,
            PLAYER_X, PLAYER_X, EMPTY,
            EMPTY,    EMPTY,    EMPTY
        ]
        move = find_best_move(game, ai_player=PLAYER_O)
        self.assertEqual(move, 2)

    def test_ai_blocks_immediate_opponent_win(self) -> None:
        """AI (O) must block opponent (X) when opponent has 2 in a row."""
        game = TicTacToeGame()
        # X has 0 and 1; cell 2 must be blocked
        game.board = [
            PLAYER_X, PLAYER_X, EMPTY,
            PLAYER_O, EMPTY,    EMPTY,
            EMPTY,    EMPTY,    EMPTY
        ]
        move = find_best_move(game, ai_player=PLAYER_O)
        self.assertEqual(move, 2)

    def test_depth_preference_faster_win(self) -> None:
        """Minimax must choose the 1-move win over a 2-move win."""
        game = TicTacToeGame()
        # O can win immediately at index 2
        game.board = [
            PLAYER_O, PLAYER_O, EMPTY,
            PLAYER_X, PLAYER_X, EMPTY,
            PLAYER_X, EMPTY,    PLAYER_O
        ]
        move = find_best_move(game, ai_player=PLAYER_O)
        self.assertEqual(move, 2)

    def test_ai_never_loses_against_random_player(self) -> None:
        """Simulate 20 games of AI (O) vs random moves (X); AI must never lose."""
        import random
        random.seed(42)

        for _ in range(20):
            game = TicTacToeGame()
            while not game.game_over:
                if game.current_player == PLAYER_X:
                    avail = game.get_available_moves()
                    game.make_move(random.choice(avail))
                else:
                    ai_move = find_best_move(game, ai_player=PLAYER_O)
                    self.assertIsNotNone(ai_move)
                    game.make_move(ai_move)

            self.assertNotEqual(
                game.winner,
                PLAYER_X,
                f"AI lost to random player! Final board: {game.board}",
            )

    def test_ai_self_play_always_draws(self) -> None:
        """Two optimal minimax players must always reach a draw."""
        game = TicTacToeGame()
        while not game.game_over:
            if game.current_player == PLAYER_X:
                move = find_best_move(game, ai_player=PLAYER_X)
            else:
                move = find_best_move(game, ai_player=PLAYER_O)

            self.assertIsNotNone(move)
            game.make_move(move)

        self.assertTrue(game.is_draw)
        self.assertIsNone(game.winner)

    def test_difficulty_modes_return_valid_moves(self) -> None:
        """Ensure all difficulty modes return legal moves on an open board."""
        game = TicTacToeGame()
        game.make_move(0)  # Human move

        for diff in ["easy", "medium", "unbeatable"]:
            move = get_ai_move(game, difficulty=diff, ai_player=PLAYER_O)
            self.assertIn(move, game.get_available_moves())


if __name__ == "__main__":
    unittest.main()
