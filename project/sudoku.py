from random import randint
from tkinter import *
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import random
from winsound import *
import pygame
from pygame.mixer import Sound

NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
LETTERS = ['A','B','C','D','E','F','G','H','I']
ITEMS_IN_ROW = 9
N = 9
M = 3
EASY_FIXED_CELLS = 40
MEDIUM_FIXED_CELLS = 32
HARD_FIXED_CELLS = 24


class Box:
    def __init__(self):
        self.isValue = False
        self.value = ''
        self.hasInitVal = False
        self.bckgrnd = "white"


def createGrid(difficulty):
    global grid
    grid = [[Box() for i in range(N)] for j in range(ITEMS_IN_ROW)]
    global board
    board = [[None for a in range(ITEMS_IN_ROW)] for a in range(ITEMS_IN_ROW)]
    search()
    diff = 0
    if (difficulty == "easy"):
        diff = EASY_FIXED_CELLS
    elif (difficulty == "medium"):
        diff = MEDIUM_FIXED_CELLS
    elif ((difficulty == "hard")):
        diff = HARD_FIXED_CELLS
    rows = [0 for i in range(ITEMS_IN_ROW)]
    columns = [0 for i in range(ITEMS_IN_ROW)]
    for i in range(diff):
        while True:
            x = randint(0, 8)
            y = randint(0, 8)
            check = 0
            if (i == diff - 1):
                for j in range(ITEMS_IN_ROW):
                    if (rows[j] == 0 or columns[j] == 0):
                        check = 1
                        break
            if (grid[x][y].isValue == False):
                grid[x][y].isValue = True
                grid[x][y].hasInitVal = True
                grid[x][y].value = board[x][y]
                rows[x] = columns[y] = 1
                break
            if (check == 1):
                break
    if (check == 1):
        createGrid(difficulty)



class ResetDialog(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background="white")
        written = Frame(reset_dialog)
        written.pack(side="top")
        label = tk.Label(written, text="Chcete vymazať zadané polia \n a spustiť hru znovu?", borderwidth=1, height=5,
                         width=40, font=20, background="grey", foreground="white")
        label.grid(row=0, column=0)
        click_frame = Frame(reset_dialog)
        click_frame.pack(side="bottom")
        yb = tk.Button(click_frame, text="ÁNO", width=30, height=2, fg="white", background="green", cursor="plus")
        yb.grid(row=5, column=1)
        yb.config(command=clear_sudoku)
        nb = tk.Button(click_frame, text="NIE", width=30, height=2, background="red")
        nb.grid(row=5, column=15)
        nb.config(command=reset_dialog.destroy)
        reset_dialog.minsize(55, 110)


def show_reset_dialog():
    global reset_dialog
    reset_dialog = tk.Tk()
    reset_dialog.title("ZMAZAŤ POLIA?")
    ResetDialog(reset_dialog).pack(side="top", fill="x")
    reset_dialog.mainloop()


class NewGameDialog(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background="white")
        written = Frame(new_game_dialog)
        written.pack(side="top")
        label = tk.Label(written, text="Chcete začať novú hru?", borderwidth=1, height=5, width=40, font=30,
                         background="grey", foreground="white")
        label.grid(row=0, column=0)
        click_frame = Frame(new_game_dialog)
        click_frame.pack(side="bottom")
        nb = tk.Button(click_frame, text="NIE", width=30, height=2, background="red")
        nb.grid(row=5, column=15)
        nb.config(command=new_game_dialog.destroy)
        yb = tk.Button(click_frame, text="ÁNO", width=30, height=2, fg="white", background="green")
        yb.grid(row=5, column=1)
        yb.config(command=new_game)
        new_game_dialog.minsize(55, 110)


def show_new_game_dialog():
    global new_game_dialog
    new_game_dialog = tk.Tk()
    new_game_dialog.title("NOVÁ HRA?")
    NewGameDialog(new_game_dialog).pack(side="top", fill="x")
    new_game_dialog.mainloop()


def search(c=0):
    i, j = divmod(c, N)
    i0, j0 = i - i % M, j - j % M  # Origin of mxm block
    numbers = list(range(1, N + 1))
    random.shuffle(numbers)
    for x in numbers:
        if (x not in board[i]  # row
                and all(row[j] != x for row in board)  # column
                and all(x not in row[j0:j0 + M]  # block
                        for row in board[i0:i])):
            board[i][j] = x
            if c + 1 >= N ** 2 or search(c + 1):
                return board
    else:
        # No number is valid in this cell: backtrack and try again.
        board[i][j] = None
        return None

    return search()


class MakeGrid(tk.Frame):
    def __init__(self, parent):

        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(ITEMS_IN_ROW):
            label = tk.Label(self, text=row+1,  height=2, width=3, bg="black", fg="white")
            label.config(font=("Cambria", 12))
            label.grid(row=row+1, column=0)
            label2 = tk.Label(self, text=LETTERS[row],  height=2, width=1,  bg="black", fg="white")
            label2.config(font=("Cambria", 12))
            label2.grid(row=0, column=row+1)

        for row in range(ITEMS_IN_ROW):
            current_r = []
            for column in range(ITEMS_IN_ROW):
                if (grid[row][column].hasInitVal == True):
                    label = tk.Label(self, text=grid[row][column].value, borderwidth=0, height=2, width=1, font=20,
                                     background="#ffcccc",  cursor="X_cursor")
                else:
                    validate_command = (
                        self.register(self.validateKey), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W', row, column)
                    label = tk.Entry(self, text=grid[row][column].value, borderwidth=0, width=5, font=70,
                                     background="#C2DFFF",
                                     cursor="plus red red", justify='center', validate="key",
                                     validatecommand=validate_command)

                if (column % 3 == 2 and row % 3 == 2):
                    label.grid(row=row+1, column=column+1, sticky="nsew", padx=(1, 5), pady=(1, 5))
                    current_r.append(label)
                elif (column % 3 == 2):
                    label.grid(row=row+1, column=column+1, sticky="nsew", padx=(1, 5), pady=1)
                    current_r.append(label)
                elif (row % 3 == 2):
                    label.grid(row=row+1, column=column+1, sticky="nsew", padx=1, pady=(1, 5))
                    current_r.append(label)
                else:
                    label.grid(row=row+1, column=column+1, sticky="nsew", padx=1, pady=1)
                    current_r.append(label)

            self._widgets.append(current_r)
        new_game = tk.Button(self, text="NOVÁ HRA", width=20, height=2, relief="ridge", borderwidth=5,  bg='#8FBC8F')
        new_game.grid(row=1, column=10)
        new_game.config(command=show_new_game_dialog)
        reset = tk.Button(self, text="VYMAZAŤ POLIA", width=20, height=2, relief="ridge", borderwidth=5,  bg='#E0FFFF')
        reset.grid(row=2, column=10)
        reset.config(command=show_reset_dialog)
        solve = tk.Button(self, text="ZOBRAZIŤ RIEŠENIE", width=20, height=2, relief="ridge", borderwidth=5,  bg='#E0FFFF')
        solve.grid(row=3, column=10)
        solve.config(command=MakeGrid.ShowCompleted)
        done = tk.Button(self, text="HOTOVO", width=20, height=2, relief="ridge", borderwidth=5,  bg='#8FBC8F')
        done.grid(row=8, column=10)
        done.config(command=submit_pressed)
        exit = tk.Button(self, text="UKONČIŤ", width=20, height=2, relief="ridge", borderwidth=5, bg='#FF6347')
        exit.grid(row=9, column=10)
        exit.config(command=exit_application)

        for column in range(ITEMS_IN_ROW):
            self.grid_columnconfigure(column, weight=1)

    def validateKey(self, d, i, P, s, S, v, V, W, row, column):
        if (int(i) > 0):
            self.bell()
            return False
        if (len(P) == 0):
            grid[int(row)][int(column)].value = ''
            grid[int(row)][int(column)].isValue = False
            return True
        print(S)
        for char in S:
            if (char.isdigit() == False):
                self.bell()
                return False
        inval = int(S)
        if (inval < 1 or inval > 9):
            self.bell()
            return False
        else:
            print(grid[int(row)][int(column)].value)
            grid[int(row)][int(column)].value = inval
            grid[int(row)][int(column)].isValue = True
            return True

    def ShowCompleted():
        for i in range(9):
            for j in range(9):
                grid[i][j].value = board[i][j]
        root2 = tk.Tk()
        root2.title("VYRIEŠENÉ SUDOKU")
        SolvedSudoku(root2).pack(side="top", fill="x")


class SolvedSudoku(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []

        for row in range(9):
            current_row = []
            for column in range(9):
                if (grid[row][column].hasInitVal == True):
                    label = tk.Label(self, text=grid[row][column].value, borderwidth=0, height=2, width=1, font=20,
                                     background="#ffcccc", cursor="X_cursor")
                else:
                    label = tk.Label(self, text=grid[row][column].value, borderwidth=0, width=5, font=20,
                                     background="#C2DFFF",
                                     cursor="X_cursor", justify='center')

                if (column % 3 == 2 and row % 3 == 2):
                    label.grid(row=row, column=column, sticky="nsew", padx=(1, 5), pady=(1, 5))
                    current_row.append(label)
                elif (row % 3 == 2):
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=(1, 5))
                    current_row.append(label)
                elif (column % 3 == 2):
                    label.grid(row=row, column=column, sticky="nsew", padx=(1, 5), pady=1)
                    current_row.append(label)
                else:
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(label)


def clear_sudoku():
    reset_dialog.destroy()
    for i in range(ITEMS_IN_ROW):
        for j in range(ITEMS_IN_ROW):
            if (grid[i][j].hasInitVal == False):
                grid[i][j].value = ''
                grid[i][j].isValue = False
    ROOT.destroy()
    set_environment()


def exit_application():
    ROOT.destroy()


def set_environment():
    global ROOT
    ROOT = tk.Tk()
    ROOT.title("SUDOKU")
    MakeGrid(ROOT).pack(side="top", fill="x")
    ROOT.mainloop()


def show_result(chk1):
    result = tk.Tk()
    result.title("VÝSLEDOK")
    w = Canvas(result, width=400, height=400)
    w.pack()
    if (chk1 == 0):
        information = "GRATULUJEME! "
        x = y = 20 + 4 * 40 + 40 / 2
        w.create_text(x, y, text=information, fill="green", font=("Cambria", 35))
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        pygame.init()
        x = pygame.mixer.Sound('sounds/celebrate.flac')
        x.play(loops=0, maxtime=0, fade_ms=0)
    else:
        information = "NEÚSPEŠNÉ!"
        x = y = 20 + 4 * 40 + 40 / 2
        w.create_text(x, y, text=information, fill="red", font=("Cambria", 35))
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        pygame.init()
        s = pygame.mixer.Sound('sounds/error.wav')
        s.play(loops=0, maxtime=0, fade_ms=0)
    mainloop()


def new_game():
    new_game_dialog.destroy()
    ROOT.destroy()
    for i in range(ITEMS_IN_ROW):
        for j in range(ITEMS_IN_ROW):
            grid[i][j].value = ''
            grid[i][j].isValue = False
            grid[i][j].hasInitVal = False
            grid[i][j].bckgrnd = "grey"
    global ROOT_3
    ROOT_3 = tk.Tk()
    ROOT_3.title("ZVOLTE OBTIAŽNOSŤ")
    easy = tk.Button(ROOT_3, text="ĽAHKÁ", width=15, height=2, bg="Yellow", command=lambda: set_difficulty('easy'))
    easy.grid(row=0, column=3)
    easy.config(font=('helvetica', 25, 'bold italic'))
    medium = tk.Button(ROOT_3, text="STREDNÁ", width=15, height=2, bg="Green", command=lambda: set_difficulty('medium'))
    medium.grid(row=3, column=3)
    medium.config(font=('helvetica', 25, 'bold italic'))
    hard = tk.Button(ROOT_3, text="ŤAŽKÁ", width=15, height=2, bg="Red", command=lambda: set_difficulty('hard'))
    hard.grid(row=6, column=3)
    hard.config(font=('helvetica', 25, 'bold italic'))
    ROOT_3.mainloop()


def submit_pressed():
    x = 0
    y = 0
    for i in range(ITEMS_IN_ROW):
        for j in range(ITEMS_IN_ROW):

            if (grid[i][j].hasInitVal):
                continue
            if (grid[i][j].isValue == False):
                y = 1
            val = grid[i][j].value
            for k in range(ITEMS_IN_ROW):
                if (grid[i][k].value == val and val != '' and k != j):
                    x = 1
                if (grid[k][j].value == val and val != '' and k != i):
                    x = 1
            startx = i - (i % 3)
            starty = j - (j % 3)
            for k in range(startx, startx + 3):
                for m in range(starty, starty + 3):
                    if (grid[k][m].value == val and val != '' and (k != i and m != j)):
                        x = 1
                        break
        if (y == 1):
            break
    if (y == 0 and x == 0):
        show_result(x)
    else:
        show_result(1)


def set_difficulty(d):
    ROOT_3.destroy()
    createGrid(d)
    global ROOT
    ROOT = tk.Tk()
    ROOT.title("SUDOKU")
    MakeGrid(ROOT).pack(side="top", fill="x")
    ROOT.mainloop()


def main():
    global ROOT_3
    ROOT_3 = tk.Tk()
    ROOT_3.title("ZVOLTE OBTIAŽNOSŤ")
    easy = tk.Button(ROOT_3, text="ĽAHKÁ", width=15, height=2, bg="Yellow", command=lambda: set_difficulty('easy'))
    easy.grid(row=0, column=3)
    easy.config(font=('helvetica', 25, 'bold italic'))
    medium = tk.Button(ROOT_3, text="STREDNÁ", width=15, height=2, bg="Green", command=lambda: set_difficulty('medium'))
    medium.grid(row=3, column=3)
    medium.config(font=('helvetica', 25, 'bold italic'))
    hard = tk.Button(ROOT_3, text="ŤAŽKÁ", width=15, height=2, bg="Red", command=lambda: set_difficulty('hard'))
    hard.grid(row=6, column=3)
    hard.config(font=('helvetica', 25, 'bold italic'))
    ROOT_3.mainloop()


main()
