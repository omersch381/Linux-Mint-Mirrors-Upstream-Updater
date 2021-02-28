FROM kalilinux/kali-rolling

COPY . /mirrors_project
WORKDIR /mirrors_project

RUN apt-get update
RUN apt-get install python -y
RUN apt-get install pip -y

RUN pip3 install bs4
RUN pip3 install configparser
RUN pip3 install pythonping
RUN pip3 install argparse
RUN pip3 install docker