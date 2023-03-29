#!/bin/bash

## Usage:
##   . ./export-env.sh ; $COMMAND
##   . ./export-env.sh ; echo ${MINIENTREGA_FECHALIMITE}

cd backend
flask run --host=0.0.0.0 --port=$1
