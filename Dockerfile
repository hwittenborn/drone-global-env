FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get dist-upgrade -y

RUN apt-get install python3 python3-pip -y

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

COPY ./src/ /usr/local/share/drone-global-env/
WORKDIR /usr/local/share/drone-global-env/
ENTRYPOINT ["hypercorn", "main:app", "--bind", "0.0.0.0:8080"]
