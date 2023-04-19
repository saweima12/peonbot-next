#!/bin/bash

export BOT_CONFIG="$(pwd)/env.py"
pipenv run sanic peonbot:create_app --factory -H 0.0.0.0 -p 8000 -d
