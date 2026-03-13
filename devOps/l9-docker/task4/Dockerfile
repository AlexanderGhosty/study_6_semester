# Этап 1: Подготовка
FROM python:3.14-slim AS builder

WORKDIR /app

COPY app.py .

# Проверяем, что код валиден (компиляция в байткод)
RUN python -m py_compile app.py

# Этап 2: Минимальный runtime
FROM python:3.14-alpine

WORKDIR /app

# Копируем только проверенный файл из builder-этапа
COPY --from=builder /app/app.py .

CMD ["python", "app.py"]