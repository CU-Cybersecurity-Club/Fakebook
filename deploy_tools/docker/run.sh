#!/bin/bash

service ssh start
sudo -u $flask_user -s -- <<EOF
cd $fakebook_home
python3 app.py &
EOF
