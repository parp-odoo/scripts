#!/bin/bash
BASEDIR=$(dirname "$0")
exec python3 "$BASEDIR/src/main.py" "$@"
