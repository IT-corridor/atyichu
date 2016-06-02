#!/bin/bash

NAME=atyichu
BASEDIR =/home/django
ENVDIR="${BASEDIR}/venv"
DJANGODIR="${BASEDIR}/${NAME}/businesscenter"
SOCKFILE="/tmp/${NAME}.sock"
NUM_WORKERS=3
DJANGO_WSGI_MODULE="${NAME}.wsgi"
GUNICORN=gunicorn

cd $DJANGODIR
source "${ENVDIR}/bin/activate"

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR
exec $GUNICORN "${DJANGO_WSGI_MODULE}:application" \
  --env DJANGO_SETTINGS_MODULE=settings.production_test \
  --workers $NUM_WORKERS \
  --bind "unix:${SOCKFILE}" \

