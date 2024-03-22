FROM rust:slim-buster

FROM python:3.7-slim

RUN apt-get -y update

RUN apt-get install -y sudo


WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
RUN pip install iop-python
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]