from pathlib import Path

import matplotlib

# Headless backend for terminal-only environments.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_digits, load_iris
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.manifold import Isomap
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB


def ensure_output_dir() -> Path:
    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def task_2_1_pairplot(out_dir: Path) -> None:
    print("\n" + "=" * 60)
    print("2.1 Pairplot для датасета Iris")
    print("=" * 60)

    iris = load_iris(as_frame=True)
    iris_df = iris.frame.copy()
    iris_df["species"] = iris.target.map(dict(enumerate(iris.target_names)))
    iris_df = iris_df.drop(columns=["target"])

    g = sns.pairplot(iris_df, hue="species", height=1.8)
    output_path = out_dir / "2_1_iris_pairplot.png"
    g.fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(g.fig)
    print(f"Сохранено: {output_path}")


def task_2_2_linear_regression(out_dir: Path) -> None:
    print("\n" + "=" * 60)
    print("2.2 Линейная регрессия на случайных точках")
    print("=" * 60)

    rng = np.random.RandomState(42)
    x = 10 * rng.rand(50)
    y = 2 * x - 1 + rng.randn(50)

    model = LinearRegression(fit_intercept=True)
    X = x[:, np.newaxis]
    model.fit(X, y)

    xfit = np.linspace(-1, 11, 100)
    Xfit = xfit[:, np.newaxis]
    yfit = model.predict(Xfit)

    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, s=24, label="Случайные точки")
    plt.plot(xfit, yfit, color="red", linewidth=2, label="Линейная аппроксимация")
    plt.title("Линейная регрессия")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()

    output_path = out_dir / "2_2_linear_regression.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Коэффициент: {model.coef_[0]:.4f}")
    print(f"Свободный член: {model.intercept_:.4f}")
    print(f"Сохранено: {output_path}")


def task_2_3_gaussian_nb(out_dir: Path) -> None:
    print("\n" + "=" * 60)
    print("2.3 Наивный Байесов классификатор (Iris)")
    print("=" * 60)

    iris = load_iris(as_frame=True)
    X = iris.data
    y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=1
    )

    model = GaussianNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"Точность GaussianNB на Iris: {acc:.4f}")

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)
    plt.xlabel("Предсказанный класс")
    plt.ylabel("Истинный класс")
    plt.title("Confusion Matrix: Iris + GaussianNB")

    output_path = out_dir / "2_3_iris_gaussiannb_confusion.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Сохранено: {output_path}")


def task_2_4_pca(out_dir: Path) -> None:
    print("\n" + "=" * 60)
    print("2.4 Метод главных компонент (PCA)")
    print("=" * 60)

    iris = load_iris(as_frame=True)
    X = iris.data
    y = iris.target

    model = PCA(n_components=2, random_state=42)
    X_2d = model.fit_transform(X)

    pca_df = pd.DataFrame({
        "PCA1": X_2d[:, 0],
        "PCA2": X_2d[:, 1],
        "species": y.map(dict(enumerate(iris.target_names))),
    })

    plt.figure(figsize=(7, 5))
    sns.scatterplot(data=pca_df, x="PCA1", y="PCA2", hue="species", s=45)
    plt.title("PCA проекция Iris до 2D")

    output_path = out_dir / "2_4_iris_pca.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    explained = model.explained_variance_ratio_
    print(f"Доли объясненной дисперсии: PC1={explained[0]:.4f}, PC2={explained[1]:.4f}")
    print(f"Сохранено: {output_path}")


def task_2_5_digits_load_visualize_reduce(out_dir: Path) -> tuple[np.ndarray, np.ndarray]:
    print("\n" + "=" * 60)
    print("2.5 Загрузка, визуализация и снижение размерности цифр")
    print("=" * 60)

    digits = load_digits()
    X = digits.data
    y = digits.target

    print(f"Форма массива изображений: {digits.images.shape}")
    print(f"Форма матрицы признаков X: {X.shape}")
    print(f"Форма вектора целей y: {y.shape}")

    fig, axes = plt.subplots(10, 10, figsize=(8, 8), subplot_kw={"xticks": [], "yticks": []})
    for i, ax in enumerate(axes.flat):
        ax.imshow(digits.images[i], cmap="binary", interpolation="nearest")
        ax.text(0.05, 0.05, str(digits.target[i]), transform=ax.transAxes, color="green")

    output_grid = out_dir / "2_5_digits_grid.png"
    plt.savefig(output_grid, dpi=150, bbox_inches="tight")
    plt.close(fig)

    iso = Isomap(n_components=2, n_neighbors=10)
    data_projected = iso.fit_transform(X)

    plt.figure(figsize=(8, 6))
    sc = plt.scatter(
        data_projected[:, 0],
        data_projected[:, 1],
        c=y,
        edgecolor="none",
        alpha=0.6,
        cmap=plt.get_cmap("Spectral", 10),
    )
    plt.colorbar(sc, label="digit label", ticks=range(10))
    plt.clim(-0.5, 9.5)
    plt.title("Проекция Digits в 2D (Isomap)")

    output_isomap = out_dir / "2_5_digits_isomap.png"
    plt.savefig(output_isomap, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Сохранено: {output_grid}")
    print(f"Сохранено: {output_isomap}")

    return X, y


def task_2_6_digits_classification(X: np.ndarray, y: np.ndarray, out_dir: Path) -> None:
    print("\n" + "=" * 60)
    print("2.6 Классификация цифр (GaussianNB)")
    print("=" * 60)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )

    model = GaussianNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"Точность на тестовой выборке: {acc:.4f}")

    mat = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(7, 6))
    sns.heatmap(mat, square=True, annot=True, fmt="d", cbar=False, cmap="Blues")
    plt.xlabel("Predicted value")
    plt.ylabel("True value")
    plt.title("Confusion Matrix: Digits + GaussianNB")

    output_path = out_dir / "2_6_digits_confusion_matrix.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Сохранено: {output_path}")


def main() -> None:
    sns.set_theme(style="whitegrid")
    out_dir = ensure_output_dir()

    task_2_1_pairplot(out_dir)
    task_2_2_linear_regression(out_dir)
    task_2_3_gaussian_nb(out_dir)
    task_2_4_pca(out_dir)
    X, y = task_2_5_digits_load_visualize_reduce(out_dir)
    task_2_6_digits_classification(X, y, out_dir)

    print("\nВсе задания 2.1-2.6 выполнены.")


if __name__ == "__main__":
    main()
