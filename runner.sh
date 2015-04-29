#!/bin/sh

# Only forward if the pause file doesn't exist
if [ ! -f ./pause ]; then
    python forwardNotif.py
fi
