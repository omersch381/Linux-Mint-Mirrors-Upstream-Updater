FROM archlinux

COPY . /mirrors_project
WORKDIR /mirrors_project

RUN pacman -Syu python git python-pip networkmanager vim --noconfirm

RUN pip3 install setuptools configparser bs4 pythonping docker argparse

RUN systemctl enable NetworkManager

#RUN python mirrors_manager.py --parser arch
