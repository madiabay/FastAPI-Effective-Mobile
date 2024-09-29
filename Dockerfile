FROM python:3.12-slim

# Установка обновлений и очистка кэша
RUN apt-get update \
    && apt clean \
    && rm -rf /var/cache/apt/*

# Аргументы и переменные окружения
ARG ENV
ENV ENV=${ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1 \
    POETRY_SYNC=1

# Установка зависимостей и Poetry
WORKDIR /tmp
COPY ./poetry.lock ./pyproject.toml /tmp/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install "poetry==$POETRY_VERSION" \
    && pip uninstall -y uvloop \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

# Создание пользователя
RUN useradd -m -d /proj -s /bin/bash app

# Копирование проекта и настройка прав
COPY . /proj
WORKDIR /proj
RUN chown -R app:app /proj/*
COPY ./django.start.sh /start-django
RUN chmod +x /start-django

ADD . /proj/
