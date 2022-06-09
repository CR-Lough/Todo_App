# syntax=docker/dockerfile:1
FROM python:3.9.6-slim-buster

WORKDIR /core
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY core/ /core/

CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"