import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import pycountry
from mpl_toolkits.mplot3d import Axes3D

# Размер шрифта для подписей на графиках
PLOT_LABEL_FONT_SIZE = 14


# Функция генерации списка цветов для графиков
def getColors(n):
    COLORS = []
    cm = plt.cm.get_cmap('hsv', n)
    for i in np.arange(n):
        COLORS.append(cm(i))
    return COLORS


# Функция установки размера графика
def set_plot_size(w, h, figure=plt):
    fig_size = plt.rcParams['figure.figsize']
    fig_size[0] = 12
    fig_size[1] = 4.5
    figure.rcParams['figure.figsize'] = fig_size


# Устанавливаем размер графиков
set_plot_size(12, 4.5)


# Функция сортировки словаря по значению (по убыванию)
def dict_sort(my_dict):
    keys = []
    values = []
    my_dict = sorted(my_dict.items(), key=lambda x: x[1], reverse=True)
    for k, v in my_dict:
        keys.append(k)
        values.append(v)
    return (keys, values)


# Чтение данных из CSV-файла
df = pd.read_csv('./content/scrubbed.csv', escapechar='`', low_memory=False)
df.fillna(value='unknown')

# Подсчет количества наблюдений по форме объекта
shapes_label_count = pd.value_counts(df['shape'].values, sort=True)

# Подсчет количества наблюдений по странам
country_count = pd.value_counts(df['country'].values, sort=True)
country_count_keys, country_count_values = dict_sort(dict(country_count))

# Визуализация количества наблюдений по странам
TOP_COUNTRY = len(country_count_keys)
plt.title('Страны, где больше всего наблюдений', fontsize=PLOT_LABEL_FONT_SIZE)
plt.bar(np.arange(TOP_COUNTRY), country_count_values, color=getColors(TOP_COUNTRY))
plt.xticks(np.arange(TOP_COUNTRY), country_count_keys, rotation=0, fontsize=12)
plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
plt.ylabel('Количество наблюдений', fontsize=PLOT_LABEL_FONT_SIZE)
plt.show()

# Подсчет количества наблюдений по типам объектов
shapes_type_count = pd.value_counts(df['shape'].values, sort=True)
shapes_type_count_keys, shapes_type_count_values = dict_sort(dict(shapes_type_count))

# Визуализация количества наблюдений по типам объектов
OBJECT_COUNT = len(shapes_type_count_keys)
plt.title('Типы объектов', fontsize=PLOT_LABEL_FONT_SIZE)
bar = plt.bar(np.arange(OBJECT_COUNT), shapes_type_count_values, color=getColors(OBJECT_COUNT))
plt.xticks(np.arange(OBJECT_COUNT), shapes_type_count_keys, rotation=90, fontsize=PLOT_LABEL_FONT_SIZE)
plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
plt.ylabel('Сколько раз видели', fontsize=PLOT_LABEL_FONT_SIZE)
plt.show()

# Подсчет частоты появления объектов по месяцам
MONTH_COUNT = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
MONTH_LABEL = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
               'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

for i in df['datetime']:
    m, d, y_t = i.split('/')
    MONTH_COUNT[int(m) - 1] = MONTH_COUNT[int(m) - 1] + 1

# Визуализация частоты появления объектов по месяцам
plt.bar(np.arange(12), MONTH_COUNT, color=getColors(12))
plt.xticks(np.arange(12), MONTH_LABEL, rotation=90, fontsize=PLOT_LABEL_FONT_SIZE)
plt.ylabel('Частота появления', fontsize=PLOT_LABEL_FONT_SIZE)
plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
plt.title('Частота появления объектов по месяцам', fontsize=PLOT_LABEL_FONT_SIZE)
plt.show()

# Подсчет среднего времени появления каждого объекта (в часах)
shapes_durations_dict = {}
for i in shapes_type_count_keys:
    dfs = df[['duration (seconds)', 'shape']].loc[df['shape'] == i]
    shapes_durations_dict[i] = dfs['duration (seconds)'].mean(axis=0) / 60.0 / 60.0

shapes_durations_dict_keys = []
shapes_durations_dict_values = []
for k in shapes_type_count_keys:
    shapes_durations_dict_keys.append(k)
    shapes_durations_dict_values.append(shapes_durations_dict[k])

# Визуализация среднего времени появления объектов
plt.title('Среднее время появление каждого объекта', fontsize=PLOT_LABEL_FONT_SIZE)
plt.bar(np.arange(OBJECT_COUNT), shapes_durations_dict_values, color=getColors(OBJECT_COUNT))
plt.xticks(np.arange(OBJECT_COUNT), shapes_durations_dict_keys, rotation=90, fontsize=PLOT_LABEL_FONT_SIZE)
plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
plt.ylabel('Среднее время появления в часах', fontsize=PLOT_LABEL_FONT_SIZE)
plt.show()

shapes_durations_dict = {}
for i in shapes_type_count_keys:
    dfs = df[['duration (seconds)', 'shape']].loc[df['shape'] == i]
    shapes_durations_dict[i] = dfs['duration (seconds)'].median(axis=0) / 60.0 / 60.0

# Подсчет медианного времени появления каждого объекта (в часах)
shapes_durations_dict_keys = []
shapes_durations_dict_values = []
for k in shapes_type_count_keys:
    shapes_durations_dict_keys.append(k)
    shapes_durations_dict_values.append(shapes_durations_dict[k])

# Визуализация медианного времени появления объектов
plt.title('Медианное время появление каждого объекта', fontsize=PLOT_LABEL_FONT_SIZE)
plt.bar(np.arange(OBJECT_COUNT), shapes_durations_dict_values, color=getColors(OBJECT_COUNT))
plt.xticks(np.arange(OBJECT_COUNT), shapes_durations_dict_keys, rotation=90, fontsize=PLOT_LABEL_FONT_SIZE)
plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
plt.ylabel('Среднее время появления в часах', fontsize=PLOT_LABEL_FONT_SIZE)
plt.show()
