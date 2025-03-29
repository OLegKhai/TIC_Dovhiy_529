import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import scipy.signal as signal
import scipy.fft as fft
import matplotlib.pyplot as plt

n = 500
Fs = 1000
F_max = 11
Dt_values = [2, 4, 8, 16]
F_filter = 18

raw_signal = np.random.normal(0, 10, n)
w = F_max / (Fs / 2)
lowpass_filter = signal.butter(3, w, 'low', output='sos')
filtered_signal = signal.sosfiltfilt(lowpass_filter, raw_signal)

discrete_signals = []
discrete_spectrums = []
restored_signals = []
errors = []
SNR_values = []

for Dt in Dt_values:
        discrete_signal = np.zeros(n)
        for i in range(0, n, Dt):
                discrete_signal[i] = filtered_signal[i]
        discrete_signals.append(discrete_signal)

        # Расчет спектра
        spectrum = fft.fft(discrete_signal)
        discrete_spectrums.append(np.abs(fft.fftshift(spectrum)))

        # Фильтрация
        w_norm = F_filter / (Fs / 2)
        filter_params = signal.butter(3, w_norm, 'low', output='sos')
        restored_signal = signal.sosfiltfilt(filter_params, discrete_signal)
        restored_signals.append(restored_signal)

        # Оценка ошибок
        error = restored_signal - filtered_signal
        errors.append(np.var(error))
        SNR_values.append(np.var(filtered_signal) / np.var(error))

fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
for i in range(2):
        for j in range(2):
                idx = i * 2 + j
                ax[i, j].plot(np.arange(n) / Fs, discrete_signals[idx], linewidth=1)
                ax[i, j].set_title(f'Dt = {Dt_values[idx]}')
plt.savefig('/IdeaProjects/TIC_Dovhiy_529/SignalProcessing/figures/discrete_signals.png', dpi=600)

fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
for i in range(2):
        for j in range(2):
                idx = i * 2 + j
                ax[i, j].plot(np.fft.fftshift(np.fft.fftfreq(n, 1/Fs)), discrete_spectrums[idx], linewidth=1)
                ax[i, j].set_title(f'Спектр Dt = {Dt_values[idx]}')
plt.savefig('IdeaProjects/TIC_Dovhiy_529/SignalProcessing/figures/discrete_spectrums.png', dpi=600)

fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
for i in range(2):
        for j in range(2):
                idx = i * 2 + j
                ax[i, j].plot(np.arange(n) / Fs, restored_signals[idx], linewidth=1)
                ax[i, j].set_title(f'Відновлений сигнал Dt = {Dt_values[idx]}')
plt.savefig('IdeaProjects/TIC_Dovhiy_529/SignalProcessing/figures/restored_signals.png', dpi=600)

plt.figure(figsize=(10, 5))
plt.plot(Dt_values, errors, marker='o', linestyle='-')
plt.xlabel('Крок дискретизації')
plt.ylabel('Дисперсія похибки')
plt.savefig('IdeaProjects/TIC_Dovhiy_529/SignalProcessing/figures/error_variance.png', dpi=600)

plt.figure(figsize=(10, 5))
plt.plot(Dt_values, SNR_values, marker='o', linestyle='-')
plt.xlabel('Крок дискретизації')
plt.ylabel('Співвідношення сигнал-шум')
plt.savefig('IdeaProjects/TIC_Dovhiy_529/SignalProcessing/figures/snr.png', dpi=600)

