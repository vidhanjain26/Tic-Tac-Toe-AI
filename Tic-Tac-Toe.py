import tkinter as tk
from tkinter import messagebox
import random

# Initialize the board
board = [' ' for _ in range(9)]
current_player = 'X'
game_mode = None  # Variable to store the selected game mode: 'ai' or 'manual'

def check_win(player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Vertical
        [0, 4, 8], [2, 4, 6]             # Diagonal
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def check_draw():
    return ' ' not in board

def get_ai_move():
    # AI tries to win
    for move in range(9):
        if board[move] == ' ':
            board[move] = 'O'
            if check_win('O'):
                return move
            board[move] = ' '
    
    # AI tries to block the user's win
    for move in range(9):
        if board[move] == ' ':
            board[move] = 'X'
            if check_win('X'):
                board[move] = 'O'
                return move
            board[move] = ' '
    
    # If no win or block, pick a random available spot
    available_moves = [i for i in range(9) if board[i] == ' ']
    return random.choice(available_moves)

def on_button_click(index):
    global current_player

    if board[index] == ' ':
        board[index] = current_player
        buttons[index].config(text=current_player, state=tk.DISABLED)
        
        if check_win(current_player):
            messagebox.showinfo("Tic-Tac-Toe", f"Player {current_player} wins!")
            reset_game()
        elif check_draw():
            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
            reset_game()
        else:
            if game_mode == 'ai':
                current_player = 'O'  # Switch to AI's turn
                ai_move = get_ai_move()
                board[ai_move] = 'O'
                buttons[ai_move].config(text='O', state=tk.DISABLED)
                
                if check_win('O'):
                    messagebox.showinfo("Tic-Tac-Toe", "AI wins!")
                    reset_game()
                elif check_draw():
                    messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                    reset_game()
                else:
                    current_player = 'X'  # Switch back to player's turn
            else:
                current_player = 'O' if current_player == 'X' else 'X'  # Switch turns for manual mode

def reset_game():
    global board, current_player
    board = [' ' for _ in range(9)]
    current_player = 'X'
    for button in buttons:
        button.config(text='', state=tk.NORMAL)

# Function to start AI mode
def start_ai_mode():
    global game_mode
    game_mode = 'ai'
    reset_game()
    messagebox.showinfo("Game Mode", "You are playing against the AI. Click OK to start.")

# Function to start manual mode
def start_manual_mode():
    global game_mode
    game_mode = 'manual'
    reset_game()
    messagebox.showinfo("Game Mode", "You are playing with a friend. Click OK to start.")

# Create the main window
window = tk.Tk()
window.title("Tic-Tac-Toe")
window.configure(bg='lightblue')  # Set background color for the window

# Create a frame for the buttons
frame = tk.Frame(window, bg='lightblue')
frame.pack()

# Create buttons for selecting game mode
ai_mode_button = tk.Button(window, text="Play with AI", width=15, command=start_ai_mode)
ai_mode_button.pack(pady=10)
manual_mode_button = tk.Button(window, text="Play with a Friend", width=15, command=start_manual_mode)
manual_mode_button.pack(pady=10)

# Create buttons for the board (initially hidden until game mode is selected)
buttons = []
for i in range(9):
    button = tk.Button(frame, text='', width=4, height=2, font=('Arial', 20), bg='white', fg='black',
                       activebackground='lightgreen', activeforeground='black',
                       command=lambda i=i: on_button_click(i))
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
    buttons.append(button)
    button.config(state=tk.DISABLED)  # Disable buttons initially

# Function to enable buttons after game mode selection
def enable_buttons():
    for button in buttons:
        button.config(state=tk.NORMAL)

# Start the main event loop
window.mainloop()
