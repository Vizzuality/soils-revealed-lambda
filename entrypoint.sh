#!/bin/bash
set -e

case "$1" in
    develop)
        echo "Running Development Server"
        exec python dev_server.py
        ;;
    start)
        echo "Running Start"
        exec gunicorn --config=./gunicorn.py soils:app
        ;;
    *)
        exec "$@"
esac
