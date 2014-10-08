"""
2048 Game using the tkinter library
Author: Cole Lawrence (Lawrence0)
Version: 0.0.1
"""

import tkinter as tk
from random import randint
nsew = tk.N + tk.S + tk.W + tk.E


class Grid():
    def __init__(self, update, rows, columns, score_adj):
        self._update = update
        self.score_adjust = score_adj
        self.rows = rows
        self.columns = columns
        self.cells = []
        for i in range(rows):
            self.cells.append([0] * columns)

        self.update()

    def update(self, add_random=True):
        if add_random:
            if self.place_random():
                res = []
                for arr in self.cells:
                    res += arr
                self._update(res)
            else:
                print("Gameover")
                self._update()

    def place_random(self):
        available = self.available_cells()

        if len(available) != 0:
            coords = available[randint(0, len(available) - 1)]
            self.cells[coords[0]][coords[1]] = randint(1, 2) * 2
            return True

        else:
            # Game over
            return False

    def in_bounds(self, x, y):
        return x > -1 and y > -1 and x < self.rows and y < self.columns

    def cell_available(self, x, y):
        return self.cells[y][x] == 0

    def available_cells(self):
        cells = []
        for x in range(self.rows):
            for y in range(self.columns):
                if self.cell_available(x, y):
                    cells.append((y, x))
        return cells

    def move(self, dx, dy):
        (x_traversals, y_traversals) = self.build_traversals(dx, dy)

        # set-up merges
        merges = []
        for i in range(self.rows):
            merges.append([False] * self.columns)

        moved = False

        for x in x_traversals:
            for y in y_traversals:
                current_tile = self.cells[y][x]
                (farthest_x, farthest_y, next_x, next_y) = self.find_farthest(x, y, dx, dy)
                merged = False

                next_tile = False
                if self.in_bounds(next_x, next_y):
                    next_tile = self.cells[next_y][next_x]
                
                if next_tile != False and next_tile == current_tile and merges[x][y] == False:
                    merges[x][y] = True
                    # combine
                    self.cells[y][x] = 0
                    self.cells[next_y][next_x] *= 2
                    self.score_adjust(self.cells[next_y][next_x])
                    moved = True
                elif farthest_x != x or farthest_y != y:
                    self.cells[farthest_y][farthest_x] = self.cells[y][x]
                    self.cells[y][x] = 0
                    moved = True
        return moved

    def find_farthest(self, cx, cy, dx, dy):
        while True:
            farthest_x = cx
            farthest_y = cy
            next_x = cx + dx
            next_y = cy + dy
            cx += dx
            cy += dy
            if not self.in_bounds(cx, cy) or \
                not self.cell_available(cx, cy):
                break
        return (farthest_x, farthest_y, next_x, next_y)

    def build_traversals(self, dx, dy):
        xt = list(range(self.rows))
        yt = list(range(self.columns))
        if dx == 1:
            xt.reverse()
        if dy == 1:
            yt.reverse()
        return (xt, yt)

    def shift_up(self):
        self.update(add_random=self.move(0, -1))

    def shift_down(self):
        self.update(add_random=self.move(0, 1))

    def shift_left(self):
        self.update(add_random=self.move(-1, 0))

    def shift_right(self):
        self.update(add_random=self.move(1, 0))


class App(tk.Frame):
    """Primary window for 2048 game display"""
    def __init__(self, master=None, rows=4, columns=4):
        super(App, self).__init__(master)
        self._t_w = rows
        self._t_h = columns

        fontSize = 16
        self.customFont = ("Helvetica", fontSize)

        self.master.title("2048py")
        self.master.rowconfigure(0, weight = 1)
        self.master.columnconfigure(0, weight = 1)

        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1)
        
        self.grid(sticky = nsew)

        btns = tk.Frame(self, bg="gray")
        btns.grid(row=0, column=0, sticky = nsew)
        btns.columnconfigure(0, weight = 1)
        btns.columnconfigure(1, weight = 1)

        self._text_start = tk.StringVar()
        self._btn_start = tk.Button(btns,
                                    textvariable=self._text_start,
                                    command=self.startGame)
        self._text_start.set("Start Game")
        self._btn_start.grid(column=0, row=0)

        self._text_status = tk.StringVar()
        self._text_status.set("Start Game")

        tk.Label(btns, textvariable=self._text_status, bg="gray").grid(column=0, row=2)
        self._t_score = 0

        self._text_score = tk.StringVar()
        tk.Label(btns, textvariable=self._text_score, font="Helvetica 24").grid(column=1, row=0, rowspan=2, sticky=nsew)

        cellGrid = tk.Frame(self, padx=20, pady=20)
        cellGrid.grid(row=1, column=0, sticky = nsew)
        cellVars = []

        for i in range(rows):
            cellGrid.rowconfigure(i, weight=1)
            for j in range(columns):
                if i == 0:
                    cellGrid.columnconfigure(j, weight=1)
                newCellVar = tk.StringVar()
                newCell = tk.Label(cellGrid, textvariable=newCellVar,
                                   font=self.customFont, bg="#f5f5f5")
                newCellVar.set("a")
                newCell.grid(row=i, column=j, sticky = nsew)
                cellVars.append(newCellVar)

        self._t_cells = cellVars

        self._t_grid = Grid(update=self.updateGridDisplay,
                            rows=rows, columns=columns,
                            score_adj=self.score_change)

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

    def score_change(self, adj):
        self._t_score += adj
        self.updateScore()

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
        self._text_score.set(str(self._t_score))
