FROM python:3.7-slim

# Need git for installing aiomysql
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
        git && \
    apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN python3 -m pip install pipenv
RUN pipenv install --ignore-pipfile --system --deploy

ADD . /code/
WORKDIR /code/

ARG TRAVIS_TAG
ENV VERSION=$TRAVIS_TAG
RUN python3 -m pip install -e .

# Main entrypoint and the default command that will be run
CMD ["/usr/local/bin/python3", "server.py"]

# Game server runs on 8000/tcp, lobby server runs on 8001/tcp, nat echo server runs on 30351/udp
EXPOSE 8000 8001 30351

RUN python3 -V
