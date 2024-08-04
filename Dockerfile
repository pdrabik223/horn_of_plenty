FROM ubuntu:22.04

RUN apt update && apt install tzdata -y

RUN apt-get update && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

ENV TZ="Europe/Warsaw"

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt install gunicorn -y
RUN apt install python3-pip -y
RUN apt install git -y

COPY server ./
RUN pip3 install -r requirements.txt


CMD [ "gunicorn","--timeout", "1200", "-w", "4", "-b", "0.0.0.0:8080", "app:app" ]