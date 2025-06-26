



from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

import sys
import os
import time
from enum import IntEnum
import random

from collections import defaultdict

atNull = 0
atInside = 1
atOutside = 2
atBorder = 3

atToStr = {
    atNull: 'null',
    atInside: 'inside',
    atOutside: 'outside',
    atBorder: 'border'
}


class Location():

    def __init__(self):
        self.left_wall = False
        self.up_wall = False
        self.visited = False
        self.mark = 0
        self.multimark = defaultdict(int)
        self.attr = 0
        self.start = False
        self.meet_loc = False
        self.direction = -1

    def __repr__(self):
        return f'Location ({self.left_wall} {self.up_wall})'

def _generator(what_to_call, i):
    for i in range(i):
        yield what_to_call()

def randint(n):
    return random.randint(0, n-1)

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
        self.main_offset = QPoint(10, 10)

        self.prepare_arrows()

    def prepare_arrows(self):
        f = 15
        h = 5
        ap0 = [QPoint(f, 0), QPoint(-f, 0), QPoint(f-15, h), QPoint(f-15, -h)]
        self.aps = [ap0]
        ap = ap0
        for i in range(3):
            # rotate 90 degress counterclockwise
            ap = list(map(lambda p: QPoint(p.y(), -p.x()), ap))
            self.aps.append(ap)

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

        def draw_arrow(ap, center):
            _ap = [QPoint(p) for p in ap]
            for p in _ap:
                p += center
            painter.drawLine(_ap[0], _ap[1])
            painter.drawLine(_ap[0], _ap[2])
            painter.drawLine(_ap[0], _ap[3])

        CELLSIZE = 60

        o = offset = self.main_offset

        rect = QRect(0, 0, CELLSIZE*self.width, CELLSIZE*self.height)
        rect.moveTopLeft(o)
        painter.fillRect(rect, Qt.gray)

        MAX_N = 0
        MAX_N_0 = 0
        MAX_N_1 = 0
        for x in range(self.width):
            for y in range(self.height):
                cell = self[x, y]
                MAX_N = max(MAX_N, cell.mark)
                MAX_N_0 = max(MAX_N_0, cell.multimark[0])
                MAX_N_1 = max(MAX_N_1, cell.multimark[1])

        widget.maze_cells.clear()

        for x in range(self.width):
            for y in range(self.height):
                cell = self[x, y]

                is_mouse_marked_cell = False
                for p in window.points:
                    if p.x() == x and p.y() == y:
                        is_mouse_marked_cell = True
                        break

                r1 = QRect(QPoint(x*CELLSIZE, y*CELLSIZE), QPoint((x+1)*CELLSIZE, (y+1)*CELLSIZE))
                r1.moveTopLeft(o + r1.topLeft())

                painter.setPen(QPen(Qt.red, 4))
                if is_mouse_marked_cell:
                    r1_small = r1.adjusted(10, 10, -10, -10)
                    painter.drawLine(r1_small.topLeft(), r1_small.bottomRight())
                    painter.drawLine(r1_small.bottomLeft(), r1_small.topRight())

                widget.maze_cells.append((r1, x, y))

                if cell.start:
                    painter.fillRect(r1, QColor(220, 100, 100))

                if MAX_N != 0:
                    factor = cell.mark/MAX_N
                    color = QColor.fromHslF(0.6, factor, factor*0.5, 0.5)
                    painter.fillRect(r1, color)
                else:
                    for n, _max in enumerate((MAX_N_0, MAX_N_1)):
                        if _max != 0:
                            mark_value = cell.multimark[n]
                            if mark_value == 0.0: # если это закоментировать, то остальные клетки будут темнеть
                                continue
                            factor = mark_value/_max
                            if n == 0:
                                hue = 0.6
                            else:
                                hue = 1.0
                            if cell.meet_loc:
                                hue = 0.2
                            if mark_value == 1.0:
                                factor = 1.0
                            color = QColor.fromHslF(hue, factor, 0.5, factor*0.5)

                            if mark_value == 1.0:
                                r1 = r1.adjusted(10, 10, -10, -10)

                            painter.fillRect(r1, color)

                            painter.save()
                            direction = cell.direction
                            if direction != -1 and not cell.meet_loc:
                                color = QColor.fromHslF(hue, 1.0, 0.5, 1.0)
                                painter.setPen(QPen(color, 4))
                                draw_arrow(self.aps[direction], r1.center())
                            painter.restore()

                painter.setPen(QPen(Qt.black, 2))
                path = QPainterPath()
                if cell.up_wall:
                    path.moveTo(o + QPoint(x*CELLSIZE, y*CELLSIZE))
                    path.lineTo(o + QPoint((x+1)*CELLSIZE, y*CELLSIZE))
                if cell.left_wall:
                    path.moveTo(o + QPoint(x*CELLSIZE, y*CELLSIZE))
                    path.lineTo(o + QPoint(x*CELLSIZE, (y+1)*CELLSIZE))
                painter.drawPath(path)

                attr = atToStr[self[x, y].attr]
                text = f'{cell.multimark[0]} {cell.multimark[1]}\n{attr}\n{x}:{y}'

                color = {
                    0: Qt.black,
                    1: Qt.white,
                    2: QColor(100, 100, 100),
                    3: Qt.blue
                }

                painter.setPen(QPen(color[self[x, y].attr], 2))
                painter.drawText(r1, Qt.AlignCenter, text)

        painter.setPen(QPen(Qt.black, 2))

        path = QPainterPath()
        path.moveTo(o + QPoint(0, self.height*CELLSIZE))
        path.lineTo(o + QPoint(self.width*CELLSIZE, self.height*CELLSIZE))
        path.lineTo(o + QPoint(self.width*CELLSIZE, 0))
        painter.drawPath(path)

        painter.setPen(QPen(Qt.red, 3))
        if self.Path:
            i = 0
            for p in self.Path:
                xc = CELLSIZE * (2 * p.x() + 1) // 2
                yc = CELLSIZE * (2 * p.y() + 1) // 2
                rect1 = QRect(QPoint(xc-5, yc-5), QPoint(xc+5, yc+5))
                rect1.moveTopLeft(offset + rect1.topLeft())
                painter.drawEllipse(rect1)
                i += 1

        painter.restore()

    def recursiveSolve(self, s: QPoint, f: QPoint):

        self.Path = []

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

            p = QPoint(x, y)
            self[x, y].visited = True  #поменить локацию как посещённую
            self.Path.append(p)

            window.update()
            app.processEvents()
            time.sleep(0.2)

            if (x == f.x()) and (y == f.y()):
                # Path.append(QPoint(x, y))
                return True

            for i in range(4):
                if CanGo(x, y, DX[i], DY[i]) and not self[x+DX[i], y+DY[i]].visited:
                    if Solve(x + DX[i], y + DY[i], depth + 1):
                        # Path.append(QPoint(x, y))
                        return True

            self.Path.remove(p)
            self[x, y].visited = False

            return False

        for xx in range(self.width):
            for yy in range(self.height):
                self[xx, yy].visited = False

        if Solve(s.x(), s.y(), 0):
            # print('solved')
            pass
        else:
            self.Path = []
            # print('not solved')

    def waveTracingSolve(self, s: QPoint, f: QPoint, freeze=0.2):

        self.Path = []

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


        def make_iteration_copy_and_clear(data_list):
            _iteration_copy = data_list[:]
            data_list.clear()
            return _iteration_copy

        # поиск решения
        def Solve() -> bool:

            N_mark_locations = []

            loc = self[s.x(), s.y()]
            loc.mark = 1
            N_mark_locations.append(loc)

            N = 1
            while True:

                window.update()
                app.processEvents()
                time.sleep(freeze)

                noSolution = True
                for loc in make_iteration_copy_and_clear(N_mark_locations):
                    for i in range(4):
                        try:
                            cur_loc = self[loc._xx + DX[i], loc._yy + DY[i]]
                        except (IndexError, AttributeError):
                            continue
                        if CanGo(loc._xx, loc._yy, DX[i], DY[i]) and (cur_loc.mark == 0):
                            noSolution = False
                            cur_loc.mark = N + 1
                            N_mark_locations.append(cur_loc)
                            if (loc._xx + DX[i] == f.x()) and (loc._yy + DY[i] == f.y()):
                                return True

                N += 1
                if noSolution:
                    break
            return False

        for xx in range(self.width):
            for yy in range(self.height):
                l  = self[xx, yy]
                l.mark = 0
                l._xx = xx
                l._yy = yy

        if Solve():
            # print('solved')
            x = f.x()
            y = f.y()

            finish_mark = self[x, y].mark
            for N in range(finish_mark, 0, -1):
                self.Path.append(QPoint(x, y))
                for i in range(4):
                    if CanGo(x, y, DX[i], DY[i]) and (self[x+DX[i], y+DY[i]].mark == N-1):
                        x += DX[i]
                        y += DY[i]
                        break
            return True
        else:
            # print('not solved')
            self.Path = []
            return False

    def doubleWaveTracingSolve(self, start: QPoint, finish: QPoint, freeze=0.2):

        DX = (1, 0, -1, 0)
        DY = (0, -1, 0, 1)
        # i       0   1   2   3
        # angle   0   90  180 270

        # служебная функция, определяет
        # можно ли пройти из локации(x, y) в локацию (x+dx, y+dy),
        # то есть нет ли между ними стены
        def CanGo(x, y, dx, dy) -> bool:
            if dx == -1: return not self[x, y].left_wall
            elif dx == 1: return not self[x+1, y].left_wall
            elif dy == -1: return not self[x, y].up_wall
            else: return not self[x, y+1].up_wall

        def makeIterationCopyAndClear(data_list):
            _iteration_copy = data_list[:]
            data_list.clear()
            return _iteration_copy

        # поиск решения

        meet_loc = None
        def Solve(start_point, end_point, _id) -> bool:
            nonlocal meet_loc

            step_list = []

            loc = self[start_point.x(), start_point.y()]
            loc.multimark[_id] = 1
            step_list.append(loc)

            N = 1
            while True:

                window.update()
                app.processEvents()
                time.sleep(freeze)

                noSolution = True
                for loc in makeIterationCopyAndClear(step_list):
                    for i in range(4):
                        try:
                            cur_loc = self[loc._xx + DX[i], loc._yy + DY[i]]
                        except (IndexError, AttributeError):
                            continue
                        if CanGo(loc._xx, loc._yy, DX[i], DY[i]) and (cur_loc.multimark[_id] == 0):
                            noSolution = False
                            cur_loc.multimark[_id] = N + 1
                            cur_loc.direction = i
                            step_list.append(cur_loc)
                            if (_id == 1 and cur_loc.multimark[0] != 0) or (_id == 0 and cur_loc.multimark[1] != 0):
                                # когда два "киселя" встречаются, запоминаем место встречи и заканчиваем просчёт;
                                # встретится они могут во время просчёта шагов первого и второго "киселей"
                                meet_loc = cur_loc
                                meet_loc.meet_loc = True
                                return StopIteration
                            if (loc._xx + DX[i] == end_point.x()) and (loc._yy + DY[i] == end_point.y()):
                                return StopIteration

                N += 1
                if noSolution:
                    break

                yield True
            yield False

        for xx in range(self.width+1):
            for yy in range(self.height+1):
                l  = self[xx, yy]
                l.multimark = defaultdict(int)
                l.meet_loc = False
                l._xx = xx
                l._yy = yy

        r1 = r2 = False
        for r1, r2 in zip(Solve(start, finish, 0), Solve(finish, start, 1)):
            pass
            # print(r1, r2)

        self.Path = []

        if r1 and r2 and meet_loc is not None:

            to_prevent_double_in_path = True
            x = meet_loc._xx
            y = meet_loc._yy
            meet_mark_for_1 = self[x, y].multimark[1]
            for N in range(meet_mark_for_1, 0, -1):
                if to_prevent_double_in_path:
                    to_prevent_double_in_path = False
                else:
                    self.Path.append(QPoint(x, y))
                for i in range(4):
                    if CanGo(x, y, DX[i], DY[i]) and (self[x+DX[i], y+DY[i]].multimark[1] == N-1):
                        x += DX[i]
                        y += DY[i]
                        break

            x = meet_loc._xx
            y = meet_loc._yy
            meet_mark_for_0 = self[x, y].multimark[0]
            for N in range(meet_mark_for_0, 0, -1):
                self.Path.insert(0, QPoint(x, y))
                for i in range(4):
                    if CanGo(x, y, DX[i], DY[i]) and (self[x+DX[i], y+DY[i]].multimark[0] == N-1):
                        x += DX[i]
                        y += DY[i]
                        break

            # чтобы подержать точку пересечения
            window.update()
            app.processEvents()
            time.sleep(freeze)

            return True
        else:
            return False

    def PrimGenerateMaze(self, Width, Height):

        DX = (1, 0, -1, 0)
        DY = (0, -1, 0, 1)

        def breakWall(x, y, dx, dy):
            if dx == -1:
                self[x, y].left_wall = False
            elif dx == 1:
                self[x+1, y].left_wall = False
            elif dy == -1:
                self[x, y].up_wall = False
            else:
                self[x, y+1].up_wall = False

        def check_bounds(xc, yc):
            return (xc >= 0) and (yc >= 0) and (xc < Width) and (yc < Height)

        self.Path = []

        self.width = Width
        self.height = Height

        self.setLength(Width+1, Height+1)

        for x in range(Width):
            for y in range(Height):
                self[x, y].attr = atOutside

        for x in range(Width+1):
            for y in range(Height+1):
                l = self[x, y]
                l.left_wall = True
                l.up_wall = True
                l._xx = x
                l._yy = y

        random.seed(random.randint(0, 1000))
        x = randint(Width) # выбираем начальную локацию
        y = randint(Height) # и присваиваем ей атрибут Inside
        self[x, y].attr = atInside
        self[x, y].start = True

        border_locations = []
        cur_loc = None

        for i in range(4):  # всем её соседям присваиваем атрибут Border
            xc = x + DX[i]
            yc = y + DY[i]
            if check_bounds(xc, yc):
                loc = self[xc, yc]
                loc.attr = atBorder
                border_locations.append(loc)

        while True:  # главный цикл
            window.update()
            app.processEvents()
            time.sleep(0.1)

            if border_locations:
                cur_loc = random.choice(border_locations) # выбираем одну случайную
                border_locations.remove(cur_loc)

                cur_loc.attr = atInside

                inside_locations = []
                for i in range(4):
                    xc = cur_loc._xx + DX[i]
                    yc = cur_loc._yy + DY[i]
                    l = self[xc, yc]
                    if check_bounds(xc, yc):
                        if l.attr == atInside:
                            l.dx = DX[i]
                            l.dy = DY[i]
                            inside_locations.append(l)
                        if l.attr == atOutside:
                            l.attr = atBorder
                            border_locations.append(l)

                r_loc = random.choice(inside_locations)
                breakWall(cur_loc._xx, cur_loc._yy, r_loc.dx, r_loc.dy)
            else:
                break

    def KruskalGenerateMaze(self, Width, Height):

        def breakWall(x, y, dx, dy):
            if dx == -1:
                self[x, y].left_wall = False
            elif dx == 1:
                self[x+1, y].left_wall = False
            elif dy == -1:
                self[x, y].up_wall = False
            else:
                self[x, y+1].up_wall = False

        def isConnected(xs, ys, xf, yf):
            # res = self.waveTracingSolve(QPoint(xs, ys), QPoint(xf, yf), freeze=0.1)
            res = self.doubleWaveTracingSolve(QPoint(xs, ys), QPoint(xf, yf), freeze=0.1)
            self.Path = []
            return res

        class Wall():
            def __init__(self):
                self.x = 0
                self.y = 0
                self.dx = 0
                self.dy = 0


        self.width = Width
        self.height = Height

        self.setLength(Width+1, Height+1)

        walls = list()

        for i in range(Width+1):
            for j in range(Height+1):
                self[i, j].left_wall = True
                self[i, j].up_wall = True

        # заполнение массива стен
        for i in range(Width):
            for j in range(Height): #сначала все горизонтальные
                wall = Wall()
                wall.x = i
                wall.y = j
                wall.dx = -1
                wall.dy = 0

                walls.append(wall)

        for i in range(Width):
            for j in range(Height):
                wall = Wall() #потом все вертикальные
                wall.x = i
                wall.y = j
                wall.dx = 0
                wall.dy = -1
                walls.append(wall)

        random.shuffle(walls)

        while walls:
            cur_wall = walls.pop()
            if not isConnected(cur_wall.x, cur_wall.y, cur_wall.x + cur_wall.dx, cur_wall.y + cur_wall.dy):
                breakWall(cur_wall.x, cur_wall.y, cur_wall.dx, cur_wall.dy)
                window.update()
                app.processEvents()
                time.sleep(0.1)

class Window(QWidget):


    def __init__(self,):
        super().__init__()
        self.maze = None
        self.maze_cells = []
        self.points = []
        self.points.append(QPoint(0, 0))
        self.points.append(QPoint(4, 0))

        self.insert_index = 0
        self.insert_activated = False

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        if self.maze:
            self.maze.drawMaze(painter, self)
        painter.end()

    def maze_cell_rect_to_cell_indexes(self, event, i):
        for r1, x, y in self.maze_cells:
            if r1.contains(event.pos()):
                self.points[i] = QPoint(x, y)

    def mousePressEvent(self, event):

        if self.insert_activated:
            self.maze_cell_rect_to_cell_indexes(event, self.insert_index)
            if self.insert_index == 0:
                self.insert_index = 1
            elif self.insert_index == 1:
                self.insert_index = 0
                self.insert_activated = False
        else:

            path = os.path.join(os.path.dirname(__file__), 'new_maze.txt')

            subMenu = QMenu()
            recursive_solve = subMenu.addAction("Рекурсивный обход")
            wave_tracing = subMenu.addAction("Волновая трассировка")
            double_wave_tracing = subMenu.addAction("Волновая трассировка из обоих концов")

            subMenu.addSeparator()
            prim_generate_maze = subMenu.addAction("Алгоритм Прима")
            kruskal_generate_maze = subMenu.addAction("Алгоритм Краскала")
            subMenu.addSeparator()
            set_start_and_finish_points = subMenu.addAction("Задать стартовую и финишную точки")
            subMenu.addSeparator()
            save_maze = subMenu.addAction("Сохранить")
            open_maze = subMenu.addAction("Открыть")

            action = subMenu.exec_(QCursor().pos())
            if action is None:
                pass

            elif action is recursive_solve:
                print('recursive solve')
                self.maze.recursiveSolve(self.points[0], self.points[1])

            elif action is wave_tracing:
                print('wave tracing')
                self.maze.waveTracingSolve(self.points[0], self.points[1])

            elif action is double_wave_tracing:
                print('double wave tracing')
                self.maze.doubleWaveTracingSolve(self.points[0], self.points[1])

            elif action is prim_generate_maze:
                self.maze.PrimGenerateMaze(10, 8)

            elif action is kruskal_generate_maze:
                self.maze.KruskalGenerateMaze(10, 8)

            elif action is set_start_and_finish_points:
                self.insert_activated = True

            elif action is save_maze:
                data = QFileDialog.getSaveFileName(self, "Save file", f"{path}", None)
                path = data[0]
                if path:
                    self.maze.saveMaze(path)

            elif action is open_maze:
                dialog = QFileDialog()
                dialog.setFileMode(QFileDialog.ExistingFile)
                data = dialog.getOpenFileName(self, "Open file", path, "Maze File (*.txt)")
                path = data[0]
                if path:
                    self.maze.loadMaze(path)


        self.update()


def main():

    global app, window
    app = QApplication(sys.argv)

    maze = Maze()
    maze.loadMaze('maze.txt')

    window = Window()
    window.maze = maze
    window.resize(1100, 700)
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
