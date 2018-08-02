FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    python3-pip \
    python3-wheel \
    python3-setuptools && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN apt-get update && \
    apt-get install -y software-properties-common python-software-properties
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update && \
    apt-get install -y python3.6 python3.6-dev build-essential && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel
ADD requirements.txt .
RUN python3.6 -m pip install -r requirements.txt
