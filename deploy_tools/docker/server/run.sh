#!/bin/sh

# Run gunicorn server
sudo -u www-data -s -- <<EOF

cd $FAKEBOOK_HOME
gunicorn --worker-class gevent --bind 0.0.0.0:8000 app

EOF
