#!/bin/bash

set -e

bash -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" || /bin/true
curl https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/templates/zshrc.zsh-template > ~/.zshrc
echo "source ~/.bash_aliases" >> ~/.zshrc

/usr/bin/python3.8 -m venv .venv 
.venv/bin/pip install -r requirements.txt
