import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns
from sklearn.datasets import make_blobs, make_moons
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier

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

# Применяем стиль seaborn для красивых графиков
sns.set_theme()

print("="*60)
print("ЗАДАЧА 1.3: Кластеризация методом k-means")
print("="*60)

# Генерация случайно 7 групп точек на плоскости
np.random.seed(42)
XY = []
for i in range(7):
    # n_features=2 - двумерное пространство (X и Y)
    bxy, bc = make_blobs(n_samples=200, centers=1, n_features=2, cluster_std=2)
    XY.append(bxy)

# Исправлен неверный код цвета '#9E955Z' на '#9E955E'
colors = ('#582B5C', '#8CBEB2', '#9E955E', '#F3B562', '#912424', 
          '#5B56D6', '#D185D6', '#408018', '#7B3C19', '#8096BF')

# Вывод исходных точек в ч/б и цветном виде
fig_1 = plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
for i in range(len(XY)):
    plt.scatter(XY[i][:, 0], XY[i][:, 1], c='black', edgecolors='none', s=25)
plt.title('Исходные данные')
plt.xticks([]); plt.yticks([])

plt.subplot(1, 2, 2)
for i in range(len(XY)):
    plt.scatter(XY[i][:, 0], XY[i][:, 1], c=colors[i % len(colors)], edgecolors='none', s=25)
plt.title('Исходные данные в цвете показывают ' + str(len(XY)) + ' кластеров')
plt.xticks([]); plt.yticks([])

print("Построение и сохранение исходных данных...")
save_and_maybe_show(fig_1, "1_3_kmeans_input_data.png")

# Преобразование (reshape) исходных данных к нужному виду
XY_points = []
scatter_x = []
scatter_y = []
for x in XY:
    XY_points.extend(x)
    scatter_x.extend(x[:, 0])
    scatter_y.extend(x[:, 1])

# Выведем результаты кластеризации для разного количества кластеров (от 2 до 10)
print("Обучение k-means для разного числа кластеров (от 2 до 10)...")
fig_2 = plt.figure(figsize=(12, 10))
plt.subplots_adjust(hspace=0.3) # Добавим отступы между графиками

for num_clusters in range(2, 11):
    # Добавлен n_init='auto' для подавления предупреждений (warnings) scikit-learn
    kMeans = KMeans(n_clusters=num_clusters, n_init='auto', random_state=42)
    kMeans.fit(XY_points)
    predictions = kMeans.predict(XY_points)
    
    clrs = [colors[p % len(colors)] for p in predictions]
    
    plt.subplot(3, 3, num_clusters - 1)
    plt.scatter(scatter_x, scatter_y, c=clrs, edgecolors='none', s=7)
    plt.xticks([]); plt.yticks([])
    plt.title(str(num_clusters) + ' clusters')

print("Сохранение результатов k-means...\n")
save_and_maybe_show(fig_2, "1_3_kmeans_clusters_2_10.png")


print("="*60)
print("ЗАДАЧА 1.4: Классификация с помощью нейронной сети (MLPClassifier)")
print("="*60)

# Пример использования MLP
# Обучение на двух простых точках
X_mlp = [[0., 0.], [1., 1.]]
y_mlp = [0, 1]

# Создание и обучение нейросети
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
clf.fit(X_mlp, y_mlp)

print("Обучена простая нейросеть на точках [0,0]->0 и [1,1]->1")

# Предсказание для новых точек
test_points = [[2., 2.], [-1., -2.]]
preds = clf.predict(test_points)
print(f"Предсказание классов (predict) для {test_points}: {preds}")

# Вероятности классов
proba_points = [[2., 2.], [1., 2.]]
probs = clf.predict_proba(proba_points)
print(f"Вероятности классов (predict_proba) для {proba_points}:\n{probs}\n")


# Дополнительно: Демонстрация влияния регуляризации (L2/alpha)
print("Подготовка визуализации влияния параметра регуляризации alpha...")
# Генерируем датасет "луны", который часто используется для демонстрации нелинейной классификации
X_moons, y_moons = make_moons(n_samples=100, noise=0.25, random_state=3)

alphas = [0.01, 1.0, 10.0]
fig_3 = plt.figure(figsize=(15, 4))

for i, alpha in enumerate(alphas):
    # Создаем нейросеть с разной силой штрафа за большие веса (alpha)
    mlp = MLPClassifier(solver='lbfgs', max_iter=1000, random_state=0,
                        hidden_layer_sizes=[10, 10], alpha=alpha)
    mlp.fit(X_moons, y_moons)
    
    # Визуализация разделяющей поверхности
    ax = plt.subplot(1, 3, i + 1)
    
    # Создаем сетку для фона
    x_min, x_max = X_moons[:, 0].min() - .5, X_moons[:, 0].max() + .5
    y_min, y_max = X_moons[:, 1].min() - .5, X_moons[:, 1].max() + .5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))
    
    # Получаем предсказания для сетки
    Z = mlp.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    Z = Z.reshape(xx.shape)
    
    # Рисуем фон (синий/красный)
    cm = plt.cm.RdBu
    cm_bright = ListedColormap(['#FF0000', '#0000FF'])
    ax.contourf(xx, yy, Z, cmap=cm, alpha=.8)
    
    # Рисуем сами точки
    ax.scatter(X_moons[:, 0], X_moons[:, 1], c=y_moons, cmap=cm_bright, edgecolors='k')
    ax.set_title(f"alpha = {alpha}")
    ax.set_xticks(()); ax.set_yticks(())

print("Сохранение графиков регуляризации MLP.")
save_and_maybe_show(fig_3, "1_4_mlp_alpha_regularization.png")