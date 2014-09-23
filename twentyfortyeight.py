"""
2048 Game using the tkinter library
Author: Cole Lawrence (Lawrence0)
Version: 0.0.1
"""

import tkinter as tk

def key(event):
    print("pressed", repr(event.char))

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

        self._t_scoreLabel = tk.Label(self, text="Start Game")
        self._t_scoreLabel.grid()
        self._t_score = 0

        cellGrid = tk.Frame(self, width=480, height=480, padx=20, pady=20)
        cellGrid.grid()
        cells = []

        cellWidth = int(480/fontSize/columns)
        cellHeight = int(480/fontSize/rows*.56)
        print(cellWidth, cellHeight)
        for i in range(rows):
            for j in range(columns):
                newCell = tk.Label(cellGrid, text="a", width=cellWidth, height=cellHeight, font=self.customFont)
                newCell.grid(row=i, column=j)
                cells.append(newCell)

        self._t_cells = cells
        self._t_grid = cellGrid

        cellGrid.bind("<Key>", key)

        self.winfo_toplevel().bind("<Button-1>", lambda e: cellGrid.focus_set())
        #cellGrid.pack()

    def updateScore(self):
        self._scoreLabel["text"] = "Score: " + str(self._score)
