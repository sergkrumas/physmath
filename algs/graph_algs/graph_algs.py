

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
            raise TypeError('Array elements must me all integers!')

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

    solving_path = []

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

        cls.solving_path.clear()

        def inner_repeat_body():
            nonlocal v
            v = cls.L[v.PrevVertex]
            cls.solving_path.insert(0, v)
            window.memo.setPlainText(f'{v.State} \n{window.memo.toPlainText()}')

        def repeat_body():
            nonlocal HeadIdx, c, v
            v = cls.L[HeadIdx] # v - первый элемент списка
            c += 1

            if cls.IsGoal(v.State): # если текущая вершина является целевой
                window.memo.setPlainText(f'{v.State} \n')

                cls.solving_path.insert(0, v)
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

        cls.solving_path.clear()

        def inner_repeat_body():
            nonlocal v
            v = cls.L2[v.PrevVertex]
            cls.solving_path.insert(0, v)
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

    @classmethod
    def animated_resolution(cls):
        global gtv
        Program.Initialize()
        gtv = GameStateVisualizer(Program.StartingState, Program.solving_path)
        gtv.show()

class GameStateVisualizer(QWidget):

    def prepare_state_for_viz(self, vertex_state):
        number_states = dict()
        for i in range(3):
            for j in range(3):
                value = vertex_state.State[j, i]
                if value == 0:
                    continue
                number_states[value] = (i, j)
        return number_states

    def __init__(self, game_state, solving_path):
        super().__init__()
        self.game_state = game_state
        self.solving_path = solving_path

        self.transitions = []

        self.restart_transition()

        for n, solve_step in enumerate(self.solving_path[:-1]):
            a = self.prepare_state_for_viz(solve_step)
            b = self.prepare_state_for_viz(self.solving_path[n+1])
            self.transitions.append((a, b))


        self.setWindowTitle('Animated Solve Path')

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_handler)
        self.timer.setInterval(100)

    def restart_transition(self):
        self.transition_index = 0
        self.transition_step_factor = 0.0

    def timer_handler(self):
        if not self.animation_tick():
            self.timer.stop()
            self.restart_transition()
            print('ANIMATION DONE')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # self.animation_tick()
            self.timer.start()

    def animation_tick(self):
        self.transition_step_factor += 0.2
        if self.transition_step_factor > 1.0:
            self.transition_step_factor = 0.0
            self.transition_index += 1

        last_index = len(self.transitions)-1
        if self.transition_index > last_index:
            self.transition_index = last_index
            self.transition_step_factor = 1.0
            return False

        self.update()
        return True

    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)


        font = painter.font()
        font.setPixelSize(20)
        painter.setFont(font)


        WIDTH = 50

        def draw_number(highlight=False):
            rect = QRectF(i*WIDTH, j*WIDTH, WIDTH-1, WIDTH-1)

            if highlight:
                bc = QColor(220, 150, 150)
                pc = Qt.black
            else:
                bc = Qt.white
                pc = Qt.gray

            painter.setBrush(QBrush(bc))
            painter.setPen(QPen(pc, 2))

            path = QPainterPath()
            path.addRoundedRect(rect, 5, 5)
            painter.drawPath(path)

            painter.save()
            painter.setPen(QPen(QColor(220, 50, 50)))
            painter.restore()

            painter.drawText(rect, Qt.AlignCenter, str(value))

        if self.transitions:
            current_transiton = self.transitions[self.transition_index]
            factor = self.transition_step_factor
            factor_inv = 1.0 - factor

            a = current_transiton[0]
            b = current_transiton[1]

            for number_key in a.keys():
                a_pos = a[number_key]
                b_pos = b[number_key]

                number_pos = a_pos
                is_moving = a_pos != b_pos
                if is_moving:
                    number_pos = (
                            b_pos[0]*factor+a_pos[0]*factor_inv,
                            b_pos[1]*factor+a_pos[1]*factor_inv
                        )

                i, j = number_pos
                value = number_key
                draw_number(highlight=is_moving)

            status_string = f'{self.transition_index} {self.transition_step_factor:.01f} '

        else:

            for i in range(3):
                for j in range(3):
                    value = self.game_state[j, i]
                    if value == 0:
                        continue
                    draw_number()

            status_string = f'Решение не загружено!'

        painter.drawText(self.rect(), Qt.AlignCenter, status_string)

        painter.end()




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

        show_btn = QPushButton('Animated')
        show_btn.clicked.connect(Program.animated_resolution)

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

        main.addWidget(show_btn)
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
