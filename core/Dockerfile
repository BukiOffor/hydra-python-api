FROM rust:1.67 as builder

FROM python:3.8-slim

RUN apt-get -y update

RUN apt-get install -y sudo


WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]