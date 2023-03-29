FROM python:3.8-slim-buster
# FROM nvidia-runtime

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app
COPY . /app/backend
COPY setup.py /app

RUN mkdir -p /backend/model
RUN mkdir -p /backend/data

VOLUME /backend/model
VOLUME /backend/data

RUN pip install -e .
WORKDIR /app/backend
# CMD ["python", "app.py"]
# ADD start.sh /
# RUN chmod +x /start.sh
# CMD ["/start.sh", "5050"]