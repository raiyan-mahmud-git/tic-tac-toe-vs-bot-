# Tic-Tac-Toe with Depth-Aware Minimax AI

An enhanced, modular Python Tic-Tac-Toe application with a Tkinter graphical interface, depth-weighted Minimax AI, race-condition safe event handling, and a full automated test suite.

---

## Features

- **Decoupled Architecture**: Pure Python game engine (`game_logic.py`) completely separated from the UI and AI solver, making it easily testable and extensible.
- **Depth-Aware Minimax AI**:
  - Scores earlier wins higher (`10 - depth`) and delays defeat (`depth - 10`).
  - Guarantees the AI takes the fastest path to victory.
- **Multiple Difficulty Modes**:
  - `Unbeatable`: Mathematically perfect Minimax.
  - `Medium`: Takes immediate wins and blocks opponent wins, mixing optimal play with occasional casual moves.
  - `Easy`: Random moves for beginner players.
- **Concurrency & Race-Condition Safe**:
  - Prevents rapid double-clicks while the AI is "thinking".
  - Explicitly cancels scheduled `root.after` callbacks upon game reset, preventing ghost moves on fresh boards.
- **Automatic Round Restart & Persistent Scoreboard**:
  - Automatically resets the board 1.5 seconds after any game conclusion (win, loss, or draw) so you can smoothly start the next round without manual clicks.
  - Scores (Player X, AI O, Draws) stay completely intact across auto-restarts until you choose to click "Reset Scores".
  - Manual "Restart Game" remains available at any time.

---

## Project Structure

```
tic_tac_toe/
├── game_logic.py     # Core game state, rules, move validation, and win/draw detection
├── ai.py             # Minimax algorithm with depth penalty and difficulty heuristics
├── gui.py            # Tkinter interface with race-condition guards and score tracking
├── main.py           # Main application entry point
├── test_game.py      # Unit tests for game rules, winning lines, draws, and AI decisions
├── test_gui.py       # Integration tests for Tkinter GUI, widget states, and event handling
└── README.md         # Documentation and run instructions
```

---

## Running the Game

Ensure Python 3.8+ is installed with Tkinter support (standard in official Python distributions).

### Launch the Application

From the project directory, run:

```bash
python main.py
```

Or run the GUI module directly:

```bash
python gui.py
```

---

## Running Automated Tests

The test suite uses Python's built-in `unittest` framework with no external dependencies required.

### Run All Tests (Unit + Integration)

```bash
python -m unittest discover -v
```

### Run Game Logic and AI Tests

```bash
python -m unittest test_game.py -v
```

### Run GUI Integration Tests

```bash
python -m unittest test_gui.py -v
```

---

## Test Coverage Summary

The automated test suite tests:
1. **Initial State**: Empty 3x3 board, Player X active, no winner, flags cleared.
2. **Turn Transitions**: Proper switching between X and O after valid moves.
3. **Move Validation**: Rejection of occupied cell selections and out-of-bounds indices (`ValueError`).
4. **Game Over Enforcement**: Preventing moves once a terminal state is reached.
5. **Winning Combinations**: Exhaustive testing of all 8 winning lines for both Player X and Player O (3 horizontal rows, 3 vertical columns, 2 diagonals).
6. **Draw Handling**: Verification of 9-cell full-board draws without false positive winners.
7. **Reset Integrity**: Clean restoration of all state attributes upon restart.
8. **AI Immediate Win**: AI taking the winning cell in 1 move.
9. **AI Threat Blocking**: AI prioritizing blocking opponent 2-in-a-row lines.
10. **Minimax Optimality**: AI never losing in simulations against random players, and self-play between two minimax agents always producing a draw.
11. **GUI Concurrency**: Blocking rapid multi-clicks while the AI delay is active, and canceling pending callbacks on reset.
