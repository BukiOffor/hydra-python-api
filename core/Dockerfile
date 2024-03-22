FROM rust:1.67 as builder

FROM python:3.8-slim


RUN sudo apt-get install -y python3 make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git && \
    curl https://pyenv.run | bash && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3

ENV HOME /home/admin
ENV PYENV_ROOT $HOME/.pyenv
ENV POETRY_ROOT $HOME/.poetry
ENV CARGO_ROOT /usr/local/cargo
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
ENV PATH $POETRY_ROOT/bin:$PATH
ENV PATH $CARGO_ROOT/bin:$PATH


WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]