FROM python:3.8-slim

RUN pip3 install --upgrade pip==9.0.3 \
    && pip3 install requests


# set working directory
ADD . /app
WORKDIR /app
COPY /app /app


# This is the runtime command for the container
CMD python3 app.py