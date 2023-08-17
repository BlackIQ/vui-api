#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <username>"
    exit 1
fi

username=$1

# Disable SSH access for the user
sudo usermod -s /usr/sbin/nologin $username