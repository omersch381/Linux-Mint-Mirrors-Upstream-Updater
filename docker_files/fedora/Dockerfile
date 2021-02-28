FROM fedora

COPY . /mirrors_project
WORKDIR /mirrors_project

RUN yum install -y python

RUN pip install bs4
RUN pip install configparser
RUN pip install pythonping
RUN pip install argparse
RUN pip install docker