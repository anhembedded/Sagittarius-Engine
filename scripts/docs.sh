#!/bin/bash
if [ "$1" = "serve" ]; then
    .venv/bin/python -m mkdocs serve
elif [ "$1" = "build" ]; then
    .venv/bin/python -m mkdocs build --strict
else
    echo "Usage: ./scripts/docs.sh [serve|build]"
fi
