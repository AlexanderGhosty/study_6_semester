# Этап 1: Установка зависимостей
FROM python:3.14-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Этап 2: Минимальный runtime-образ
FROM python:3.14-slim

WORKDIR /app

# Копируем установленные зависимости из builder-этапа
COPY --from=builder /install /usr/local

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]