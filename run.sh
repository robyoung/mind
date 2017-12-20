#!/bin/sh

make migrate

exec gunicorn \
  --config gunicorn.py \
  -b ":8000" \
  application:app
