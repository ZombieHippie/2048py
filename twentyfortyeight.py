"""
2048 Game using the tkinter library
Author: Cole Lawrence (Lawrence0)
Version: 0.0.1
"""

import tkinter as tk


class Grid():
    def __init__(self, update, end, rows, columns):
        self._update = update
        self.end = end
        self.rows = rows
        self.columns = columns
        self.cells = []
        for i in range(rows):
            self.cells.append([0] * columns)

        self.update()

    def update(self):
        res = []
        for arr in self.cells:
            res += arr
        self._update(res)

    def shiftUp(self):
        self.update()

    def shiftDown(self):
        self.update()

    def shiftLeft(self):
        self.update()

    def shiftRight(self):
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

        self._t_gameStartBtnText = tk.StringVar()
        self._t_gameStartBtn = tk.Button(self,
                                         textvariable=self._t_gameStartBtnText,
                                         command=self.startGame)
        self._t_gameStartBtnText.set("Start Game")
        self._t_gameStartBtn.grid()

        self._t_scoreLabel = tk.Label(self, text="Start Game")
        self._t_scoreLabel.grid()
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
        self._t_grid = Grid(update=self.updateGridDisplay, end=self.endGame,
                            rows=rows, columns=columns)

        self.keyHandlers = {
            "w": self._t_grid.shiftUp,
            "a": self._t_grid.shiftLeft,
            "d": self._t_grid.shiftRight,
            "s": self._t_grid.shiftDown
        }

        cellGrid.bind("<Key>", self.keyHandler)

        self.winfo_toplevel().bind("<Button-1>", lambda e: cellGrid.focus_set())
        #cellGrid.pack()

        self.gameStarted = False
        self.gameOver = False

        self.startGame()
        cellGrid.focus_set()

    def updateGridDisplay(self, numbersArray):
        print(numbersArray)
        for n in range(len(numbersArray)):
            value = numbersArray[n]
            value = "" if value is 0 else str(value)
            self._t_cells[n].set(value)

    def startGame(self):
        if not self.gameStarted and not self.gameOver:
            self.gameStarted = True
            self._t_gameStartBtnText.set("Game in progress")

    def endGame(self):
        if self.gameStarted and not self.gameOver:
            self.gameOver = True
            self._t_gameStartBtn["text"] = "Game in progress"

    def keyHandler(self, event):
        letter = str(event.char)
        if self.gameStarted and letter in self.keyHandlers:
            self.keyHandlers[letter]()

    def updateScore(self):
        self._scoreLabel["text"] = "Score: " + str(self._score)
