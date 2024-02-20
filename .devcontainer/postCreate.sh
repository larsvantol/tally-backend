#!/bin/bash

pip install --user -r requirements.txt
cd tally
python manage.py migrate
