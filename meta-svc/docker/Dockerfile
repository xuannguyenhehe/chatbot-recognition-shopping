# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9

LABEL MAINTAINER="Pham Nguyen Xuan Nguyen <nickpham2808@gmail.com>"

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip

RUN pip install -r requirements.txt --default-timeout=20000
RUN apt-get update
RUN apt-get install -y iputils-ping
RUN apt-get install -y --no-install-recommends libgl1 libglib2.0-0 dos2unix

WORKDIR /meta-service
COPY . /meta-service

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
RUN dos2unix ./entrypoint.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*
RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]