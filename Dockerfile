FROM python:3.6-buster

WORKDIR /tmp
COPY requirements.txt .

RUN python -m pip install -r requirements.txt --no-cache-dir

WORKDIR /app

COPY user_ids.py .
COPY app.py .

ENV WORKERS=$(nproc)

CMD ["sh", "-c", "gunicorn -w ${WORKERS:-1} -b 0.0.0.0:${PORT:-80} app:app"]