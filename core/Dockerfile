FROM nikolaik/python-nodejs
USER pn
WORKDIR /home/pn/app

COPY . /home/pn/app/
RUN ls -la /home/pn/app/*
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH /home/pn/.cargo/bin:$PATH

# Install Python dependencies.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/home/pn/app/"


EXPOSE 5000
ENV FLASK_APP=/home/pn/app/app.py
# Specify the command to run on container start
CMD [ "python", "/home/pn/app/app.py" ]