# Dockerfile
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Устанавливаем переменные окружения (опционально, если используем .env, можно удалить)
# ENV BOT_TOKEN=ваш_токен
# ENV ADMIN_IDS=ваш_id

# Команда запуска бота
CMD ["python", "bot/main.py"]
