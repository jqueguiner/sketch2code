FROM ubuntu:18.04

ENV LANG C.UTF-8

RUN apt-get update -y 

RUN  apt-get install -y python python3.5 python-pip virtualenv

RUN apt-get install -y vim

RUN pip install setuptools pip --upgrade --force-reinstall

RUN apt-get install -y python3-pip

RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender-dev

RUN mkdir -p /src

COPY src /src

WORKDIR /src

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]

RUN  ["app.py"]
