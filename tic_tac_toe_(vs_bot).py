import tkinter as tk

# Initialize window
root = tk.Tk()
root.title("Tic Tac Toe (AI)")

board = [""] * 9
buttons = []
game_over = False


def check_winner(player):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(all(board[i] == player for i in w) for w in wins)


def is_draw():
    return all(cell != "" for cell in board)


def minimax(is_maximizing):
    if check_winner("O"):
        return 1
    if check_winner("X"):
        return -1
    if is_draw():
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(False)
                board[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(True)
                board[i] = ""
                best_score = min(score, best_score)
        return best_score


def best_move():
    best_score = -float("inf")
    move = None

    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i

    return move


def disable_buttons():
    for b in buttons:
        b.config(state="disabled")


def ai_turn():
    global game_over

    move = best_move()
    if move is not None:
        board[move] = "O"
        buttons[move].config(text="O")

    if check_winner("O"):
        status.config(text="AI wins!")
        game_over = True
        disable_buttons()
        return

    if is_draw():
        status.config(text="Draw!")
        game_over = True
        return

    status.config(text="Your turn (X)")


def on_click(i):
    global game_over

    if board[i] == "" and not game_over:
        board[i] = "X"
        buttons[i].config(text="X")

        if check_winner("X"):
            status.config(text="You win!")
            game_over = True
            disable_buttons()
            return

        if is_draw():
            status.config(text="Draw!")
            game_over = True
            return

        status.config(text="AI thinking...")
        root.after(300, ai_turn)  # small delay for realism


def reset_game():
    global board, game_over
    board = [""] * 9
    game_over = False

    for b in buttons:
        b.config(text="", state="normal")

    status.config(text="Your turn (X)")


# Create buttons
for i in range(9):
    btn = tk.Button(root, text="", width=10, height=3,
                    font=("Arial", 16),
                    command=lambda i=i: on_click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

# Status label
status = tk.Label(root, text="Your turn (X)", font=("Arial", 12))
status.grid(row=3, column=0, columnspan=3)

# Reset button
reset_btn = tk.Button(root, text="Restart", command=reset_game)
reset_btn.grid(row=4, column=0, columnspan=3)

root.mainloop()