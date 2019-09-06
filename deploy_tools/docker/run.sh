#!/bin/bash
# Script to run everything required for the lab
service ssh start

cd "$fakebook_home" && sudo $flask_user python3 app.py &
