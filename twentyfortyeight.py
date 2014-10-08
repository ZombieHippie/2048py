"""
2048 Game using the tkinter library
Author: Cole Lawrence (Lawrence0)
Version: 0.0.1
"""

import tkinter as tk
from random import randint


class Grid():
    def __init__(self, update, rows, columns):
        self._update = update
        self.rows = rows
        self.columns = columns
        self.cells = []
        for i in range(rows):
            self.cells.append([0] * columns)

        self.update()

    def update(self):
        if self.place_random():
            res = []
            for arr in self.cells:
                res += arr
            print("Updated grid")
            self._update(res)
        else:
            print("Gameover")
            self._update()

    def place_random(self):
        available = self.available_cells()

        if len(available) != 0:
            coords = available[randint(0, len(available))]
            self.cells[coords[0]][coords[1]] = randint(1, 2) * 2
            return True

        else:
            # Game over
            return False

    def available_cells(self):
        cells = []
        for x in range(self.rows):
            for y in range(self.columns):
                if self.cells[x][y] == 0:
                    cells.append((x, y))
        return cells

    def shift_up(self):
        self.update()

    def shift_down(self):
        self.update()

    def shift_left(self):
        self.update()

    def shift_right(self):
        self.update()


class App(tk.Frame):
    """Primary window for 2048 game display"""
    def __init__(self, master=None, rows=4, columns=4):
        super(App, self).__init__(master)
        self._t_w = rows
        self._t_h = columns

        fontSize = 16
        self.customFont = ("Helvetica", fontSize)

        self.grid()
        self.master.title("2048py")

        self._text_start = tk.StringVar()
        self._btn_start = tk.Button(self,
                                    textvariable=self._text_start,
                                    command=self.startGame)
        self._text_start.set("Start Game")
        self._btn_start.grid()

        self._text_score = tk.StringVar()
        self._text_score.set("Start Game")

        tk.Label(self, textvariable=self._text_score).grid()
        self._t_score = 0

        cellGrid = tk.Frame(self, width=480, height=480, padx=20, pady=20)
        cellGrid.grid()
        cellVars = []

        cellWidth = int(480/fontSize/columns)
        cellHeight = int(480/fontSize/rows*.56)
        print(cellWidth, cellHeight)
        for i in range(rows):
            for j in range(columns):
                newCellVar = tk.StringVar()
                newCell = tk.Label(cellGrid, textvariable=newCellVar,
                                   width=cellWidth, height=cellHeight,
                                   font=self.customFont)
                newCellVar.set("a")
                newCell.grid(row=i, column=j)
                cellVars.append(newCellVar)

        self._t_cells = cellVars
        self._t_grid = Grid(update=self.updateGridDisplay,
                            rows=rows, columns=columns)

        self.keyHandlers = {
            "w": self._t_grid.shift_up,
            "a": self._t_grid.shift_left,
            "d": self._t_grid.shift_right,
            "s": self._t_grid.shift_down
        }

        cellGrid.bind("<Key>", self.keyHandler)

        self.winfo_toplevel().bind("<Button-1>", lambda e: cellGrid.focus_set())
        #cellGrid.pack()

        self.gameStarted = False
        self.gameOver = False

        self.startGame()
        cellGrid.focus_set()

    def updateGridDisplay(self, numbersArray=False):
        if not numbersArray:
            self.gameOver = True
            self.endGame()
        else:
            for n in range(len(numbersArray)):
                value = numbersArray[n]
                value = "" if value is 0 else str(value)
                self._t_cells[n].set(value)

    def startGame(self):
        if not self.gameStarted and not self.gameOver:
            self.gameStarted = True
            self._text_start.set("Game in progress")

    def endGame(self):
        if self.gameOver:
            self._text_start.set("Game Over!")

    def keyHandler(self, event):
        letter = str(event.char)
        if self.gameStarted and letter in self.keyHandlers:
            self.keyHandlers[letter]()

    def updateScore(self):
        self._text_score.set("Score: " + str(self._score))
