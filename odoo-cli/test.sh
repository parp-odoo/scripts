#!/bin/bash
BASEDIR=$(dirname "$0")
exec python3 "$BASEDIR/src/run_tests.py" "$@"
