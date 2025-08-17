import numpy as np
import matplotlib.pyplot as plt

# параметры
T = 10          # время моделирования
N = 1000        # количество точек
RC = 1.0        # постоянная времени RC

# ось времени
t = np.linspace(0, T, N)
dt = t[1] - t[0]

# входной прямоугольный сигнал (длительностью 3 сек)
u = np.where((t >= 1) & (t <= 4), 1.0, 0.0)

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
