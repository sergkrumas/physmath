import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import interactive
from IPython.display import display

# параметры моделирования
T = 10          # время моделирования
N = 1000        # количество точек

# ось времени
t = np.linspace(0, T, N)
dt = t[1] - t[0]

# функция для моделирования
def rc_response(RC=1.0, t_start=1.0, t_end=4.0, amplitude=1.0):
    # входной прямоугольный сигнал
    u = np.where((t >= t_start) & (t <= t_end), amplitude, 0.0)

    # импульсная характеристика RC-цепи: h(t) = (1/RC) * exp(-t/RC) * u(t)
    h = (1/RC) * np.exp(-t/RC)

    # свёртка (учитываем dt для правильной амплитуды)
    y = np.convolve(u, h) * dt

    # ось времени для результата
    t_conv = np.linspace(0, 2*T, 2*N - 1)

    # построение графиков
    plt.figure(figsize=(12, 8))

    plt.subplot(3,1,1)
    plt.plot(t, u, 'b')
    plt.title('Прямоугольный входной сигнал')
    plt.grid()

    plt.subplot(3,1,2)
    plt.plot(t, h, 'r')
    plt.title('Импульсная характеристика RC-цепи')
    plt.grid()

    plt.subplot(3,1,3)
    plt.plot(t_conv, y, 'g')
    plt.title('Выходной сигнал (свёртка)')
    plt.grid()

    plt.tight_layout()
    plt.show()

# интерактивные ползунки
widget = interactive(rc_response, 
                     RC=widgets.FloatSlider(value=1.0, min=0.1, max=5.0, step=0.1),
                     t_start=widgets.FloatSlider(value=1.0, min=0.0, max=5.0, step=0.1),
                     t_end=widgets.FloatSlider(value=4.0, min=0.0, max=10.0, step=0.1),
                     amplitude=widgets.FloatSlider(value=1.0, min=0.1, max=5.0, step=0.1))
display(widget)
