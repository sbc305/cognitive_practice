FROM python:3.9 AS base

WORKDIR /usr/local/cognitive_app

# prep
FROM base AS core-base
COPY core ./core
ENV PYTHONPATH="/usr/local/cognitive_app/core/"
RUN pip install --no-cache-dir --upgrade -r ./core/requirements.txt

FROM core-base AS backend-base
COPY backend ./backend
RUN pip install --no-cache-dir --upgrade -r backend/requirements.txt
WORKDIR /usr/local/cognitive_app/backend

# Set default values for host and port as environment variables
ENV HOST=0.0.0.0
ENV PORT=8000
EXPOSE ${PORT}
CMD ["sh", "-c", "uvicorn main:app --host $HOST --port $PORT"]

# TODO
# FROM base AS fronted-base
