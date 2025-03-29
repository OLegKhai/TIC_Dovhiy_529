import random
from scipy import signal, fft
import matplotlib
import numpy
import scipy
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

n=500
Fs = 1000
r = numpy.random.normal(0, 10, n)

F_max = 11
w = F_max/(Fs/2)
FNCH = scipy.signal.butter(3, w, 'low', output='sos')
fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
filtered_signal = scipy.signal.sosfiltfilt(FNCH, r)
ax.plot(numpy.arange(n)/Fs, filtered_signal
        , linewidth=0.2)
plt.show()

ax.set_xlabel("Час (секунди)", fontsize=14)
ax.set_ylabel("Амплітуда сигналу", fontsize=14)
plt.title("Сигнал з максимальною частотою F_max = 11 Гц", fontsize=14)
spectrum = scipy.fft.fft(filtered_signal)
x2 = numpy.abs(scipy.fft.fftshift(spectrum))
frequencies_within_the_spectrum = scipy.fft.fftfreq(n, 1/n)
y2 = scipy.fft.fftshift(frequencies_within_the_spectrum)
ax.plot(y2, x2, linewidth=0.8)
ax.set_xlabel("Частота (Гц)", fontsize=14)
ax.set_ylabel("Амплітуда спектру", fontsize=14)
plt.title("Спектр з максимальною частотою F_max = 11 Гц", fontsize=14)
plt.show()
