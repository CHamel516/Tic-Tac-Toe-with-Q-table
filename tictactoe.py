import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.resizable(False, False)
        self.initialize_board()
        self.current_player = 'X'
        self.agent = QLearningAgent()
        self.is_game_over = False

    def initialize_board(self):
        self.board = [' ' for _ in range(9)]
        self.buttons = []
        for i in range(3):
            for j in range(3):
                action = lambda x=i, y=j: self.on_click(x, y)
                button = tk.Button(self.window, text=' ', font=('Arial', 20), height=3, width=6, command=action)
                button.grid(row=i, column=j)
                self.buttons.append(button)

    def on_click(self, row, col):
        idx = row * 3 + col
        if self.board[idx] == ' ' and not self.is_game_over:
            self.make_move(idx, 'X')
            self.agent_turn()

    def agent_turn(self):
        if ' ' in self.board and not self.is_game_over:
            state = tuple(self.board)
            action = self.agent.choose_action(state, self.board)
            self.make_move(action, 'O')

    def make_move(self, idx, player):
    # Save the previous state before making a move
        prev_state = tuple(self.board)
        self.board[idx] = player
        self.buttons[idx].config(text=player)
        
        # For agent's move, update the Q-table
        if player == 'O':
            new_state = tuple(self.board)
            reward = 0  # Default reward for non-terminal state
            self.agent.update_q_table(prev_state, idx, reward, new_state, False)
    
        self.check_game_over()

    def check_game_over(self):
        winner = self.agent.check_win(self.board)
        game_over = False
        reward = 0
        if winner:
            messagebox.showinfo("Game Over", f"{winner} wins!")
            reward = 1 if winner == 'O' else -1  # Reward or penalize the agent
            game_over = True
        elif ' ' not in self.board:
            messagebox.showinfo("Game Over", "It's a draw!")
            reward = 0.5  # Neutral reward for a draw
            game_over = True

        if game_over:
        # Update Q-table with terminal reward
            state = tuple(self.board)
            self.agent.update_q_table(state, None, reward, None, True)
            self.ask_replay()


    def ask_replay(self):
        answer = messagebox.askyesno("Game Over", "Do you want to play again?")
        if answer:
            self.reset_board()
        else:
            self.window.destroy()

    def reset_board(self):
        self.initialize_board()
        self.current_player = 'X'
        self.is_game_over = False

class QLearningAgent:
    def __init__(self):
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 0.1

    def choose_action(self, state, board):
        available_actions = [i for i, x in enumerate(board) if x == ' ']
        if np.random.rand() < self.epsilon:
            return random.choice(available_actions)

        q_values = {action: self.q_table.get((state, action), 0) for action in available_actions}
        max_q = max(q_values.values()) if q_values else 0
        max_actions = [action for action, q in q_values.items() if q == max_q]

        return random.choice(max_actions) if max_actions else None

    def check_win(self, board):
        conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for condition in conditions:
            if board[condition[0]] == board[condition[1]] == board[condition[2]] != ' ':
                return board[condition[0]]
        return None
    
    def update_q_table(self, state, action, reward, next_state, game_over):
        if not game_over:
            next_max = max(self.q_table.get((next_state, a), 0) for a in self.available_actions(list(next_state)))
        else:
            next_max = 0  # No next state if the game is over

        old_value = self.q_table.get((state, action), 0)
        new_value = old_value + self.learning_rate * (reward + self.discount_factor * next_max - old_value)
        self.q_table[(state, action)] = new_value


if __name__ == "__main__":
    TicTacToe().window.mainloop()
