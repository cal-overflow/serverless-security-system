# FROM python:3.9-alpine3.15 as base
FROM python:3.9-slim-buster as base

# ENV PYTHONFAULTHANDLER=1 \
#     PYTHONHASHSEED=random \
#     PYTHONBUFFERED=1

WORKDIR /app

# ENV PIP_NO_CACHE_DIR=off \
#   PIP_DISABLE_PIP_VERSION_CHECK=on \
#   PIP_DEFAULT_TIMEOUT=100

COPY requirements.txt requirements.txt

# RUN apk add --no-cache gcc g++ musl-dev libffi-dev
RUN pip3 install -r requirements.txt

# Install FFMPEG - TODO - uncomment
# RUN apk add --no-cache ffmpeg

COPY . .
ENTRYPOINT ["python", "src/main.py"]
