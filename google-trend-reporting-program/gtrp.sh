#!/bin/bash

eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv activate toy-box

rm -rf google-trend-reporting-program.log
nohup python -u main.py > google-trend-reporting-program.log 2>&1 < /dev/null &