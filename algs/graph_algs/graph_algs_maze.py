



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
            for y in range(self.height):
                for x in range(self.width):
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
        o = QPoint(10, 10)

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

        painter.restore()


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


def main():
    
    maze = Maze()

    maze.loadMaze('maze.txt')

    print(maze.width, maze.height)
    print(maze.maze_array)

    maze.saveMaze('new_maze.txt')




    global app, window
    app = QApplication(sys.argv)
    window = Window()
    window.maze = maze
    window.resize(1100, 500)
    window.show()
    app.exec_()





if __name__ == '__main__':
    main()
