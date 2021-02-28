FROM archlinux

RUN pacman -Syu python git python-pip networkmanager --noconfirm

RUN python -m pip install bs4 pythonping docker

RUN systemctl enable NetworkManager

COPY . /mirrors_project
