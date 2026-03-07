#!/bin/bash

apt-get update && apt-get install -y python3-pip python3 file sqlite3 # python3-dev 
apt-get install -y poppler-utils  # pdftotext

TZ=Etc/UTC 
apt-get -y install tzdata 


# pytest is for debugging
pip3 install gradescope-utils pylint pytest requests Pillow bs4 
python3 -m pip install Django==5.2 django-extensions

# install clients for 3 language generative models 
pip3 install google-genai  cerebras-cloud-sdk openai

