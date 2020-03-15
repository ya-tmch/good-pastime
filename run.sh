#!/bin/bash

pip install -r requirements.txt

export PYTHONUNBUFFERED=0  

/usr/local/bin/python3.6 /app/run.py