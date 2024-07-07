#!/bin/sh

pyenv activate toy-box

rm -rf oogle-trend-reporting-program.log
nohup python -u main.py > google-trend-reporting-program.log 2>&1 < /dev/null &