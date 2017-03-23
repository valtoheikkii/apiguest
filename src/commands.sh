#!/usr/bin/env bash

cp ./common/queue_worker.py ./queue_worker.py

python -u queue_worker.py &

gunicorn --config=gunicorn.py guest_service:app

#python -u guest_service.py