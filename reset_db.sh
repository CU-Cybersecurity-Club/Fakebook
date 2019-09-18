#!/bin/sh
BASE_DIR=$(dirname "$0")
sqlite3 "$BASE_DIR/data.db" < "$BASE_DIR/config/default_database"
