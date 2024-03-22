FROM rust:slim-buster
RUN apt-get -y update
RUN apt-get install -y sudo

RUN adduser --disabled-password --gecos '' admin
RUN adduser admin sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN chown -R admin /home/admin

USER admin

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
ENV FLASK_APP=my_flask.py
CMD ["flask", "run", "--host", "0.0.0.0"]