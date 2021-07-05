# syntax=docker/dockerfile:1

FROM python:slim-buster

WORKDIR /usr/src/server

RUN mkdir Downloads
RUN mkdir Profile
RUN apt-get update && apt-get -y upgrade

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip cache purge

COPY src/server .

EXPOSE 5000

CMD [ "python", "-m" , "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app" ]
