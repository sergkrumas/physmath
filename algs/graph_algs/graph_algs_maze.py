



from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

import sys
import time


from enum import IntEnum

from collections import namedtuple

import random

class Location():

    def __init__(self):
        self.left_wall = False
        self.up_wall = False
        self.visited = False
        self.mark = 0

    def __repr__(self):
        return f'Location ({self.left_wall} {self.up_wall})'

def _generator(what_to_call, i):

    for i in range(i):
        yield what_to_call()

class Maze():

    def __getitem__(self, index):
        i, j = index
        value = self.maze_array[i][j]
        return value

    def __setitem__(self, index, value):
        i, j = index
        self.maze_array[i][j] = value

    def __init__(self):
        self.width = 0
        self.height = 0
        self.maze_array = []

        self.Path = []

    def setLength(self, w, h):
        self.maze_array = []
        for i in range(w):
            sa = list(_generator(Location, h))
            self.maze_array.append(sa)

    def readBoolPair(self, line):
        a, b = self.readIntPair(line)
        return bool(a), bool(b)

    def readIntPair(self, line):
        a, b = line.split(" ")
        return int(a), int(b)

    def loadMaze(self, filename):
        with open(filename, 'r', encoding='utf8') as file:
            lines = list(map(str.strip, file.readlines()))

            self.width, self.height = self.readIntPair(lines[0])
            self.setLength(self.width+1, self.height+1)

            i = 1
            for y in range(self.height+1):
                for x in range(self.width+1):
                    if y == self.height or x == self.width:
                        self[x, y].left_wall = True
                        self[x, y].up_wall = True
                    else:
                        a, b = self.readBoolPair(lines[i])
                        i += 1
                        self[x, y].left_wall = b
                        self[x, y].up_wall = a

    def saveMaze(self, filename):
        with open(filename, 'w+', encoding='utf8') as file:
            file.write(f'{self.width} {self.height}\n')
            for y in range(self.height):
                for x in range(self.width):
                    a = int(self[x, y].left_wall)
                    b = int(self[x, y].up_wall)
                    file.write(f'{b} {a}\n')

    def drawMaze(self, painter, widget):
        painter.save()

        CELLSIZE = 50
        o = offset = QPoint(10, 10)

        rect = QRect(0, 0, CELLSIZE*self.width, CELLSIZE*self.height)
        rect.moveTopLeft(o)
        painter.fillRect(rect, Qt.gray)

        painter.setPen(QPen(Qt.black, 2))

        for x in range(self.width):
            for y in range(self.height):
                cell = self[x, y]
                path = QPainterPath()
                if cell.up_wall:
                    path.moveTo(o + QPoint(x*CELLSIZE, y*CELLSIZE))
                    path.lineTo(o + QPoint((x+1)*CELLSIZE, y*CELLSIZE))
                if cell.left_wall:
                    path.moveTo(o + QPoint(x*CELLSIZE, y*CELLSIZE))
                    path.lineTo(o + QPoint(x*CELLSIZE, (y+1)*CELLSIZE))
                painter.drawPath(path)


        path = QPainterPath()
        path.moveTo(o + QPoint(0, self.height*CELLSIZE))
        path.lineTo(o + QPoint(self.width*CELLSIZE, self.height*CELLSIZE))
        path.lineTo(o + QPoint(self.width*CELLSIZE, 0))
        painter.drawPath(path)

        if self.Path:
            i = 0
            Path = self.Path
 
            for p in self.Path:
                xc = CELLSIZE * (2 * p.x() + 1) // 2
                yc = CELLSIZE * (2 * p.y() + 1) // 2
                rect1 = QRect(QPoint(xc-5, yc-5), QPoint(xc+5, yc+5))
                rect1.moveTopLeft(offset + rect1.topLeft())
                painter.drawEllipse(rect1)
                i += 1

        painter.restore()

    def recursiveSolve(self, s: QPoint, f: QPoint):

        Path = []

        DX = (1, 0, -1, 0)
        DY = (0, -1, 0, 1)

        # служебная функция, определяет
        # можно ли пройти из локации(x, y) в локацию (x+dx, y+dy),
        # то есть нет ли между ними стены
        def CanGo(x, y, dx, dy) -> bool:
            if dx == -1: return not self[x, y].left_wall
            elif dx == 1: return not self[x+1, y].left_wall
            elif dy == -1: return not self[x, y].up_wall
            else: return not self[x, y+1].up_wall

        # поиск финишной локации из точки (x, y)
        def Solve(x, y, depth) -> bool:

            nonlocal Path
            self[x, y].visited = True  #поменить локацию как посещённую

            if (x == f.x()) and (y == f.y()):
                Path.append(QPoint(x, y))
                return True

            for i in range(4):
                if CanGo(x, y, DX[i], DY[i]) and not self[x+DX[i], y+DY[i]].visited:
                    if Solve(x + DX[i], y + DY[i], depth + 1):
                        Path.append(QPoint(x, y))
                        return True

            self[x, y].visited = False

            return False

        for xx in range(self.width):
            for yy in range(self.height):
                self[xx, yy].visited = False

        if Solve(s.x(), s.y(), 0):
            self.Path = Path
            print('solved')
        else:
            self.Path = []
            print('not solved')


    def waveTracingSolve(self, s: QPoint, f: QPoint):

        Path = []

        DX = (1, 0, -1, 0)
        DY = (0, -1, 0, 1)

        # служебная функция, определяет
        # можно ли пройти из локации(x, y) в локацию (x+dx, y+dy),
        # то есть нет ли между ними стены
        def CanGo(x, y, dx, dy) -> bool:
            if dx == -1: return not self[x, y].left_wall
            elif dx == 1: return not self[x+1, y].left_wall
            elif dy == -1: return not self[x, y].up_wall
            else: return not self[x, y+1].up_wall

        # поиск решения
        def Solve() -> bool:

            N = 1

            while True:
                noSolution = True
                for x in range(self.width):
                    for y in range(self.height):
                        if self[x, y].mark == N:
                            for i in range(4):
                                if CanGo(x, y, DX[i], DY[i]) and (self[x + DX[i], y + DY[i]].mark == 0):
                                    noSolution = False
                                    self[x + DX[i], y + DY[i]].mark = N + 1
                                    if (x + DX[i] == f.x()) and (y + DY[i] == f.y()):
                                        return True
                N += 1
                if noSolution:
                    break
            return False


        for xx in range(self.width):
            for yy in range(self.height):
                self[xx, yy].mark = 0

        self[s.x(), s.y()].mark = 1



        if Solve():
            print('solved')

            x = f.x()
            y = f.y()

            finish_mark = self[f.x(), f.y()].mark
            for N in range(finish_mark, 0, -1):
                Path.append(QPoint(x, y))


                for i in range(4):
                    if CanGo(x, y, DX[i], DY[i]) and (self[x+DX[i], y + DY[i]].mark == N-1):
                        x += DX[i]
                        y += DY[i]
                        break

        else:
            print('not solved')


        self.Path = Path


    def PrimGenerateMaze(self, Width, Height):

        DX = (1, 0, -1, 0)
        DY = (0, -1, 0, 1)


        AttrTypeInside = 1
        AttrTypeOutside = 2
        AttrTypeBorder = 3

        def breakWall(x, y, dx, dy):
            if dx == -1: self[x, y].left_wall = False
            elif dx == 1: self[x+1, y].left_wall = False
            elif dy == -1: self[x, y].up_wall = False
            else: self[x, y+1].up_wall = False


        self.width = Width
        self.height = Height

        self.setLength(Width+1, Height+1)

        for x in range(Width):
            for y in range(Height):
                self[x, y].attribute = AttrTypeOutside

        for y in range(Height+1):
            for x in range(Width+1):
                self[x, y].left_wall = True
                self[x, y].up_wall = True

        x = random.randint(0, Width)
        y = random.randint(0, Height)
        self[x, y].attribute = AttrTypeInside


        for i in range(4):
            xc = x + DX[i]
            yc = y + DY[i]
            if (xc >= 0) and (yc >= 0) and (xc < Width) and (yc < Height):
                self[xc, yc].attribute = AttrTypeBorder

        ExitFor1 = False
        ExitFor2 = False
        ExitFor3 = False

        while True:
            isEnd = True
            counter = 0
            print('new cycle')
            for x in range(Width):
                for y in range(Height):
                    if self[x, y].attribute == AttrTypeBorder:
                        counter += 1

            counter = random.randint(0, counter) + 1
            for x in range(Width):
                if ExitFor1:
                    break
                for y in range(Height):
                    if ExitFor1:
                        break
                    if self[x, y].attribute == AttrTypeBorder:
                        counter -= 1
                        if counter == 0:
                            xloc = x
                            yloc = y
                            ExitFor1 = True
                            break
            if ExitFor1:
                print('exit for 1')
                self[xloc, yloc].attribute = AttrTypeInside

                counter = 0
                for i in range(4):
                    xc = xloc + DX[i]
                    yc = yloc + DY[i]
                    if (xc >= 0) and (yc >= 0) and (xc < Width) and (yc < Height):
                        if self[xc, yc].attribute == AttrTypeInside:
                            counter += 1
                        if self[xc, yc].attribute == AttrTypeOutside:
                            self[xc, yc].attribute = AttrTypeBorder

                counter = random.randint(0, counter) + 1
                for i in range(4):
                    xc = xloc + DX[i]
                    yc = yloc = DY[i]

                    if (xc >= 0) and (yc >= 0) and (xc < Width) and (yc < Height) and (self[xc, yc].attribute == AttrTypeInside):
                        counter -= 1
                        if counter == 0:
                            breakWall(xloc, yloc, DX[i], DY[i])
                            ExitFor2 = True
                            ExitFor1 = False
                            break

                ExitFor1 = False

            if ExitFor2:
                print('exit for 2')
                for x in range(Width):
                    if ExitFor3:
                        break
                    for y in range(Height):
                        if ExitFor3:
                            break
                        if self[x, y].attribute == AttrTypeBorder:
                            IsEnd = False
                            ExitFor3 = True
                            ExitFor2 = False
                            break

                ExitFor2 = False

            if ExitFor3:
                print('exit for 3')
                window.update()
                app.processEvents()

                ExitFor3 = False

            if isEnd:
                print('break of loop, isEnd =', isEnd)
                break

class Window(QWidget):


    def __init__(self,):
        super().__init__()
        self.maze = None

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        if self.maze:
            self.maze.drawMaze(painter, self)
        painter.end()


    def mousePressEvent(self, event):

        subMenu = QMenu()
        recursive_solve = subMenu.addAction("Рекурсивный обход")
        wave_tracing = subMenu.addAction("Волновая трассировка")
        subMenu.addSeparator()
        prim_generate_maze = subMenu.addAction("Алгоритм Прима")

        action = subMenu.exec_(QCursor().pos())
        if action is None:
            pass

        elif action is recursive_solve:
            print('recursive solve')
            self.maze.recursiveSolve(QPoint(0, 3), QPoint(4, 0))

        elif action is wave_tracing:
            print('wave tracing')
            self.maze.waveTracingSolve(QPoint(0, 0), QPoint(4, 0))

        elif action is prim_generate_maze:
            self.maze.PrimGenerateMaze(10, 8)




        self.update()


def main():
    
    maze = Maze()

    maze.loadMaze('maze.txt')

    print(maze.width, maze.height)
    print(maze.maze_array)

    # maze.saveMaze('new_maze.txt')




    global app, window
    app = QApplication(sys.argv)
    window = Window()
    window.maze = maze
    window.resize(1100, 500)
    window.show()
    app.exec_()





if __name__ == '__main__':
    main()
