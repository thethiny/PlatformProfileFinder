FROM python:3.6-buster

WORKDIR /tmp
COPY requirements.txt .

RUN python -m pip install -r requirements.txt --no-cache-dir

WORKDIR /app

COPY user_ids.py .
COPY app.py .

ENV WORKERS=$(nproc)

ENTRYPOINT [ "gunicorn", "-w", "${WORKERS}", "-b", "0.0.0.0:${PORT}", "app:app" ]