

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

import sys
import time








class GameState(): #состояние игрового поля

    LEN = 9

    def _check_array(self):
        if len(self.array) != self.LEN:
            raise ValueError('Array length must be 9!')
        if not all(map(lambda x: isinstance(x, int), self.array)):
            raise ValueError('Array elements must me all integers!')

    def _check_indexes(self, i, j):
        if i not in self.allowed_indexes or j not in self.allowed_indexes:
            raise IndexError('Index values must be 0, 1 or 2!')

    def __init__(self, init_value=None):
        self.array = [0] * self.LEN
        if init_value is not None:
            if isinstance(init_value, list):
                self.array = init_value
            elif isinstance(init_value, GameState):
                self.array = list(init_value.array)
        self._check_array()
        self.allowed_indexes = (0, 1, 2)

    def __getitem__(self, index):
        i, j = index
        self._check_indexes(i, j)
        value = self.array[3*i+j]
        return value

    def __setitem__(self, index, value):
        i, j = index
        self._check_indexes(i, j)
        self.array[3*i+j] = value

    def __repr__(self):
        return Program.StateToString(self)


class Vertex(): #вершина графа

    def __init__(self):
        self.State = GameState() # соответствующее состояние
        self.PrevVertex = 0 # номер предыдущей вершины на пути к текущей

class AdvancedVertex():

    def __init__(self):
        self.State = GameState() # GameState instance
        self.PrevVertex = 0

        self.Cost = 0
        self.Heuristics = 0
        self.Marked = False


def _generator(what_to_call, i):

    for i in range(i):
        yield what_to_call()

class Program():

    StartingState = GameState() #начальное состояние
    Neighbours = list(_generator(GameState, 4)) #массив соседних состояний
    L = list(_generator(Vertex, 10000)) # список просматриваемых вершин
    L2 = list(_generator(AdvancedVertex, 10000)) # список просматриваемых вершин для эвристической функции
    TailIdx = 0 #указатель на хвост списка

    # !!! автор книги: для упрощения программы, список L описан как массив из 10 000 элементов. Конечно, на практике это решение никуда не годится: для любого более-менее сложного начального расположения кубиков произойдёт выход за границы массива. В реальных приложениях лучше использоваться динамические массивы или связные списки.

    GOAL_CONST = GameState([1, 2, 3, 4, 5, 6, 7, 8, 0, ])

    start_state = [4, 1, 3, 2, 0, 6, 7, 5, 8]

    @staticmethod
    def GridItemToInt(data):
        if data is None:
            return 0
        else:
            try:
                value = int(data.text())
            except:
                value = 0
            return value
 
    @classmethod
    def Initialize(cls):
        for i in range(3):
            for j in range(3):
                cls.StartingState[i, j] = Program.GridItemToInt(window.tw.item(i, j))
        window.memo.setPlainText('')
        # print('starting state', cls.StartingState)

    @classmethod
    def GetNeighbours(cls, s: GameState) -> int: # получение списка соседних вершин графа

        zi = 0
        zj = 0

        di = [-1, 0, 1, 0]
        dj = [0, -1, 0, 1]

        # находим пустую (нулевую) клетку
        # zi, zj - её координаты
        for i in range(3):
            for j in range(3):
                if s[i, j] == 0:
                    zi = i
                    zj = j

        idx = 0 #порядковый номер текущей соседней вершины
        for k in range(4):
            i = zi + di[k] #i, j - координаты клетки, соседней с пустой
            j = zj + dj[k] #(на каждой итерации рассматривается новая)

            # если соседняя клетка находится в пределах поля
            if (i >= 0) and (j >= 0) and (i <= 2) and (j <= 2):
                cls.Neighbours[idx] = GameState(s) #записываем очередной элемент в массив Neighbours.
                cls.Neighbours[idx][i, j] = 0 #пустая клетка меняется местами с соседней
                cls.Neighbours[idx][zi, zj] = s[i, j]
                idx += 1

        return idx # возвращаем количество найденных вершин

        # !!! автор книги: в любой игровой ситуации можно сделать не меньше двух и не больше четырёх различных ходов. Любой ход есть не что иное, как сдвиг пустой ячейки в одну из четырёх сторон - влево, вправо, вверх или вниз. Понятно, что пустая ячейка, расположенная в центре поля, даст больше свободы действий, чем находящаяся в углу.
        # GetNeighbours просматривает по очереди все четыре соседние с пустой клетки и, если ход оказывается допустимым, меняет местами пустую клетку с текущей соседней, тем самым генерируя новую вершину графа.

    @classmethod
    def IsGoal(cls, s: GameState) -> bool: # проверяем, является ли состояние s целевым

        for i in range(3):
            for j in range(3):
                s_value = s[i, j]
                g_value = cls.GOAL_CONST[i, j]

                if s_value != g_value:
                    return False
        return True

    @classmethod
    def StateToString(cls, s: GameState) -> str:
        r = '\n'
        for i in range(3):
            for j in range(3):
                r += f'{s[i, j]} '
            r += '\n'
        return r

    @classmethod
    def do_deep_search(cls): #поиск в ширину
        v = None #текущая исследуемая вершина

        cls.Initialize()
        cls.L[0].State = GameState(cls.StartingState) #вносим в список L стартовую вершину
        cls.L[0].PrevVertex = -1 #предыдущей вершины у стартовой нет
        HeadIdx = 0 #указатель на начало списка L
        cls.TailIdx = 1
        c = 0 #количество уже исследованных вершин

        def inner_repeat_body():
            nonlocal v
            v = cls.L[v.PrevVertex]
            window.memo.setPlainText(f'{v.State} \n{window.memo.toPlainText()}')

        def repeat_body():
            nonlocal HeadIdx, c, v
            v = cls.L[HeadIdx] # v - первый элемент списка
            c += 1

            if cls.IsGoal(v.State): # если текущая вершина является целевой
                window.memo.setPlainText(f'{v.State} \n')

                # шаг за шагом определяем путь от целевой вершины до стартовой,
                # на каждой итерации выводя соответствующее состояние
                inner_repeat_body()
                while (v.PrevVertex != -1):
                    inner_repeat_body()

                window.memo.setPlainText(f'{window.memo.toPlainText()} \nИсследовано состояний: {c}')
                return False

            # определяем соседние вершины и вносим их в список L
            N = cls.GetNeighbours(v.State) # количество соседних состояний
            for i in range(N):
                cls.L[cls.TailIdx].State = GameState(cls.Neighbours[i])
                cls.L[cls.TailIdx].PrevVertex = HeadIdx
                cls.TailIdx += 1

            HeadIdx += 1 #сдвиг головы списка

            return True

        repeat_body()
        while HeadIdx != cls.TailIdx:
            if not repeat_body():
                return

        window.memo.setPlainText(f'Решение не найдено {time.time()}, {c}')

    @classmethod
    def CalculateHeuristics(cls, s: GameState) -> int:
        return cls.CalculateHeuristics2(s)
        # return cls.CalculateHeuristics1(s)

    @classmethod
    def CalculateHeuristics1(cls, s: GameState) -> int:

        # координаты кубиков в целевой позиции. Позиция нулевого кубика не учитывается, потому что это и не кубик вовсе
        def RowOf(n):
            return (n-1) // 3
        def ColOf(n):
            return (n-1) % 3

        r = 0
        for i in range(3):
            for j in range(3):
                if s[i, j] != 0:
                    if (i != RowOf(s[i, j])) and (j != ColOf(s[i, j])):
                        r += 1
        return r

    @classmethod
    def CalculateHeuristics2(cls, s: GameState) -> int: # более умная эвристическая функция
        # [(n, (n-1) // 3, (n-1) % 3) for n in range(1, 9)]
        
        def RowOf(n):
            return (n-1) // 3
        def ColOf(n):
            return (n-1) % 3

        r = 0
        for i in range(3):
            for j in range(3):
                if s[i, j] != 0:
                    # сопоставляем каждой вершине сумму расстояний от каждого кубика до его целевой позиции.
                    # используем здесь так называемое «манхэттенское расстояние».
                    # расстояние (кубик, цель) = Abs(Хкубика-Хцели) + Abs(Yкубика-Yцели)
                    r += abs(RowOf(s[i, j]) - i) + abs(ColOf(s[i, j]) - j)
        return r

    @classmethod
    def GetIndexofNextElement(cls) -> int:
        # определить следующую вершину извлекаемую из списка L2
        Min = 1000000
        idx = 0
        for i in range(cls.TailIdx):
            if (cls.L2[i].Marked == False) and (cls.L2[i].Cost + cls.L2[i].Heuristics < Min):
                idx = i # определяем неотмеченный элемент списка с минимальным значением величины "цена + эвристика"
                Min = cls.L2[i].Cost + cls.L2[i].Heuristics
        return idx
        # автор книги: последовательный просмотр всего списка на каждом шаге алгоритма - решение далеко не лучшее; хорошо оно лишь своей простотой. К сожалению, более скоростные способы организовать работу алгоритма требуют использования и более сложных структур данных, а не простых массивов.

    @classmethod
    def do_A_start_deep_search(cls):

        v = None # текущая исследуемая вершина
        idx = 0 # индекс анализируемого элемента

        cls.Initialize()
        cls.L2[0].State = GameState(cls.StartingState)
        cls.L2[0].PrevVertex = -1
        cls.L2[0].Cost = 0
        # вычисляем эвристику
        cls.L2[0].Heuristics = cls.CalculateHeuristics(GameState(cls.StartingState))
        cls.L2[0].Marked = False

        cls.TailIdx = 1
        c = 0

        def inner_repeat_body():
            nonlocal v
            v = cls.L2[v.PrevVertex]
            window.memo.setPlainText(f'{v.State} \n{window.memo.toPlainText()}')

        def repeat_body():
            nonlocal idx, c, v
            # определяем следующий анализируемый элемент списка
            idx = cls.GetIndexofNextElement()
            v = cls.L2[idx] # извлекаем элемент из списка
            c += 1
            cls.L2[idx].Marked = True #помечаем его как рассмотренный

            if cls.IsGoal(v.State):
                window.memo.setPlainText(f'{v.State} \n')

                inner_repeat_body()
                while (v.PrevVertex != -1):
                    inner_repeat_body()

                window.memo.setPlainText(f'{window.memo.toPlainText()} \nИсследовано состояний: {c}')
                return False

            N = cls.GetNeighbours(v.State)
            for i in range(N):
                cls.L2[cls.TailIdx].State = GameState(cls.Neighbours[i])
                # цена текущей это цена предыдущей вершины плюс вес ребра
                cls.L2[cls.TailIdx].Cost = v.Cost + 1
                cls.L2[cls.TailIdx].Heuristics = cls.CalculateHeuristics(cls.Neighbours[i])
                cls.L2[cls.TailIdx].PrevVertex = idx

                cls.TailIdx += 1


            return True

        repeat_body()
        while cls.TailIdx != 0:
            if not repeat_body():
                return

        window.memo.setPlainText(f'Решение не найдено {time.time()}, {c}')






class Window(QWidget):


    def __init__(self):
        super().__init__()

        tw = self.tw = QTableWidget()


        tw.setRowCount(3)
        tw.setColumnCount(3)

        tw.setMaximumHeight(100)
        tw.setMaximumWidth(150)

        tw.horizontalHeader().setDefaultSectionSize(24)
        tw.verticalHeader().setDefaultSectionSize(24)

        tw.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        tw.verticalHeader().setVisible(False)
        tw.horizontalHeader().setVisible(False)

        # tw.setEditTriggers(QAbstractItemView.NoEditTriggers)

        deepsearch_btn = QPushButton('Поиск в ширину')
        deepsearch_btn.clicked.connect(Program.do_deep_search)

        astar_deepsearch_btn = QPushButton('A*')
        astar_deepsearch_btn.clicked.connect(Program.do_A_start_deep_search)

        memo = self.memo = QPlainTextEdit()

        main = QVBoxLayout(self)
        self.setLayout(main)
        # deepsearch_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        deepsearch_btn.setMinimumHeight(50)
        astar_deepsearch_btn.setMinimumHeight(50)

        main.addWidget(tw)
        secondary = QHBoxLayout()
        main.addLayout(secondary)

        secondary.addWidget(tw)
        secondary.addWidget(deepsearch_btn)
        secondary.addWidget(astar_deepsearch_btn)
        secondary.setAlignment(deepsearch_btn, Qt.AlignTop | Qt.AlignVCenter)
        secondary.setAlignment(astar_deepsearch_btn, Qt.AlignTop | Qt.AlignVCenter)

        main.addWidget(memo)

        tw.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        tw.show()

        for n, v in enumerate(Program.start_state):
            self.tw.setItem(n // 3, n % 3, QTableWidgetItem(str(v)))

        self.setWindowTitle('Игра в 8')


def main():


    global app, window
    app = QApplication(sys.argv)
    window = Window()
    window.resize(500, 900)
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
