import numpy as np
import copy
import os
import PySimpleGUI as sg

rows = 6 - 1
columns = 7


class Win(Exception):
    """Raised when a player has won"""

    pass


class colume:
    col = -1
    p = np.array([])

    def __init__(self, col) -> None:
        self.col = col

    def isFull(self) -> bool:
        return (len(self.p) - 1) > rows

    def add(self, str):
        self.p = np.append(self.p, str)
        if self.isFull():
            raise Exception("Error :(")
        return [len(self.p), self.col - 1]

    def getLast(self):
        cLen = len(self.p)
        if cLen > 0:
            return [cLen, self.p[cLen - 1]]
        return [-1, ""]

    # def __iter__(self) -> str:
    #     pass

    def __getitem__(self, key) -> str:
        if len(self.p) > key and key >= 0:
            return self.p[key]

        return "-"


class app:
    grid: any
    cGamer = "X"

    def __init__(self) -> None:
        cGrid = []
        for x in range(columns):
            cGrid.append(colume(x))

        self.grid = np.array(cGrid)

        headings = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
        ]
        header = [[sg.Text(h, size=(3, 1), pad=(30, 0)) for h in headings]]

        input_rows = [
            [
                sg.Text(
                    size=(3, 1),
                    pad=(30, 0),
                    key=(f"{col}{row}"),
                    # text=f"{col}{row}",
                )
                for col in range(0, len(headings))
            ]
            for row in range(rows, 0, -1)
        ]

        self.Window = sg.Window(
            "4 Gewinnt GUI",
            [
                [
                    sg.Column(
                        header
                        + input_rows
                        + [
                            [
                                sg.Text(
                                    key="player",
                                    size=(30, 1),
                                    justification="center",
                                ),
                            ],
                            [
                                sg.InputText(key="row"),
                            ],
                            [
                                sg.Button(key="btn", button_text="submit"),
                            ],
                        ]
                    ),
                ]
            ],
            finalize=True,
        )
        self.Window["row"].bind("<Return>", "_Enter")

    def WindowsDrawCPlayer(self) -> None:
        self.Window["player"].update(
            f"Gamer {self.cGamer} please select your colume[1-{len(self.grid)}]"
        )

    def drawGrid(self) -> None:
        table = np.array()
        for cR in range(rows):
            row = np.array([])
            for cC in range(columns):
                cGrid = self.grid[cC]
                # Not array instead convert to dictonary
                # https://stackoverflow.com/questions/37949409/dictionary-in-a-numpy-array
                row = np.append(row, (cGrid[cR]))
            table = np.append(table, row)
        self.Window["-TABLE-"].update(values=table[1:][:])

    def isWin(self) -> None:
        try:
            # Check if !cGamer has a win
            cGamer = "O" if self.cGamer == "X" else "X"
            # check vertical |
            for cGrid in self.grid:
                [cLen, last] = cGrid.getLast()
                if cLen < 0:
                    continue
                cFoundEl = 1
                if last == cGamer:
                    for ccR in range(2, 5):
                        last = cGrid[cLen - ccR]
                        if last != cGamer:
                            break
                        cFoundEl += 1
                        if cFoundEl == 4:
                            raise Win(f"Player {cGamer} won - [vertical]")
                # check horizontal ----
            for cR in range(rows):
                cFoundEl = 1
                for cC in range(columns):
                    cGrid = self.grid[cC]
                    cPlayer = cGrid[cR]
                    # print(f"{cC}/{cR}: {cPlayer} {cFoundEl}")
                    if cPlayer == cGamer:
                        cFoundEl += 1
                    else:
                        cFoundEl = 1
                    if cFoundEl == 4:
                        raise Win(f"Player {cGamer} won - [horizontal]")

                # check diagonal /
            for ccR in range(rows - 4):
                for ccC in range(columns - 4):
                    a = self.grid[5][ccC]
                    b = self.grid[rows - ccR - 1][ccC + 1]
                    c = self.grid[rows - ccR - 2][ccC + 2]
                    d = self.grid[rows - ccR - 3][ccC + 3]
                    if [a, b, c, d] == 4 * [cGamer]:
                        raise Win(f"Player {cGamer} won - [diagonal /]")

            # check diagonal \
            for ccR in range(rows - 4):
                for ccC in range(columns - 4):
                    a = self.grid[ccR][ccC]
                    b = self.grid[ccR + 1][ccC + 1]
                    c = self.grid[ccR + 2][ccC + 2]
                    d = self.grid[ccR + 3][ccC + 3]
                    if [a, b, c, d] == 4 * [cGamer]:
                        raise Win(f"Player {cGamer} won - [diagonal \]")
            return False
        except Win as e:
            print(repr(e))
            return True

    def loop(self) -> None:
        self.WindowsDrawCPlayer()
        whiling = True

        while True:
            try:
                event, values = self.Window.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                elif event == "btn":
                    if whiling == True:
                        [row, col] = self.grid[int(values["row"])].add(self.cGamer)
                        self.Window[f"{col}{row}"].update(self.cGamer)

                        # self.grid[colume] = cGrid
                        self.cGamer = "O" if self.cGamer == "X" else "X"

                        if self.isWin():
                            whiling = False
                            self.Window["row"].update(f"player {self.cGamer} won")
                        else:
                            self.Window["row"].update("")

                        self.WindowsDrawCPlayer()
                        # self.drawGrid()
                    else:
                        # TODO restart :)
                        pass
            except IndexError as e:
                print(e)
                print(f"Bitte nur Zahlen von 0-{columns}")
            except Exception as e:
                print(e)
