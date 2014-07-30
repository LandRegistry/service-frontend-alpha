#!/bin/bash

source ./environment.sh

set +o errexit
createuser -s landregistry
createdb -U landregistry -O landregistry landregistry_users -T template0

python manage.py db upgrade
python run_dev.py
