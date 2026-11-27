# Tic-Tac-Toe vs. Minimax AI

A Tic-Tac-Toe game with two interfaces: a Python desktop app built with Tkinter and a browser version built with HTML, CSS, and JavaScript. Both versions include three difficulty levels and a depth-aware Minimax opponent.

## Play in a browser

The browser app is in [`docs/`](docs/). It runs entirely in the visitor's browser; it does not need a Python server, database, or other backend.

If GitHub Pages is enabled, play it here:

**[Play Tic-Tac-Toe](https://raiyan-mahmud-git.github.io/tic-tac-toe-vs-bot-/)**

The browser version includes:

- **Unbeatable** — depth-aware Minimax searches the remaining game and plays optimally.
- **Medium** — takes immediate wins and blocks immediate losses, otherwise mixes optimal and random moves.
- **Easy** — chooses a random available square.
- Score tracking, difficulty selection, automatic round restart, and manual controls to start a new round or reset scores.

### Enable or update GitHub Pages

For a GitHub Free account, the repository needs to be public to use Pages. In the repository settings:

1. Open **Settings → Pages**.
2. Under **Build and deployment**, set the source to **Deploy from a branch**.
3. Select branch **`main`** and folder **`/docs`**, then save.
4. GitHub publishes the site at `https://raiyan-mahmud-git.github.io/tic-tac-toe-vs-bot-/`.

Future pushes to `main` update the site. A first deployment or update can take several minutes.

## Run the desktop app

Install Python 3.8 or later with Tkinter support, then run from the project directory:

```bash
python main.py
```

You can also start the interface directly:

```bash
python gui.py
```

## Run the Python tests

The Python test suite uses the standard-library `unittest` framework:

```bash
python -m unittest discover -v
```

Or run one test module:

```bash
python -m unittest test_game.py -v
python -m unittest test_gui.py -v
```

The tests cover game rules, move validation, win and draw detection, resets, AI choices, GUI behavior, and scheduled AI callbacks.

## Project structure

```text
├── ai.py             # Python Minimax AI and difficulty modes
├── game_logic.py     # Python game rules and state
├── gui.py            # Tkinter desktop interface
├── main.py           # Desktop app entry point
├── test_game.py      # Game logic and AI tests
├── test_gui.py       # Tkinter interface tests
├── docs/
│   ├── index.html    # Browser app page
│   ├── styles.css    # Browser app layout and styling
│   └── game.js       # Browser game logic and AI
└── README.md
```
