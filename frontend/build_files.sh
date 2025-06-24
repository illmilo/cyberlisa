#!/bin/bash
echo "BUILD START"
python3 -m pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py collectstatic --noinput --clear
python3 create_admin.py
echo "BUILD END"