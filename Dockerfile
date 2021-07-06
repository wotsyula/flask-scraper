# syntax=docker/dockerfile:1

FROM python:slim-buster

WORKDIR /usr/src

RUN apt-get update && apt-get -y upgrade

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip cache purge

COPY src .

EXPOSE 5000

CMD [ "python", "-m" , "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "server.app:app" ]
