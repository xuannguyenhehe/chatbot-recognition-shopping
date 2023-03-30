FROM python:3.8-slim-buster
# FROM nvidia-runtime

COPY ./requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install gcc -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt --default-timeout=200
RUN pip install pandas matplotlib
RUN pip install seaborn
# COPY ./yolov5/requirements.txt requirements-yolov5.txt
# RUN pip install --no-cache-dir --upgrade -r requirements-yolov5.txt

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

CMD ["python", "app.py"]
ADD start.sh /
RUN chmod +x /start.sh
CMD ["/start.sh", "8001"]