# Tic Tac Toe (GUI + AI) in Python

## Overview
This project is a Tic Tac Toe game built using Python with a graphical user interface (GUI) and an unbeatable AI opponent. The GUI is created using Tkinter, and the AI uses the Minimax algorithm, a classic decision-making algorithm in game theory.

The player plays as "X" and the AI plays as "O".


## Features
- Interactive GUI using Tkinter
- Unbeatable AI (Minimax algorithm)
- Real-time game status updates
- Restart button to reset the game
- Clean and simple interface


## How It Works
The game board is represented as a list of 9 elements. Each button in the GUI corresponds to a position on the board.

When the player clicks a button:
1. The player's move ("X") is placed.
2. The game checks if the player has won or if it's a draw.
3. If the game continues, the AI calculates the best move using Minimax.
4. The AI places its move ("O").
5. The game checks again for a win or draw.

The Minimax algorithm evaluates all possible future game states and always chooses the optimal move, making the AI impossible to beat.


## Requirements
- Python 3.x
- Tkinter (comes pre-installed with most Python distributions)


## How to Run
1. Download or copy the Python file.
2. Open the file in VS Code or any Python IDE.
3. Run the script using:

   python tic_tac_toe_ai_gui.py


## File Structure
- tic_tac_toe_vs_bot.py  -> Main game file


## Controls
- Click any empty cell to place your move (X)
- The AI will automatically respond
- Click "Restart" to start a new game


## Future Improvements
- Add difficulty levels (Easy, Medium, Hard)
- Add score tracking system
- Improve UI design (colors, animations)
- Convert into a web application using Flask or Django
- Deploy online for public access


## Learning Outcomes
This project demonstrates:
- Python fundamentals
- GUI programming with Tkinter
- Game logic implementation
- Recursion and algorithm design (Minimax)
- Event-driven programming


## License
This project is open-source and free to use for learning purposes.
