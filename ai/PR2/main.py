import os
import random
import sys
from dataclasses import dataclass
from typing import Callable

import numpy as np
import sympy as sp

if "MPLCONFIGDIR" not in os.environ:
    local_cache = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".mplconfig")
    os.makedirs(local_cache, exist_ok=True)
    os.environ["MPLCONFIGDIR"] = local_cache

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6 import QtCore, QtWidgets


@dataclass
class Individual:
    x: float
    y: float = 0.0


@dataclass
class GAParams:
    pop_size: int
    generations: int
    cut_point_prob: float
    crossover_rate: float
    crossover_coeff: float
    mutation_rate: float
    mutation_strength: float


class GeneticOptimizer:
    def __init__(
        self,
        fn: Callable[[np.ndarray], np.ndarray],
        left: float,
        right: float,
        maximize: bool,
        params: GAParams,
    ):
        self.fn = fn
        self.left = left
        self.right = right
        self.maximize = maximize
        self.params = params

    def run(self) -> list[list[Individual]]:
        population = [Individual(random.uniform(self.left, self.right)) for _ in range(self.params.pop_size)]
        history: list[list[Individual]] = []

        for _ in range(self.params.generations):
            self._evaluate(population)
            history.append([Individual(a.x, a.y) for a in population])

            survivors = self._select_survivors(population)
            next_population = [Individual(a.x, a.y) for a in survivors]

            while len(next_population) < self.params.pop_size:
                p1 = self._tournament_pick(survivors)
                p2 = self._tournament_pick(survivors)
                c1, c2 = self._crossover(p1.x, p2.x)
                next_population.append(Individual(self._mutate(c1)))
                if len(next_population) < self.params.pop_size:
                    next_population.append(Individual(self._mutate(c2)))

            population = next_population

        return history

    def _fitness_key(self, item: Individual) -> float:
        return item.y if self.maximize else -item.y

    def _evaluate(self, population: list[Individual]) -> None:
        xs = np.array([a.x for a in population], dtype=float)
        ys = np.asarray(self.fn(xs), dtype=float)
        ys = np.nan_to_num(ys, nan=-1e12 if self.maximize else 1e12, posinf=1e12, neginf=-1e12)
        for i, value in enumerate(ys):
            population[i].y = float(value)

    def _select_survivors(self, population: list[Individual]) -> list[Individual]:
        ranked = sorted(population, key=self._fitness_key, reverse=True)
        keep = max(2, self.params.pop_size // 2)
        return ranked[:keep]

    def _tournament_pick(self, pool: list[Individual], size: int = 3) -> Individual:
        k = min(size, len(pool))
        candidates = random.sample(pool, k=k)
        return max(candidates, key=self._fitness_key)

    def _encode(self, x: float, bits: int = 32) -> int:
        scale = (2**bits - 1) / (self.right - self.left)
        return int(round((x - self.left) * scale))

    def _decode(self, code: int, bits: int = 32) -> float:
        scale = (self.right - self.left) / (2**bits - 1)
        return self.left + code * scale

    def _crossover(self, x1: float, x2: float) -> tuple[float, float]:
        if random.random() > self.params.crossover_rate:
            return self._clip(x1), self._clip(x2)

        if random.random() < self.params.cut_point_prob:
            b1 = f"{self._encode(x1):032b}"
            b2 = f"{self._encode(x2):032b}"
            cut = random.randint(1, 31)
            child1 = int(b1[:cut] + b2[cut:], 2)
            child2 = int(b2[:cut] + b1[cut:], 2)
            return self._clip(self._decode(child1)), self._clip(self._decode(child2))

        alpha = min(1.0, max(0.0, self.params.crossover_coeff))
        child1 = alpha * x1 + (1.0 - alpha) * x2
        child2 = alpha * x2 + (1.0 - alpha) * x1
        return self._clip(child1), self._clip(child2)

    def _mutate(self, x: float) -> float:
        if random.random() > self.params.mutation_rate:
            return self._clip(x)
        spread = (self.right - self.left) * self.params.mutation_strength
        mutated = x + random.gauss(0.0, spread)
        return self._clip(mutated)

    def _clip(self, x: float) -> float:
        return min(self.right, max(self.left, x))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.history: list[list[Individual]] = []
        self.function: Callable[[np.ndarray], np.ndarray] | None = None
        self.left = -10.0
        self.right = 10.0
        self.display_margin = 2.0

        self.setWindowTitle("ГА поиска экстремума функции")
        self.resize(1100, 760)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QtWidgets.QWidget()
        self.setCentralWidget(root)
        layout = QtWidgets.QVBoxLayout(root)

        controls = QtWidgets.QGroupBox("Параметры")
        grid = QtWidgets.QGridLayout(controls)
        layout.addWidget(controls)

        self.function_edit = QtWidgets.QLineEdit("2*x*sin(x)-x/5")
        self.a_edit = QtWidgets.QLineEdit("-10")
        self.b_edit = QtWidgets.QLineEdit("10")
        self.d_edit = QtWidgets.QLineEdit("2")
        self.optimum_box = QtWidgets.QComboBox()
        self.optimum_box.addItems(["максимум", "минимум"])

        self.generations_spin = QtWidgets.QSpinBox()
        self.generations_spin.setRange(1, 500)
        self.generations_spin.setValue(40)

        self.pop_size_spin = QtWidgets.QSpinBox()
        self.pop_size_spin.setRange(4, 1000)
        self.pop_size_spin.setValue(60)

        self.cut_point_spin = QtWidgets.QDoubleSpinBox()
        self.cut_point_spin.setRange(0.0, 1.0)
        self.cut_point_spin.setSingleStep(0.05)
        self.cut_point_spin.setValue(0.5)

        self.crossover_rate_spin = QtWidgets.QDoubleSpinBox()
        self.crossover_rate_spin.setRange(0.0, 1.0)
        self.crossover_rate_spin.setSingleStep(0.05)
        self.crossover_rate_spin.setValue(0.9)

        self.crossover_coeff_spin = QtWidgets.QDoubleSpinBox()
        self.crossover_coeff_spin.setRange(0.0, 1.0)
        self.crossover_coeff_spin.setSingleStep(0.05)
        self.crossover_coeff_spin.setValue(0.5)

        self.mutation_rate_spin = QtWidgets.QDoubleSpinBox()
        self.mutation_rate_spin.setRange(0.0, 1.0)
        self.mutation_rate_spin.setSingleStep(0.01)
        self.mutation_rate_spin.setValue(0.12)

        self.mutation_strength_spin = QtWidgets.QDoubleSpinBox()
        self.mutation_strength_spin.setRange(0.0, 1.0)
        self.mutation_strength_spin.setSingleStep(0.01)
        self.mutation_strength_spin.setValue(0.08)

        row = 0
        grid.addWidget(QtWidgets.QLabel("F(x):"), row, 0)
        grid.addWidget(self.function_edit, row, 1, 1, 5)

        row += 1
        grid.addWidget(QtWidgets.QLabel("A:"), row, 0)
        grid.addWidget(self.a_edit, row, 1)
        grid.addWidget(QtWidgets.QLabel("B:"), row, 2)
        grid.addWidget(self.b_edit, row, 3)
        grid.addWidget(QtWidgets.QLabel("d:"), row, 4)
        grid.addWidget(self.d_edit, row, 5)

        row += 1
        grid.addWidget(QtWidgets.QLabel("Оптимум:"), row, 0)
        grid.addWidget(self.optimum_box, row, 1)
        grid.addWidget(QtWidgets.QLabel("Популяций:"), row, 2)
        grid.addWidget(self.generations_spin, row, 3)
        grid.addWidget(QtWidgets.QLabel("Размер популяции:"), row, 4)
        grid.addWidget(self.pop_size_spin, row, 5)

        row += 1
        grid.addWidget(QtWidgets.QLabel("Вероятность cut-point:"), row, 0)
        grid.addWidget(self.cut_point_spin, row, 1)
        grid.addWidget(QtWidgets.QLabel("Коэф. скрещивания (rate):"), row, 2)
        grid.addWidget(self.crossover_rate_spin, row, 3)
        grid.addWidget(QtWidgets.QLabel("Коэф. скрещивания (alpha):"), row, 4)
        grid.addWidget(self.crossover_coeff_spin, row, 5)

        row += 1
        grid.addWidget(QtWidgets.QLabel("Коэф. мутации (rate):"), row, 0)
        grid.addWidget(self.mutation_rate_spin, row, 1)
        grid.addWidget(QtWidgets.QLabel("Сила мутации:"), row, 2)
        grid.addWidget(self.mutation_strength_spin, row, 3)

        self.start_button = QtWidgets.QPushButton("Старт")
        self.start_button.clicked.connect(self.start_optimization)
        grid.addWidget(self.start_button, row, 5)

        self.figure = Figure(figsize=(9, 5), constrained_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        layout.addWidget(self.canvas, stretch=1)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setEnabled(False)
        self.slider.valueChanged.connect(self.show_generation)
        layout.addWidget(self.slider)

        self.info_label = QtWidgets.QLabel("Введите параметры и нажмите Старт.")
        layout.addWidget(self.info_label)

    def start_optimization(self) -> None:
        try:
            self.left = float(self.a_edit.text().strip())
            self.right = float(self.b_edit.text().strip())
            self.display_margin = float(self.d_edit.text().strip())
            if self.left >= self.right:
                raise ValueError("Требуется A < B.")
            if self.display_margin < 0:
                raise ValueError("Параметр d должен быть >= 0.")

            self.function = self._build_function(self.function_edit.text().strip())
            params = GAParams(
                pop_size=self.pop_size_spin.value(),
                generations=self.generations_spin.value(),
                cut_point_prob=self.cut_point_spin.value(),
                crossover_rate=self.crossover_rate_spin.value(),
                crossover_coeff=self.crossover_coeff_spin.value(),
                mutation_rate=self.mutation_rate_spin.value(),
                mutation_strength=self.mutation_strength_spin.value(),
            )
            maximize = self.optimum_box.currentText() == "максимум"

            optimizer = GeneticOptimizer(self.function, self.left, self.right, maximize, params)
            self.history = optimizer.run()
            if not self.history:
                raise RuntimeError("Не удалось получить поколения.")

            self.slider.setEnabled(True)
            self.slider.setRange(0, len(self.history) - 1)
            self.slider.setValue(0)
            self.show_generation(0)
            self._show_best_result(maximize)
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(exc))

    def _build_function(self, expression: str) -> Callable[[np.ndarray], np.ndarray]:
        if not expression:
            raise ValueError("Поле F(x) не должно быть пустым.")
        x = sp.Symbol("x")
        expr = sp.sympify(expression)
        if expr.free_symbols and expr.free_symbols != {x}:
            raise ValueError("Функция должна зависеть только от x.")
        raw_fn = sp.lambdify(x, expr, modules=["numpy"])

        def wrapped(values: np.ndarray) -> np.ndarray:
            with np.errstate(all="ignore"):
                result = raw_fn(values)
            return np.asarray(result, dtype=float)

        test = wrapped(np.array([self.left, self.right], dtype=float))
        if np.all(~np.isfinite(test)):
            raise ValueError("Функция не определена на границах интервала.")
        return wrapped

    def _show_best_result(self, maximize: bool) -> None:
        all_agents = [item for generation in self.history for item in generation]
        if maximize:
            best = max(all_agents, key=lambda a: a.y)
        else:
            best = min(all_agents, key=lambda a: a.y)
        self.info_label.setText(
            f"Лучший найденный агент: x = {best.x:.6f}, F(x) = {best.y:.6f}. "
            f"Поколений: {len(self.history)}."
        )

    def show_generation(self, generation_index: int) -> None:
        if not self.history or self.function is None:
            return

        generation = self.history[generation_index]
        xs = np.linspace(self.left - self.display_margin, self.right + self.display_margin, 1400)
        ys = self.function(xs)

        self.ax.clear()
        finite_mask = np.isfinite(ys)
        self.ax.plot(xs[finite_mask], ys[finite_mask], color="#1b365d", linewidth=1.8, label="F(x)")

        pop_x = np.array([a.x for a in generation], dtype=float)
        pop_y = np.array([a.y for a in generation], dtype=float)

        maximize = self.optimum_box.currentText() == "максимум"
        order = np.argsort(pop_y)
        if maximize:
            order = order[::-1]

        split_idx = max(1, len(order) // 2)
        best_group = order[:split_idx]
        worst_group = order[split_idx:]
        if worst_group.size == 0:
            worst_group = order[-1:]

        # Draw worst first so best markers stay visible on top.
        self.ax.scatter(
            pop_x[worst_group],
            pop_y[worst_group],
            c="#d62839",
            s=38,
            edgecolors="black",
            linewidths=0.3,
            label="Наименее жизнеспособные",
            zorder=3,
        )
        self.ax.scatter(
            pop_x[best_group],
            pop_y[best_group],
            c="#2d9d3f",
            s=38,
            edgecolors="black",
            linewidths=0.3,
            label="Наиболее жизнеспособные",
            zorder=4,
        )

        self.ax.set_title(f"Поколение {generation_index + 1}/{len(self.history)}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("F(x)")
        self.ax.grid(True, alpha=0.35)
        self.ax.legend(loc="best")
        self.canvas.draw_idle()


def main() -> int:
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
