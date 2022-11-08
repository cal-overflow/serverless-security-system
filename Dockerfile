FROM python:3.9-slim-buster as base

WORKDIR /app

RUN apt-get update -y && \
    apt-get install ffmpeg libsm6 libxext6 make automake gcc g++ subversion python3-dev -y

# Upgrade to latest pip 
RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
ENTRYPOINT ["python", "src/main.py"]
