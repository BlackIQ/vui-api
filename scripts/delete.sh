#!/bin/bash

# Check if both username is provided
if [ $# -ne 1 ]; then
    echo "Usage: ./delete.sh <username>"
    exit 1
fi

# Assign the provided arguments to variables
username="$1"

# Delete the user
userdel "$username"
# userdel -r "$username"
