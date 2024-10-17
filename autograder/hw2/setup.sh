#!/bin/bash

apt-get update && apt-get install -y python3-pip python3 file python-bs4 # python3-dev 

TZ=Etc/UTC 
apt-get -y install tzdata


# pytest is for debugging
pip3 install gradescope-utils pylint pytest django requests
pip install -r /autograder/source/requirements.txt

