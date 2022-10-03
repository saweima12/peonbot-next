#!/bin/bash

export BOT_CONFIG="$(pwd)/env.py"
pipenv run sanic peonbot:app -H 0.0.0.0 -p 8000 -d