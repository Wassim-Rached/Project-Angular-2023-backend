#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r requirements.prod.txt

python source/manage.py collectstatic --no-input

python source/manage.py migrate