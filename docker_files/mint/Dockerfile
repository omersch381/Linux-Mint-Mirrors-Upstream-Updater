FROM linuxmintd/mint19-amd64

COPY . /mirrors_project
WORKDIR /mirrors_project

RUN apt-get update -y

RUN sudo apt-get install -y python3.6 vim
RUN sudo apt install -y python3-pip

RUN pip3 install setuptools
RUN pip3 install bs4 configparser pythonping argparse docker

#RUN python3 mirrors_manager.py --parser mint
