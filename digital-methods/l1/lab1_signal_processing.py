#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import os

# Создаём директорию для графиков
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

# Настройка стиля графиков
plt.rcParams['figure.figsize'] = [12, 4]
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 100

# 1. Вывод на экран графиков функций
print("\n1. Построение графиков сигнала в разных формах...")

# Создаём ряд временных значений
steps = 50  # Количество отсчётов
t = np.linspace(0, 2 * np.pi, steps)

# Создаём сигнал из набора гармонических колебаний
signal = np.cos(t) + 0.5 * np.cos(3 * t) + 0.25 * np.cos(5 * t)

# Создаём фигуру с тремя графиками
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Аналоговая форма (непрерывный сигнал)
axes[0].plot(t, signal, 'b-', linewidth=2)
axes[0].set_title('Аналоговая форма (plot)', fontsize=12)
axes[0].set_xlabel('Время, t')
axes[0].set_ylabel('Амплитуда')
axes[0].grid(True, alpha=0.3)

# Дискретная форма (stem)
axes[1].stem(t, signal, linefmt='g-', markerfmt='go', basefmt='k-')
axes[1].set_title('Дискретная форма (stem)', fontsize=12)
axes[1].set_xlabel('Время, t')
axes[1].set_ylabel('Амплитуда')
axes[1].grid(True, alpha=0.3)

# Квантованная форма (step)
axes[2].step(t, signal, 'r-', where='post', linewidth=2)
axes[2].set_title('Квантованная форма (step)', fontsize=12)
axes[2].set_xlabel('Время, t')
axes[2].set_ylabel('Амплитуда')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"{output_dir}/01_signal_forms.png", bbox_inches='tight')
plt.close()
print(f"   Сохранено: {output_dir}/01_signal_forms.png")

# Влияние количества отсчётов
steps_list = [10, 25, 50, 100]
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for i, steps in enumerate(steps_list):
    t = np.linspace(0, 2 * np.pi, steps)
    signal = np.cos(t) + 0.5 * np.cos(3 * t) + 0.25 * np.cos(5 * t)
    
    axes[i].stem(t, signal, linefmt='b-', markerfmt='bo', basefmt='k-')
    axes[i].set_title(f'Количество отсчётов: {steps}', fontsize=12)
    axes[i].set_xlabel('Время, t')
    axes[i].set_ylabel('Амплитуда')
    axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"{output_dir}/02_sampling_effect.png", bbox_inches='tight')
plt.close()
print(f"   Сохранено: {output_dir}/02_sampling_effect.png")

steps = 5  # Количество отсчётов для дискретизации

# Исходный аналоговый сигнал (высокое разрешение)
t_analog = np.linspace(0, 2 * np.pi, 1000)
signal_analog = np.cos(t_analog)

# Дискретный сигнал
t_discrete = np.linspace(0, 2 * np.pi, steps)
signal_discrete = np.cos(t_discrete)

# Восстановленный сигнал (интерполяция)
t_reconstructed = np.linspace(0, 2 * np.pi, 1000)
signal_reconstructed = np.interp(t_reconstructed, t_discrete, signal_discrete)

plt.figure(figsize=(12, 5))
plt.plot(t_analog, signal_analog, 'b-', linewidth=2, label='Аналоговый сигнал')
plt.plot(t_discrete, signal_discrete, 'go', markersize=8, label='Дискретные отсчёты')
plt.plot(t_reconstructed, signal_reconstructed, 'r--', linewidth=1.5, label='Восстановленный сигнал')

plt.title(f'Аналоговый, дискретный и восстановленный сигнал (steps = {steps})', fontsize=14)
plt.xlabel('Время, t')
plt.ylabel('Амплитуда')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)
plt.savefig(f"{output_dir}/02b_analog_discrete_reconstructed.png", bbox_inches='tight')
plt.close()
print(f"   Сохранено: {output_dir}/02b_analog_discrete_reconstructed.png")

# 2. Дельта-функция и функция Хевисайда
print("\n2. Дельта-функция и функция Хевисайда...")

# Дельта-функция
n = 50
delta = np.zeros(2 * n)
delta[n] = 1
x_axis = np.arange(-n, n)

plt.figure(figsize=(12, 4))
plt.stem(x_axis, delta, linefmt='b-', markerfmt='bo', basefmt='k-')
plt.title('Дельта-функция (единичный импульс) δ(n)', fontsize=14)
plt.xlabel('n')
plt.ylabel('δ(n)')
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.axvline(x=0, color='k', linewidth=0.5)
plt.xlim(-n, n-1)
plt.ylim(-0.1, 1.2)
plt.savefig(f"{output_dir}/03_delta_function.png", bbox_inches='tight')
plt.close()
print(f"   Сохранено: {output_dir}/03_delta_function.png")

# Функция Хевисайда
x_axis = np.linspace(-n, n, 2 * n + 1)
heaviside = np.heaviside(x_axis, 0.5)

plt.figure(figsize=(12, 4))
plt.stem(x_axis, heaviside, linefmt='g-', markerfmt='go', basefmt='k-')
plt.title('Функция Хевисайда (единичный скачок) H(n)', fontsize=14)
plt.xlabel('n')
plt.ylabel('H(n)')
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.axvline(x=0, color='k', linewidth=0.5)
plt.xlim(-n-1, n+1)
plt.ylim(-0.1, 1.2)
plt.savefig(f"{output_dir}/04_heaviside_function.png", bbox_inches='tight')
plt.close()
print(f"   Сохранено: {output_dir}/04_heaviside_function.png")

# 3. Быстрое преобразование Фурье (БПФ)
print("\n3. Быстрое преобразование Фурье...")

# Параметры сигнала
sampling_rate = 1000  # Частота дискретизации, Гц
duration = 1.0        # Длительность сигнала, с
frequency = 50        # Частота гармонического сигнала, Гц
amplitude = 1.0       # Амплитуда

# Создаём временной ряд
N = int(sampling_rate * duration)
t = np.linspace(0, duration, N, endpoint=False)

# Создаём гармонический сигнал
signal = amplitude * np.sin(2 * np.pi * frequency * t)

# Выполняем БПФ
fft_result = np.fft.fft(signal)
frequencies = np.fft.fftfreq(N, d=1/sampling_rate)
amplitude_spectrum = np.abs(fft_result) / N

# Построение графиков
fig, axes = plt.subplots(1, 2, figsize=(14, 4))

axes[0].plot(t[:200], signal[:200], 'b-', linewidth=1)
axes[0].set_title(f'Гармонический сигнал (f = {frequency} Гц)', fontsize=12)
axes[0].set_xlabel('Время, с')
axes[0].set_ylabel('Амплитуда')
axes[0].grid(True, alpha=0.3)

positive_freqs = frequencies[:N//2]
positive_spectrum = amplitude_spectrum[:N//2] * 2

axes[1].stem(positive_freqs, positive_spectrum, linefmt='r-', markerfmt='ro', basefmt='k-')
axes[1].set_title('Амплитудный спектр', fontsize=12)
axes[1].set_xlabel('Частота, Гц')
axes[1].set_ylabel('Амплитуда')
axes[1].set_xlim(0, 150)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"{output_dir}/05_fft_harmonic.png", bbox_inches='tight')
plt.close()
print(f"   Сохранено: {output_dir}/05_fft_harmonic.png")

# Разные частоты и амплитуды
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

params = [
    (25, 1.0, 'Частота 25 Гц, Амплитуда 1.0'),
    (50, 2.0, 'Частота 50 Гц, Амплитуда 2.0'),
    (100, 0.5, 'Частота 100 Гц, Амплитуда 0.5'),
    (75, 1.5, 'Частота 75 Гц, Амплитуда 1.5')
]

for i, (freq, amp, title) in enumerate(params):
    row, col = i // 2, i % 2
    sig = amp * np.sin(2 * np.pi * freq * t)
    fft_res = np.fft.fft(sig)
    spectrum = np.abs(fft_res) / N * 2
    
    axes[row, col].stem(positive_freqs, spectrum[:N//2], 
                        linefmt='b-', markerfmt='bo', basefmt='k-')
    axes[row, col].set_title(title, fontsize=11)
    axes[row, col].set_xlabel('Частота, Гц')
    axes[row, col].set_ylabel('Амплитуда')
    axes[row, col].set_xlim(0, 150)
    axes[row, col].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"{output_dir}/06_fft_variations.png", bbox_inches='tight')
plt.close()
print(f"   Сохранено: {output_dir}/06_fft_variations.png")

# 4. Спектр суммы гармонических сигналов
print("\n4. Спектр суммы гармонических сигналов...")

# Два сигнала
f1, a1 = 30, 1.0
signal1 = a1 * np.sin(2 * np.pi * f1 * t)

f2, a2 = 70, 0.5
signal2 = a2 * np.sin(2 * np.pi * f2 * t)

signal3 = signal1 + signal2

# БПФ
fft1 = np.fft.fft(signal1)
fft2 = np.fft.fft(signal2)
fft3 = np.fft.fft(signal3)

spectrum1 = np.abs(fft1)[:N//2] / N * 2
spectrum2 = np.abs(fft2)[:N//2] / N * 2
spectrum3 = np.abs(fft3)[:N//2] / N * 2

# Два отдельных спектра
fig, axes = plt.subplots(1, 2, figsize=(14, 4))

axes[0].stem(positive_freqs, spectrum1, linefmt='b-', markerfmt='bo', basefmt='k-')
axes[0].set_title(f'Амплитудный спектр Signal 1 (f = {f1} Гц)', fontsize=12)
axes[0].set_xlabel('Частота, Гц')
axes[0].set_ylabel('Амплитуда')
axes[0].set_xlim(0, 150)
axes[0].set_ylim(0, 1.2)
axes[0].grid(True, alpha=0.3)

axes[1].stem(positive_freqs, spectrum2, linefmt='g-', markerfmt='go', basefmt='k-')
axes[1].set_title(f'Амплитудный спектр Signal 2 (f = {f2} Гц)', fontsize=12)
axes[1].set_xlabel('Частота, Гц')
axes[1].set_ylabel('Амплитуда')
axes[1].set_xlim(0, 150)
axes[1].set_ylim(0, 1.2)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"{output_dir}/07_spectrum_separate.png", bbox_inches='tight')
plt.close()
print(f"   Сохранено: {output_dir}/07_spectrum_separate.png")

# Спектр суммы
plt.figure(figsize=(12, 4))
plt.stem(positive_freqs, spectrum3, linefmt='r-', markerfmt='ro', basefmt='k-')
plt.title(f'Амплитудный спектр Signal 3 = Signal 1 + Signal 2', fontsize=14)
plt.xlabel('Частота, Гц')
plt.ylabel('Амплитуда')
plt.xlim(0, 150)
plt.ylim(0, 1.2)
plt.grid(True, alpha=0.3)
plt.savefig(f"{output_dir}/08_spectrum_sum.png", bbox_inches='tight')
plt.close()
print(f"   Сохранено: {output_dir}/08_spectrum_sum.png")

# 5. Влияние количества гармоник на форму сигнала (эффект Гиббса)
print("\n5. Восстановление прямоугольного сигнала (эффект Гиббса)...")

N = 1024  # Длина сигнала

# Прямоугольный сигнал
rect_signal = np.zeros(N)
rect_signal[128:320] = 1

# БПФ
fft_rect = np.fft.fft(rect_signal)

# Исходный сигнал и спектр
fig, axes = plt.subplots(1, 2, figsize=(14, 4))

axes[0].plot(rect_signal, 'b-', linewidth=1.5)
axes[0].set_title('Исходный прямоугольный сигнал', fontsize=12)
axes[0].set_xlabel('Отсчёты')
axes[0].set_ylabel('Амплитуда')
axes[0].set_ylim(-0.1, 1.2)
axes[0].grid(True, alpha=0.3)

spectrum = np.abs(np.fft.fftshift(fft_rect)) / N
freq_axis = np.fft.fftshift(np.fft.fftfreq(N))

axes[1].plot(freq_axis, spectrum, 'r-', linewidth=1)
axes[1].set_title('Амплитудный спектр прямоугольного сигнала', fontsize=12)
axes[1].set_xlabel('Нормированная частота')
axes[1].set_ylabel('Амплитуда')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"{output_dir}/09_rect_signal_spectrum.png", bbox_inches='tight')
plt.close()
print(f"   Сохранено: {output_dir}/09_rect_signal_spectrum.png")


def reconstruct_signal(fft_data, num_harmonics):
    """Восстанавливает сигнал из заданного количества гармоник."""
    N = len(fft_data)
    fft_filtered = np.zeros(N, dtype=complex)
    fft_filtered[:num_harmonics] = fft_data[:num_harmonics]
    fft_filtered[-num_harmonics:] = fft_data[-num_harmonics:]
    return np.fft.ifft(fft_filtered).real


# Восстановление из разного количества гармоник
harmonics_list = [4, 16, 32, 128, 256, N//2]

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()

for i, num_harm in enumerate(harmonics_list):
    reconstructed = reconstruct_signal(fft_rect, num_harm)
    
    axes[i].plot(rect_signal, 'b-', linewidth=2, alpha=0.3, label='Исходный')
    axes[i].plot(reconstructed, 'r-', linewidth=1, label='Восстановленный')
    axes[i].set_title(f'Количество гармоник: {num_harm}', fontsize=11)
    axes[i].set_xlabel('Отсчёты')
    axes[i].set_ylabel('Амплитуда')
    axes[i].set_ylim(-0.3, 1.3)
    axes[i].legend(loc='upper right', fontsize=8)
    axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"{output_dir}/10_gibbs_effect.png", bbox_inches='tight')
plt.close()
print(f"   Сохранено: {output_dir}/10_gibbs_effect.png")

print("\nВсе графики сохранены в директории:", output_dir)

