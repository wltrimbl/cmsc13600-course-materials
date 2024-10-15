#!/bin/bash

apt-get update && apt-get install -y python3-pip python3 file # python3-dev 

# pytest is for debugging
pip3 install gradescope-utils pylint pytest django

