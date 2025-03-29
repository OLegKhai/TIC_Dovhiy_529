import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft

n = 500
Fs = 1000
F_max = 11
Dt_values = [2, 4, 8, 16]
F_filter = 18
M_values = [4, 16, 64, 256]

np.random.seed(42)
raw_signal = np.random.normal(0, 10, n)
w = F_max / (Fs / 2)
lowpass_filter = signal.butter(3, w, 'low', output='sos')
filtered_signal = signal.sosfiltfilt(lowpass_filter, raw_signal)

discrete_signals = []
discrete_spectrums = []
restored_signals = []
errors = []
SNR_values = []
quantized_signals = []
quantization_errors = []
quantization_SNR = []

for Dt in Dt_values:
        discrete_signal = np.zeros(n)
        for i in range(0, n, Dt):
                discrete_signal[i] = filtered_signal[i]
        discrete_signals.append(discrete_signal)

        spectrum = fft.fft(discrete_signal)
        discrete_spectrums.append(np.abs(fft.fftshift(spectrum)))

        w_norm = F_filter / (Fs / 2)
        filter_params = signal.butter(3, w_norm, 'low', output='sos')
        restored_signal = signal.sosfiltfilt(filter_params, discrete_signal)
        restored_signals.append(restored_signal)

        error = restored_signal - filtered_signal
        errors.append(np.var(error))
        SNR_values.append(np.var(filtered_signal) / np.var(error))

for M in M_values:
        delta = (np.max(filtered_signal) - np.min(filtered_signal)) / (M - 1)
        quantized_signal = delta * np.round(filtered_signal / delta)
        quantized_signals.append(quantized_signal)

        error = quantized_signal - filtered_signal
        quantization_errors.append(np.var(error))
        quantization_SNR.append(np.var(filtered_signal) / np.var(error))

        # Створення таблиці квантування
        quantize_levels = np.arange(np.min(quantized_signal), np.max(quantized_signal) + delta, delta)
        quantize_bit = np.arange(0, M)
        quantize_bit = [format(bits, '0' + str(int(np.log2(M))) + 'b') for bits in quantize_bit]
        quantize_table = np.c_[quantize_levels[:M], quantize_bit[:M]]

        fig, ax = plt.subplots(figsize=(14/2.54, M/2.54))
        table = ax.table(cellText=quantize_table, colLabels=['Значення сигналу', 'Кодова послідовність'], loc='center')
        table.set_fontsize(14)
        table.scale(1, 2)
        ax.axis('off')
        plt.savefig(f'/IdeaProjects/TIC_Dovhiy_529/SignalProcessing/figures/quantization_table_M_{M}.png', dpi=600)
        plt.close()

        # Створення бітової послідовності
        bits = []
        for signal_value in quantized_signal:
                for index, value in enumerate(quantize_levels[:M]):
                        if np.round(np.abs(signal_value - value), 0) == 0:
                                bits.append(quantize_bit[index])
                                break

        bits_str = ''.join(bits)
        bits_array = [int(item) for item in list(bits_str)]

        # Визначення кількості бітів для відображення
        if M == 4:
                display_bits = 1000
        elif M == 16:
                display_bits = 2000
        elif M == 64:
                display_bits = 3000
        else:
                display_bits = 4000

        plt.figure(figsize=(21/2.54, 14/2.54))
        plt.step(np.arange(0, min(display_bits, len(bits_array))), bits_array[:display_bits], linewidth=0.1)
        plt.xlabel('Біти')
        plt.ylabel('Значення')
        plt.title(f'Бітова послідовність для M={M}')
        plt.savefig(f'/IdeaProjects/TIC_Dovhiy_529/SignalProcessing/figures/bit_sequence_M_{M}.png', dpi=600)
        plt.close()

# Графіки квантованих сигналів
fig, ax = plt.subplots(2, 2, figsize=(14, 10))
for i in range(2):
        for j in range(2):
                idx = i * 2 + j
                ax[i, j].plot(np.arange(n), quantized_signals[idx], label=f'M={M_values[idx]}')
                ax[i, j].set_title(f'Квантування з M={M_values[idx]}')
                ax[i, j].legend()
plt.tight_layout()
plt.savefig('/IdeaProjects/TIC_Dovhiy_529/SignalProcessing/figures/quantized_signals_grid.png', dpi=600)
plt.close()

# Графік залежності дисперсії від рівнів квантування
plt.figure(figsize=(10, 5))
plt.plot(M_values, quantization_errors, marker='o', linestyle='-')
plt.xlabel('Кількість рівнів M')
plt.ylabel('Дисперсія помилки')
plt.title('Залежність дисперсії від рівнів квантування')
plt.savefig('/IdeaProjects/TIC_Dovhiy_529/SignalProcessing/figures/quantization_error_variance.png', dpi=600)
plt.close()

# Графік залежності SNR від рівнів квантування
plt.figure(figsize=(10, 5))
plt.plot(M_values, quantization_SNR, marker='o', linestyle='-')
plt.xlabel('Кількість рівнів M')
plt.ylabel('Співвідношення сигнал-шум')
plt.title('Залежність SNR від рівнів квантування')
plt.savefig('/IdeaProjects/TIC_Dovhiy_529/SignalProcessing/figures/quantization_snr.png', dpi=600)
plt.close()