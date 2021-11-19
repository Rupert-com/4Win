import numpy as np
import copy
import os

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

    def add(self, str) -> None:
        self.p = np.append(self.p, str)
        if self.isFull():
            raise Exception("Error :(")

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

    def drawGrid(self) -> None:
        strgrid = ""
        for x in range(rows, -1, -1):
            strrow = "\n| "
            for cColume in self.grid:
                strrow += cColume[x] + (" | " if cColume != 0 else "")
            strgrid += strrow
        print(
            strgrid + "\n_____________________________\n| 1 | 2 | 3 | 4 | 5 | 6 | 7 |"
        )

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
        os.system("cls")
        while self.isWin() == False:
            try:
                colume = (
                    int(
                        input(
                            f"Game {self.cGamer} please select your colume[1-{len(self.grid)}]: "
                        )
                    )
                    - 1
                )
                # cGrid = copy.deepcopy()
                self.grid[colume].add(self.cGamer)
                # self.grid[colume] = cGrid
                self.cGamer = "O" if self.cGamer == "X" else "X"
                self.drawGrid()
            except IndexError as e:
                print(e)
                print(f"Bitte nur Zahlen von 0-{columns}")
            except Exception as e:
                print(e)
