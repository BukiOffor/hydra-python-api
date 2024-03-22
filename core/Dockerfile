FROM nikolaik/python-nodejs


WORKDIR /app

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
RUN source $HOME/.cargo
ENV PATH ~/.cargo/bin:$PATH


COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]