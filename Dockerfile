# Используем официальный Python образ
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    binutils libproj-dev gdal-bin gcc python3-dev musl-dev \
    libpq-dev gettext

# Установка рабочей директории
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Установка зависимостей Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Команда запуска 
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
