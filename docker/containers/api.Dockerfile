FROM python:3.8-slim

RUN apt-get update && apt-get install -y gettext

ADD . /starnavi_test

RUN chmod +x /starnavi_test/docker/scripts/api.entrypoint.dev.sh && \
    chmod +x /starnavi_test/docker/scripts/wait-for-it.sh

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /starnavi_test/requirements/dev.txt
