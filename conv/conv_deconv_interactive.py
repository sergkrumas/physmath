import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# параметры моделирования
T = 10          # время моделирования
N = 1000        # количество точек

# ось времени
t = np.linspace(0, T, N)
dt = t[1] - t[0]

# функция для расчёта отклика
def rc_response(RC, t_start, t_end, amplitude):
    u = np.where((t >= t_start) & (t <= t_end), amplitude, 0.0)
    h = (1/RC) * np.exp(-t/RC)
    y = np.convolve(u, h) * dt
    t_conv = np.linspace(0, 2*T, 2*N - 1)
    return u, h, y, t_conv

# простая деконволюция через частотную область
def rc_deconvolution(y, h):
    # преобразуем в частотную область
    Y = np.fft.fft(y, n=len(y))
    H = np.fft.fft(h, n=len(y))
    # избегаем деления на ноль
    H[H == 0] = 1e-12
    U_est = Y / H
    u_rec = np.fft.ifft(U_est).real
    return u_rec

# начальные значения
RC0, t_start0, t_end0, amplitude0 = 1.0, 1.0, 4.0, 1.0

# создаём фигуру и оси
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 10))
plt.subplots_adjust(left=0.1, bottom=0.35)

# начальные данные
u, h, y, t_conv = rc_response(RC0, t_start0, t_end0, amplitude0)
u_rec = rc_deconvolution(y, h)

l1, = ax1.plot(t, u, 'b')
ax1.set_title('Прямоугольный входной сигнал')
ax1.grid()

l2, = ax2.plot(t, h, 'r')
ax2.set_title('Импульсная характеристика RC-цепи')
ax2.grid()

l3, = ax3.plot(t_conv, y, 'g')
ax3.set_title('Выходной сигнал (свёртка)')
ax3.grid()

l4, = ax4.plot(t_conv, u_rec, 'm')
ax4.set_title('Оценка входного сигнала (деконволюция)')
ax4.grid()

# размещение слайдеров
axcolor = 'lightgoldenrodyellow'
ax_RC = plt.axes([0.1, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_tstart = plt.axes([0.1, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_tend = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_amp = plt.axes([0.1, 0.10, 0.65, 0.03], facecolor=axcolor)

sRC = Slider(ax_RC, 'RC', 0.1, 5.0, valinit=RC0, valstep=0.1)
ststart = Slider(ax_tstart, 't_start', 0.0, 5.0, valinit=t_start0, valstep=0.1)
stend = Slider(ax_tend, 't_end', 0.0, 10.0, valinit=t_end0, valstep=0.1)
samp = Slider(ax_amp, 'Amplitude', 0.1, 5.0, valinit=amplitude0, valstep=0.1)

# функция обновления
def update(val):
    RC = sRC.val
    t_start = ststart.val
    t_end = stend.val
    amplitude = samp.val
    u, h, y, t_conv = rc_response(RC, t_start, t_end, amplitude)
    u_rec = rc_deconvolution(y, h)

    l1.set_ydata(u)
    l2.set_ydata(h)
    l3.set_xdata(t_conv)
    l3.set_ydata(y)
    l4.set_xdata(t_conv)
    l4.set_ydata(u_rec)

    ax3.relim(); ax3.autoscale_view()
    ax4.relim(); ax4.autoscale_view()
    fig.canvas.draw_idle()

sRC.on_changed(update)
ststart.on_changed(update)
stend.on_changed(update)
samp.on_changed(update)

plt.show()
