FROM python:3.9

ENV C_FORCE_ROOT=True
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/backend

WORKDIR /usr/src/backend

COPY . .

RUN mkdir -p /var/log && chown -R 1777 /var/log

RUN apt-get update && apt-get install -y  postgresql-client

RUN pip install --upgrade pip && pip install poetry && pip install -I gunicorn

RUN poetry config virtualenvs.create false && poetry install --no-ansi --no-dev --no-interaction

COPY . .

ENTRYPOINT ["gunicorn", "--config", "./backend/config/gunicorn.conf.py"]
