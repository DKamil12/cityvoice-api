# CityVoice API

**CityVoice API** — серверная часть приложения для сбора, обработки и анализа гражданских жалоб и опросов. Система позволяет пользователям отправлять жалобы с указанием местоположения, участвовать в опросах, а также предоставляет административный интерфейс для анализа данных и управления системой.

---

## 📦 Особенности

- **Аутентификация и авторизация**: реализация с использованием JWT (JSON Web Tokens).
- **Модуль жалоб (Reports)**: приём и обработка пользовательских жалоб с возможностью прикрепления изображений и геолокации.
- **Модуль опросов (Surveys)**: проведение опросов среди пользователей и сбор статистики.
- **Модуль аналитики (Charts)**: визуализация данных и статистических показателей.
- **Модуль вознаграждений (Rewards)**: система поощрения активных пользователей с возможностью обмена баллов на товары.
- **Поддержка геоданных**: интеграция с PostGIS для работы с пространственными данными.

---

## 🛠️ Технологии

- **Язык программирования**: Python 3.10+
- **Веб-фреймворк**: Django 4.x
- **База данных**: PostgreSQL с PostGIS
- **Аутентификация**: JWT
- **Хранение файлов**: Amazon S3 или локальное хранилище
- **Документация API**: Swagger / OpenAPI

---

## 🚀 Установка и запуск

### 1️⃣ Клонирование репозитория

```bash
git clone https://github.com/DKamil12/cityvoice-api.git
cd cityvoice-api

### 2️⃣ Создание и активация виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate


### 3️⃣ Установка зависимостей

```bash
pip install -r requirements.txt


### 4️⃣ Настройка переменных окружения
Создайте файл .env в корне проекта и добавьте следующие переменные:

```bash
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://user:password@localhost:5432/cityvoice_db
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name


### 5️⃣ Применение миграций и создание суперпользователя

```bash
python manage.py migrate
python manage.py createsuperuser


### 6️⃣ Запуск сервера разработки

```bash
python manage.py runserver


### 📚 Структура проекта

```bash
cityvoice-api/
├── core/              # Основной модуль Django
│   ├── settings.py         # Настройки проекта
│   ├── urls.py             # Маршруты проекта
│   └── wsgi.py             # WSGI-приложение
├── reports/                # Модуль жалоб
├── surveys/                # Модуль опросов
├── charts/                 # Модуль аналитики
├── rewards/                # Модуль вознаграждений
├── manage.py               # Утилита управления проектом
└── requirements.txt        # Зависимости проекта

