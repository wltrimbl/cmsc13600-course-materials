#!/bin/bash

apt-get update && apt-get install -y python3-pip python3 file sqlite3 python3-opencv libzbar0 # python3-dev 

TZ=Etc/UTC 
apt-get -y install tzdata 


# pytest is for debugging
pip3 install gradescope-utils pylint pytest requests Pillow bs4 qrcode 
pip3 install pyzbar    # having some problems with this 
python3 -m pip install Django==5.1
