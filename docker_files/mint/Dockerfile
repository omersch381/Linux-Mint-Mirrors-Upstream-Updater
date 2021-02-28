FROM linuxmintd/mint19-amd64

COPY . /mirrors_project
WORKDIR /mirrors_project

RUN sudo apt-get install -y python3.6
RUN sudo apt install -y python3-pip
RUN pip3 install setuptools
RUN pip3 install bs4
RUN pip3 install configparser
RUN pip3 install pythonping
RUN pip3 install argparse
RUN pip3 install docker

RUN apt-get install -y vim
RUN apt-get update -y