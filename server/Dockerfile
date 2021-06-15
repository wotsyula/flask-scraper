# syntax=docker/dockerfile:1

FROM python:slim-buster

WORKDIR /usr/src/server

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get -y upgrade

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "-m" , "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app" ]
