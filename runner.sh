#!/bin/bash

# Only forward if the pause file doesn't exist
if [ ! -f ${BASH_SOURCE[0]%/*}/pause ]; then
    python ${BASH_SOURCE[0]%/*}/forwardNotif.py
fi
