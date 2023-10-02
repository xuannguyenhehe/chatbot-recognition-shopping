FROM python:3.9

LABEL MAINTAINER="Pham Nguyen Xuan Nguyen <nickpham2808@gmail.com>"

EXPOSE 8004
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
COPY requirements/build.txt .
COPY requirements/runtime.txt .
COPY requirements/tests.txt .
RUN pip install -r requirements.txt
RUN pip install -r build.txt
RUN pip install -r runtime.txt
RUN pip install -r tests.txt

RUN apt-get update
RUN apt-get install -y iputils-ping
RUN apt-get install -y --no-install-recommends libgl1 libglib2.0-0 dos2unix

WORKDIR /mmfashion
COPY . /mmfashion

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
RUN dos2unix ./entrypoint.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*
RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]