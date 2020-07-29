#!/bin/bash
set -e

RETRIES=5

case "$1" in
    develop)
        echo "Running Development Server"
        exec python src/main.py
        ;;
    start)
        echo "Running Start"
        exec python src/main.py
        ;;
    *)
        exec "$@"
esac
