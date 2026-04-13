import numpy as np
import math
import os
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SHOW_PLOTS = bool(os.environ.get("DISPLAY"))


def save_and_maybe_show(fig, filename):
    output_path = OUTPUT_DIR / filename
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"График сохранен: {output_path}")
    if SHOW_PLOTS and plt.get_backend().lower() != "agg":
        plt.show()
    else:
        plt.close(fig)

print("="*50)
print("ЗАДАЧА 1: Регрессия по случайным точкам (Ridge)")
print("="*50)

# Создание объекта
ridge_estimator = Ridge()

# Генерация случайных точек у подъема синусоиды
np.random.seed(42)
num_pts = 100 # количество точек
noise_range = 0.2 # небольшой шум

x_vals = []
y_vals = []
(x_left, x_right) = (-2, 2)

for i in range(num_pts):
    x = np.random.uniform(x_left, x_right)
    y = np.random.uniform(-noise_range, noise_range) + (2*math.sin(x))
    x_vals.append(x)
    y_vals.append(y)

# Переформатирование наших данных x_vals в столбец
x_column = np.reshape(x_vals, [len(x_vals), 1])

# Обучение с fit()
print("Обучение модели Ridge...")
ridge_estimator.fit(x_column, y_vals)

# Предсказание с predict()
# Получаем предсказания для крайних точек, чтобы построить прямую
y_left = ridge_estimator.predict(np.array([[x_left]]))
y_right = ridge_estimator.predict(np.array([[x_right]]))

print(f"Предсказанное значение y для левого края (x={x_left}): {y_left[0]:.2f}")
print(f"Предсказанное значение y для правого края (x={x_right}): {y_right[0]:.2f}")

# Визуализация. Используем matplotlib
print("Построение и сохранение графика...")
fig = plt.figure(figsize=(10,4))

# Первый график: Исходные данные
plt.subplot(1, 2, 1)
plt.scatter(x_vals, y_vals, s=20)
plt.title('original data')

# Второй график: Данные с линией регрессии
plt.subplot(1, 2, 2)
plt.scatter(x_vals, y_vals, s=20)
# Используем y_left[0] и y_right[0] для извлечения скалярных значений из массива предсказаний
plt.plot([x_left, x_right], [y_left[0], y_right[0]], color='#ff0000', linewidth=3)
plt.title('data with best line')

# Сохраняем график и показываем его только в интерактивной среде
save_and_maybe_show(fig, "1_1_ridge_regression.png")


print("\n" + "="*50)
print("ЗАДАЧА 2: Классификация (predict, decision_function, predict_proba)")
print("="*50)

# Создаем случайный датасет для бинарной классификации (2 класса)
X, y = make_classification(n_samples=100, n_features=2, n_informative=2, n_redundant=0, random_state=42)

# Выберем классификатор из списка (Логистическая регрессия)
classifier = LogisticRegression()

# Обучаем модель
classifier.fit(X, y)

# Возьмем одну случайную выборку (объект) из наших данных для теста
# X[0:1] возвращает 2D массив, что требует scikit-learn
sample = X[0:1] 
true_class = y[0]

print(f"Истинный класс выборки: {true_class}\n")

# Метод predict() - возвращает конкретный класс
pred_class = classifier.predict(sample)
print("1. Метод predict():")
print(f"   Результат: {pred_class[0]} (Модель считает, что это класс {pred_class[0]})")
print("-" * 30)

# Метод decision_function() - возвращает "доверительную" оценку (расстояние до разделяющей гиперплоскости)
# Положительное значение - класс 1, отрицательное - класс 0. Чем больше по модулю, тем выше уверенность.
decision_score = classifier.decision_function(sample)
print("2. Метод decision_function():")
print(f"   Результат (score): {decision_score[0]:.4f}")
print("   (Оценка степени уверенности классификатора)")
print("-" * 30)

# Метод predict_proba() - возвращает вероятности принадлежности к каждому классу (в сумме дают 1)
probabilities = classifier.predict_proba(sample)
print("3. Метод predict_proba():")
print(f"   Вероятность принадлежности к классу 0: {probabilities[0][0]:.4f} ({(probabilities[0][0]*100):.1f}%)")
print(f"   Вероятность принадлежности к классу 1: {probabilities[0][1]:.4f} ({(probabilities[0][1]*100):.1f}%)")
print("   (Как видим, сумма вероятностей равна 1)")
print("="*50)