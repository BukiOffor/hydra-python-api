FROM nikolaik/python-nodejs







WORKDIR /app

RUN curl --proto '=https' --tlsv1.2 -sSf -y https://sh.rustup.rs | sh
ENV PATH /app/.cargo/bin:$PATH


COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]