FROM fedora

COPY . /mirrors_project
WORKDIR /mirrors_project

RUN yum install -y python python3-pip vim

RUN pip install bs4 configparser pythonping argparse docker

#RUN python3 mirrors_manager.py --parser fedora
