#!/bin/bash

echo "Starting Telegram Bot..."
python -m DazaiRobot &

echo "Starting Flask App..."
gunicorn -w 2 -b 0.0.0.0:$PORT app:app

wait
