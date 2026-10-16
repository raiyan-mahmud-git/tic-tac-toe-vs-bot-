"""
Main entry point for the Tic-Tac-Toe application.
"""

from gui import TicTacToeGUI


def main() -> None:
    app = TicTacToeGUI()
    app.run()


if __name__ == "__main__":
    main()
