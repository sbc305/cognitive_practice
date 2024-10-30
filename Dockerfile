FROM python:3.9 AS base

WORKDIR /usr/local/cognitive_app

# prep
FROM base AS core-base
COPY core ./core
ENV PYTHONPATH="/usr/local/cognitive_app/data/"
RUN pip install --no-cache-dir --upgrade -r ./core/requirements.txt

FROM core-base AS backend-base
COPY backend ./backend
RUN pip install --no-cache-dir --upgrade -r backend/requirements.txt

FROM backend-base AS data-base
COPY data ./data

# Set default values for host and port as environment variables
ENV HOST=0.0.0.0
ENV PORT=8000
EXPOSE ${PORT}
CMD ["sh", "-c", "uvicorn backend.main:app --reload --host $HOST --port $PORT"]

# TODO
# FROM base AS fronted-base
