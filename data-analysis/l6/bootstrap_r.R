# Установка seed для воспроизводимости
set.seed(42)

# Загрузка библиотеки boot
library(boot)

cat("ДАТАСЕТ: mtcars (Motor Trend Car Road Tests)\n")
cat(sprintf("   Количество наблюдений: %d\n", nrow(mtcars)))
cat(sprintf("   Количество переменных: %d\n", ncol(mtcars)))
cat("\n")

# --- РАЗВЕДОЧНЫЙ АНАЛИЗ ДАННЫХ ---
cat("============================================================\n")
cat("РАЗВЕДОЧНЫЙ АНАЛИЗ ДАННЫХ (EDA)\n")
cat("============================================================\n\n")

cat("Описательная статистика переменной mpg:\n")
print(summary(mtcars$mpg))
cat(sprintf("\n   Стандартное отклонение: %.2f\n", sd(mtcars$mpg)))
cat(sprintf("   90-й перцентиль mpg: %.2f\n", quantile(mtcars$mpg, 0.9)))

cat("\nОписательная статистика переменной wt:\n")
print(summary(mtcars$wt))

# Сохранение EDA графиков
png("eda_plots_r.png", width = 1200, height = 500, res = 150)
par(mfrow = c(1, 2))

# Гистограмма mpg
hist(mtcars$mpg,
  breaks = 8, col = "steelblue", border = "white",
  main = "Распределение расхода топлива",
  xlab = "Расход топлива (mpg)", ylab = "Частота"
)
abline(v = mean(mtcars$mpg), col = "red", lwd = 2, lty = 2)
abline(v = quantile(mtcars$mpg, 0.9), col = "green", lwd = 2, lty = 2)
legend("topright", legend = c(
  sprintf("Среднее: %.2f", mean(mtcars$mpg)),
  sprintf("90%% перцентиль: %.2f", quantile(mtcars$mpg, 0.9))
), col = c("red", "green"), lty = 2, lwd = 2, cex = 0.8)

# Диаграмма рассеяния mpg vs wt
plot(mtcars$wt, mtcars$mpg,
  pch = 19, col = "steelblue", cex = 1.5,
  main = "Зависимость расхода от веса",
  xlab = "Вес автомобиля (1000 фунтов)", ylab = "Расход топлива (mpg)"
)
abline(lm(mpg ~ wt, data = mtcars), col = "red", lwd = 2, lty = 2)
legend("topright", legend = "Линия регрессии", col = "red", lty = 2, lwd = 2, cex = 0.8)
grid()

dev.off()
cat("\nГрафик EDA сохранён: eda_plots_r.png\n")


# --- БУТСТРАП ДЛЯ R-КВАДРАТ ---
cat("\n============================================================\n")
cat("БУТСТРАП: ОЦЕНКА R² РЕГРЕССИИ mpg ~ wt\n")
cat("============================================================\n\n")

# Функция для вычисления R-квадрат
rsq_function <- function(formula, data, indices) {
  d <- data[indices, ] # позволяет выбрать образец
  fit <- lm(formula, data = d) # загрузить регрессионную модель
  return(summary(fit)$r.square) # возвращает результат модели
}

# Исходная регрессия
original_fit <- lm(mpg ~ wt, data = mtcars)
original_rsq <- summary(original_fit)$r.squared

cat(sprintf("Исходная регрессионная модель: mpg ~ wt\n"))
cat(sprintf("   Исходный R²: %.4f\n", original_rsq))
cat(sprintf("   Интерпретация: вес объясняет %.1f%% вариации mpg\n\n", original_rsq * 100))

# Бутстрапируем 2000 раз
B <- 2000
cat(sprintf("Запуск бутстрапа (B = %d итераций)...\n", B))

reps <- boot(
  data = mtcars, statistic = rsq_function, R = B,
  formula = mpg ~ wt
)

# Результаты бутстрапирования
cat("\nРезультаты бутстрапа:\n")
print(reps)

cat(sprintf("\n   Среднее бутстрап R²: %.4f\n", mean(reps$t)))
cat(sprintf("   Стандартная ошибка бутстрапа: %.4f\n", sd(reps$t)))
cat(sprintf("   Смещение (bias): %.4f\n", mean(reps$t) - original_rsq))

# Сохранение графика бутстрапа
png("bootstrap_results_r.png", width = 1000, height = 500, res = 150)
par(mfrow = c(1, 2))
plot(reps)
dev.off()
cat("\nГрафик бутстрапа сохранён: bootstrap_results_r.png\n")

# Рассчитаем доверительный интервал (BCa)
cat("\n")
cat("============================================================\n")
cat("ДОВЕРИТЕЛЬНЫЕ ИНТЕРВАЛЫ\n")
cat("============================================================\n\n")

cat("Доверительные интервалы для R² (уровень 95%):\n\n")
ci_result <- boot.ci(reps, type = c("norm", "basic", "perc", "bca"))
print(ci_result)

# --- БУТСТРАП ДЛЯ ДРУГОЙ РЕГРЕССИИ ---
cat("\n============================================================\n")
cat("БУТСТРАП: ОЦЕНКА R² РЕГРЕССИИ mpg ~ disp\n")
cat("============================================================\n\n")

# Исходная регрессия с disp
original_fit2 <- lm(mpg ~ disp, data = mtcars)
original_rsq2 <- summary(original_fit2)$r.squared

cat(sprintf("Регрессионная модель: mpg ~ disp (объём двигателя)\n"))
cat(sprintf("   Исходный R²: %.4f\n", original_rsq2))

# Бутстрапируем
reps2 <- boot(
  data = mtcars, statistic = rsq_function, R = B,
  formula = mpg ~ disp
)

cat(sprintf("   Среднее бутстрап R²: %.4f\n", mean(reps2$t)))
cat(sprintf("   Стандартная ошибка бутстрапа: %.4f\n", sd(reps2$t)))

ci_result2 <- boot.ci(reps2, type = "bca")
cat("\nBCa 95% ДИ:\n")
print(ci_result2)

# Сохранение сравнительного графика
png("bootstrap_comparison_r.png", width = 1200, height = 500, res = 150)
par(mfrow = c(1, 2))

# Гистограмма R² для mpg ~ wt
hist(reps$t,
  breaks = 30, col = "steelblue", border = "white",
  main = "Бутстрап R² для mpg ~ wt",
  xlab = "R²", ylab = "Частота", xlim = c(0.4, 1)
)
abline(v = original_rsq, col = "red", lwd = 2)
abline(v = quantile(reps$t, c(0.025, 0.975)), col = "green", lwd = 2, lty = 2)
legend("topleft", legend = c(
  sprintf("Исходный R²: %.3f", original_rsq),
  "95% ДИ"
), col = c("red", "green"), lty = c(1, 2), lwd = 2, cex = 0.7)

# Гистограмма R² для mpg ~ disp
hist(reps2$t,
  breaks = 30, col = "coral", border = "white",
  main = "Бутстрап R² для mpg ~ disp",
  xlab = "R²", ylab = "Частота", xlim = c(0.4, 1)
)
abline(v = original_rsq2, col = "red", lwd = 2)
abline(v = quantile(reps2$t, c(0.025, 0.975)), col = "green", lwd = 2, lty = 2)
legend("topleft", legend = c(
  sprintf("Исходный R²: %.3f", original_rsq2),
  "95% ДИ"
), col = c("red", "green"), lty = c(1, 2), lwd = 2, cex = 0.7)

dev.off()
cat("\nГрафик сравнения сохранён: bootstrap_comparison_r.png\n")

cat("\nВсе графики сохранены в текущей директории!\n")
