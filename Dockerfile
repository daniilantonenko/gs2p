FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все необходимые файлы в одну команду
COPY main.py utils.py handlers.py /app/

# Создаем папку для вывода
RUN mkdir -p /app/files

# Устанавливаем переменные окружения
ENV PYTHONPATH=/app

# Запускаем скрипт
CMD ["python", "-u", "/app/main.py"]