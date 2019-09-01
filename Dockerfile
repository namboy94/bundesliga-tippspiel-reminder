FROM ubuntu:18.04
MAINTAINER Hermann Krumrey <hermann@krumreyh.com>

ENV DEBIAN_FRONTEND=noninteractive

ADD ./ bundesliga-tippspiel-reminder
RUN apt update && \
    apt install locales -y && \
    locale-gen en_US.UTF-8 && update-locale en_US.UTF-8 && \
    apt install -y \
    python3 python3-pip && \
    rm -f /usr/bin/python && \
    rm -f /usr/bin/pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip && \
    cd bundesliga-tippspiel-reminder && \
    python setup.py install

ENTRYPOINT /usr/local/bin/bundesliga-tippspiel-bot -h

ENV LANGUAGE=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_TYPE=en_US.UTF-8
