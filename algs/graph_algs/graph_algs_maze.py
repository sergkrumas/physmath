



from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

import sys
import time


from enum import IntEnum

from collections import namedtuple


# f = namedtuple('Location', 'left_wall right_wall up_wall down_wall')



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



    def _check_indexes(self, i, j):
        if 0 <= i <= self.width and 0 <= j <= self.height:
            pass
        else:
            raise IndexError()

    def __getitem__(self, index):
        i, j = index
        self._check_indexes(i, j)
        value = self.maze_array[self.width*i+j]
        return value

    def __setitem__(self, index, value):
        i, j = index
        self._check_indexes(i, j)
        self.maze_array[self.width*i+j] = value

    def LEN(self):
        self.width * self.height

    def __init__(self):
        self.width = 0
        self.height = 0
        self.maze_array = []

        self.allowed_indexes = (0, 1, 2)

        self.Path = []

    def setLength(self, w, h):
        elements_count = w*h
        self.maze_array = list(_generator(Location, elements_count)) 

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
 
            # while not ((Path[i].x() == -1) and Path[i].y() == -1):
                # p = Path[i]

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
            print('solve depth', depth)
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
            self.Path = [QPoint(0, 0), QPoint(5, 0)]
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

        # if Solve(s.x(), s.y(), 0):
        #     self.Path = Path
        #     print('solved')
        # else:
        #     self.Path = [QPoint(0, 0), QPoint(5, 0)]
        #     print('not solved')


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

        action = subMenu.exec_(QCursor().pos())
        if action is None:
            pass

        elif action is recursive_solve:
            print('recursive solve')
            self.maze.recursiveSolve(QPoint(0, 3), QPoint(4, 0))

        elif action is wave_tracing:
            print('wave tracing')
            self.maze.waveTracingSolve(QPoint(0, 0), QPoint(4, 0))


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
