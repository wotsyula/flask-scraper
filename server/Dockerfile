# syntax=docker/dockerfile:1

FROM python:slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get -y upgrade && pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
