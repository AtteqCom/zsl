FROM ubuntu:18.04

ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=1000

ENV USERNAME=${USERNAME} \
    USER_UID=${USER_UID} \
    USER_GID=${USER_GID}

RUN groupadd --gid $USER_GID $USERNAME \
    && groupadd --gid 999 docker \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && usermod -a -G docker $USERNAME \
    && mkdir -p /home/$USERNAME/.vscode-server /home/$USERNAME/.vscode-server-insiders \
    && chown ${USER_UID}:${USER_GID} /home/$USERNAME/.vscode-server* \
    && apt-get update \
    && apt-get install -y build-essential curl git iproute2 locales net-tools vim software-properties-common sudo zsh \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

RUN sudo add-apt-repository ppa:deadsnakes/ppa \
  && sudo apt-get update \
  && sudo apt-get install -y python3.5 python3.6 python3.7 python3.8 python3-venv python3.5-venv python3.6-venv \
    python3.7-venv python3.8-venv python3.5-dev python3.6-dev python3.7-dev python3.8-dev

WORKDIR /zsl
RUN mkdir -p /zsl/.devcontainer
ADD ./install.sh /zsl/.devcontainer/

ENV SHELL=/bin/zsh
CMD zsh
