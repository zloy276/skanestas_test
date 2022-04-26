# Mediasoft CRM Boilerplate

## Установка и запуск

1. Установка:\
   Установка производится с помощью Makefile\
   ```shell
   make build migrate run
   ```

2. Запуск для локальной разработки\
   ```zsh
   uvicorn ./backend/app/main:create_app --factory --reload --bind 0.0.0.0:8000
   ```

## Заметки

1. Alembic:
    - При добавлении новых моделей необходимо проимпортировать их в файле __./alembic/env.py__
    - В конец новых импортов добавить комментарий `# no qa`
    - Пример:\
      ```python
      from backend.app.models.office import Office  # noqa
      ```