#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <username>"
    exit 1
fi

username=$1

# Enable SSH access for the user
sudo usermod -s /bin/bash $username