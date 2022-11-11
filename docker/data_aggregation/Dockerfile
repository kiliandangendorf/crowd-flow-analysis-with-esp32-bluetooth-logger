FROM python:3.6-buster

RUN apt-get update \
    && apt-get -yy install libmariadb-dev

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

VOLUME /files
WORKDIR /files

CMD [ "python", "./main.py"]

