#!/usr/bin/env python3
"""
Лабораторная работа №6: Реализация бутстрапа на Python
Датасет: mtcars (расход топлива автомобилей)
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Установка seed для воспроизводимости
np.random.seed(42)

# Загрузка датасета mtcars
# Данные взяты из R-датасета mtcars
mtcars_data = {
    'mpg': [21.0, 21.0, 22.8, 21.4, 18.7, 18.1, 14.3, 24.4, 22.8, 19.2,
            17.8, 16.4, 17.3, 15.2, 10.4, 10.4, 14.7, 32.4, 30.4, 33.9,
            21.5, 15.5, 15.2, 13.3, 19.2, 27.3, 26.0, 30.4, 15.8, 19.7, 15.0, 21.4],
    'wt': [2.620, 2.875, 2.320, 3.215, 3.440, 3.460, 3.570, 3.190, 3.150, 3.440,
           3.440, 4.070, 3.730, 3.780, 5.250, 5.424, 5.345, 2.200, 1.615, 1.835,
           2.465, 3.520, 3.435, 3.840, 3.845, 1.935, 2.140, 1.513, 3.170, 2.770, 3.570, 2.780]
}
df = pd.DataFrame(mtcars_data)

print("\nДАТАСЕТ: mtcars (Motor Trend Car Road Tests)")
print(f"   Количество наблюдений: {len(df)}")
print(f"   Переменные: mpg (расход топлива, миль/галлон), wt (вес, 1000 фунтов)")

# --- РАЗВЕДОЧНЫЙ АНАЛИЗ ДАННЫХ ---
print("\nРАЗВЕДОЧНЫЙ АНАЛИЗ ДАННЫХ (EDA)")

print("\nОписательная статистика переменной mpg:")
print(df['mpg'].describe())

print(f"\n   90-й перцентиль mpg: {np.quantile(df['mpg'], 0.9):.2f}")

# Создание графиков для EDA
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Гистограмма mpg
axes[0].hist(df['mpg'], bins=8, color='steelblue', edgecolor='white', alpha=0.7)
axes[0].axvline(np.mean(df['mpg']), color='red', linestyle='--', linewidth=2, label=f'Среднее: {np.mean(df["mpg"]):.2f}')
axes[0].axvline(np.quantile(df['mpg'], 0.9), color='green', linestyle='--', linewidth=2, label=f'90-й перцентиль: {np.quantile(df["mpg"], 0.9):.2f}')
axes[0].set_xlabel('Расход топлива (mpg)', fontsize=12)
axes[0].set_ylabel('Частота', fontsize=12)
axes[0].set_title('Распределение расхода топлива', fontsize=14)
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)

# Диаграмма рассеяния mpg vs wt
axes[1].scatter(df['wt'], df['mpg'], color='steelblue', s=80, alpha=0.7, edgecolor='white')
axes[1].set_xlabel('Вес автомобиля (1000 фунтов)', fontsize=12)
axes[1].set_ylabel('Расход топлива (mpg)', fontsize=12)
axes[1].set_title('Зависимость расхода от веса', fontsize=14)
axes[1].grid(alpha=0.3)

# Добавление линии тренда
z = np.polyfit(df['wt'], df['mpg'], 1)
p = np.poly1d(z)
axes[1].plot(sorted(df['wt']), p(sorted(df['wt'])), color='red', linestyle='--', linewidth=2, label='Линия тренда')
axes[1].legend()

plt.tight_layout()
plt.savefig('eda_plots.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nГрафик EDA сохранён: eda_plots.png")


# --- ФУНКЦИЯ БУТСТРАПА ---
def get_percentile_ci(bootstrap_stats, alpha):
    """Строит перцентильный доверительный интервал."""
    left, right = np.quantile(bootstrap_stats, [alpha / 2, 1 - alpha / 2])
    return left, right


# --- БУТСТРАП ДЛЯ 90-ГО ПЕРЦЕНТИЛЯ ---
print("\nБУТСТРАП: ОЦЕНКА 90-ГО ПЕРЦЕНТИЛЯ MPG")

n = len(df['mpg'])
B = 10000  # Количество бутстрап-выборок
alpha = 0.05  # Уровень значимости

values = df['mpg'].values
pe = np.quantile(values, 0.9)  # Точечная оценка

print(f"\nПараметры бутстрапа:")
print(f"   Размер выборки (n): {n}")
print(f"   Количество бутстрап-итераций (B): {B}")
print(f"   Уровень значимости (α): {alpha}")

# Генерация бутстрап-выборок и расчёт статистик
bootstrap_values = np.random.choice(values, (B, n), replace=True)
bootstrap_stats = np.quantile(bootstrap_values, 0.9, axis=1)

# Расчёт доверительного интервала
ci = get_percentile_ci(bootstrap_stats, alpha)

print(f"\nРезультаты:")
print(f"   Точечная оценка 90-го перцентиля: {pe:.2f} mpg")
print(f"   {(1 - alpha) * 100:.0f}% доверительный интервал: ({ci[0]:.2f}, {ci[1]:.2f}) mpg")
print(f"   Стандартная ошибка бутстрапа: {np.std(bootstrap_stats):.2f}")

# --- ВИЗУАЛИЗАЦИЯ БУТСТРАПА ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Гистограмма бутстрап-распределения
axes[0].hist(bootstrap_stats, bins=50, color='steelblue', edgecolor='white', alpha=0.7, density=True)
axes[0].axvline(pe, color='red', linestyle='-', linewidth=2.5, label=f'Точечная оценка: {pe:.2f}')
axes[0].axvline(ci[0], color='green', linestyle='--', linewidth=2, label=f'95% ДИ: ({ci[0]:.2f}, {ci[1]:.2f})')
axes[0].axvline(ci[1], color='green', linestyle='--', linewidth=2)
axes[0].axvspan(ci[0], ci[1], alpha=0.15, color='green')
axes[0].set_xlabel('90-й перцентиль mpg', fontsize=12)
axes[0].set_ylabel('Плотность', fontsize=12)
axes[0].set_title('Бутстрап-распределение 90-го перцентиля', fontsize=14)
axes[0].legend(loc='upper right')
axes[0].grid(axis='y', alpha=0.3)

# Q-Q plot для проверки нормальности
from scipy import stats
stats.probplot(bootstrap_stats, dist="norm", plot=axes[1])
axes[1].set_title('Q-Q plot бутстрап-статистик', fontsize=14)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('bootstrap_results.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nГрафик бутстрапа сохранён: bootstrap_results.png")


# --- СРАВНЕНИЕ ДВУХ ГРУПП (адаптация из 1.md) ---
print("\nБУТСТРАП: СРАВНЕНИЕ ТЯЖЁЛЫХ И ЛЁГКИХ АВТОМОБИЛЕЙ")

# Разделение на группы по весу (медиана)
median_wt = df['wt'].median()
light_cars = df[df['wt'] <= median_wt]['mpg'].values
heavy_cars = df[df['wt'] > median_wt]['mpg'].values

print(f"\nГруппировка по весу (медиана: {median_wt:.2f}):")
print(f"   Лёгкие автомобили (n={len(light_cars)}): wt ≤ {median_wt:.2f}")
print(f"   Тяжёлые автомобили (n={len(heavy_cars)}): wt > {median_wt:.2f}")

pe_diff = np.quantile(light_cars, 0.9) - np.quantile(heavy_cars, 0.9)
print(f"\n   90-й перцентиль mpg лёгких: {np.quantile(light_cars, 0.9):.2f}")
print(f"   90-й перцентиль mpg тяжёлых: {np.quantile(heavy_cars, 0.9):.2f}")
print(f"   Разница: {pe_diff:.2f} mpg")

# Бутстрап для разницы
bootstrap_light = np.random.choice(light_cars, (B, len(light_cars)), replace=True)
bootstrap_heavy = np.random.choice(heavy_cars, (B, len(heavy_cars)), replace=True)

bootstrap_metrics_light = np.quantile(bootstrap_light, 0.9, axis=1)
bootstrap_metrics_heavy = np.quantile(bootstrap_heavy, 0.9, axis=1)
bootstrap_diff = bootstrap_metrics_light - bootstrap_metrics_heavy

ci_diff = get_percentile_ci(bootstrap_diff, alpha)
has_effect = not (ci_diff[0] < 0 < ci_diff[1])

print(f"\nРезультаты бутстрапа для разницы:")
print(f"   Точечная оценка разницы: {pe_diff:.2f} mpg")
print(f"   95% ДИ для разницы: ({ci_diff[0]:.2f}, {ci_diff[1]:.2f}) mpg")
print(f"   Отличия статистически значимые: {'Да' if has_effect else 'Нет'}")

# Визуализация сравнения
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Boxplot сравнения групп
axes[0].boxplot([light_cars, heavy_cars], tick_labels=['Лёгкие\n(wt ≤ медианы)', 'Тяжёлые\n(wt > медианы)'])
axes[0].set_ylabel('Расход топлива (mpg)', fontsize=12)
axes[0].set_title('Сравнение групп по расходу топлива', fontsize=14)
axes[0].grid(axis='y', alpha=0.3)

# Гистограмма разницы
axes[1].hist(bootstrap_diff, bins=50, color='coral', edgecolor='white', alpha=0.7, density=True)
axes[1].axvline(pe_diff, color='red', linestyle='-', linewidth=2.5, label=f'Наблюдаемая разница: {pe_diff:.2f}')
axes[1].axvline(ci_diff[0], color='darkgreen', linestyle='--', linewidth=2, label=f'95% ДИ: ({ci_diff[0]:.2f}, {ci_diff[1]:.2f})')
axes[1].axvline(ci_diff[1], color='darkgreen', linestyle='--', linewidth=2)
axes[1].axvline(0, color='black', linestyle=':', linewidth=2, label='Нулевая гипотеза (0)')
axes[1].axvspan(ci_diff[0], ci_diff[1], alpha=0.15, color='green')
axes[1].set_xlabel('Разница 90-го перцентиля (лёгкие - тяжёлые)', fontsize=12)
axes[1].set_ylabel('Плотность', fontsize=12)
axes[1].set_title('Бутстрап-распределение разницы', fontsize=14)
axes[1].legend(loc='upper left')
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('bootstrap_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nГрафик сравнения сохранён: bootstrap_comparison.png")

significance = "статистически значимо" if has_effect else "статистически не значимо"
direction = "более высокий" if pe_diff > 0 else "более низкий"

print("Все графики сохранены в текущей директории!")
