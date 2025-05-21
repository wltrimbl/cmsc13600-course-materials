#!/bin/bash

apt-get update && apt-get install -y python3-pip python3 file sqlite3 
# apt-get install -y  python3-opencv libzbar0 # python3-dev 

TZ=Etc/UTC 
apt-get -y install tzdata 


apt-get install libgl1  

# pytest is for debugging
pip3 install gradescope-utils pylint pytest requests Pillow bs4 
# pip3 install qrcode opencv-python
pip3 install pyzbar 
python3 -m pip install Django==5.2 django-extensions


