#!/bin/bash

export INLINEBOT_CONFIG="$(pwd)/env.py"
pipenv run sanic inlinebot:app -H 0.0.0.0 -p 8000 -d