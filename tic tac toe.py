import pygame
import os
import tkinter as tk
WIDTH = 250
HEIGHT = 200

class TicTacToe:
    def __init__(self, window):
        # initilaizing window properties
        self.window = window
        self.window.title("Tic Tac Toe")
        self.window.geometry(f'{WIDTH}x{HEIGHT}')

        # intitializing game attributes
        self.turn = True # if true, player X's turn, if False, player O's turn
        self.num_plays = 0 # number of turns played in this game
        self.play_matrix = 9*[""]# contains plays on table internally
        self.buttons = [] # list for button objects

        self.add_start_widgets()

    # intializing and packing widgets onto window
    def add_start_widgets(self):
        self.main_frame = tk.Frame(self.window)
        self.lbl_title = tk.Label(master=self.main_frame, text="Welcome to Tic Tac Toe",
                                  font=("Times New Roman", 15, "bold"), pady=50)
        self.btn_start = tk.Button(master=self.main_frame, text="Click here to start", font=("Times New Roman", 15),
                                command=lambda: self.game_window())

        self.main_frame.pack()
        self.lbl_title.pack()
        self.btn_start.pack()

    # removing start widgets, and replacing with game grid
    def game_window(self):
        self.main_frame.destroy()
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack()

        self.construct_grid()

        sub_frame = tk.Frame(master=self.main_frame,relief=tk.SUNKEN, borderwidth=1)
        self.lbl_turn = tk.Label(sub_frame, text="Player X's turn", font=("Times New Roman", 15, "bold"))

        sub_frame.grid(row=3, columnspan=3)
        self.lbl_turn.pack()

    # intializing and packing grid of buttons onto window
    def construct_grid(self):
        for i in range(3):
            for j in range(3):
                sub_frame = tk.Frame(master=self.main_frame, relief=tk.RAISED, borderwidth=1)
                btn = My_Button(sub_frame, self)

                sub_frame.grid(row=i, column=j)
                btn.pack()

                self.buttons.append(btn)

    def check_win(self): # fix me: might be a more efficient algorithm
        if self.num_plays > 4: # of less than 4, theres not enough plays for a win
            win_combos = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
            found_win = False
            for i in range(9):
                if self.play_matrix[i] == '':
                    for tuples in win_combos:
                        if i in tuples:
                            win_combos.remove(tuples)
            i = 0
            while i < len(win_combos) and not(found_win):
                combo = win_combos[i]
                if self.play_matrix[combo[0]] == self.play_matrix[combo[1]] == self.play_matrix[combo[2]]:
                    found_win = True
                    self.buttons[combo[0]].config(bg="green yellow")
                    self.buttons[combo[1]].config(bg="green yellow")
                    self.buttons[combo[2]].config(bg="green yellow")

                    symbol = self.play_matrix[combo[0]]
                    self.lbl_turn.config(text=f"Player {symbol} wins!")
                i += 1

            # fix me: need to have case when theres a tie
            if not(found_win) and self.num_plays == 9:
                self.lbl_turn.config(text="Its a tie!")

class My_Button(tk.Button):
    def __init__(self, master, game):
        super().__init__(master=master,  width=8, height=3, command=lambda: play(game, self))
        self.clickable = True
        self.symbol = ""

def play(game, button):
    if button.clickable:
        if game.turn: # player Xs turn
            button.symbol = "X"
            button.config(text="X")
            game.lbl_turn.config(text="Player O's turn")

        else: # player O's turn
            button.symbol = "O"
            button.config(text="O")
            game.lbl_turn.config(text="Player X's turn")

        game.num_plays += 1
        game.play_matrix[game.buttons.index(button)] = button.symbol
        game.turn = not (game.turn)
        button.clickable = False
        game.check_win()

window = tk.Tk()
run = TicTacToe(window)
window.mainloop()
