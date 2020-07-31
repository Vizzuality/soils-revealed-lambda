#!/bin/bash
set -e

case "$1" in
    develop)
        echo "Running Development Server"
        exec python dev_server.py
        ;;
    start)
        echo "Running Start"
        exec gunicorn -b 0.0.0.0:8000 soils:app
        ;;
    *)
        exec "$@"
esac
