#!/bin/bash

# Check if username is provided
if [ $# -ne 1 ]; then
    echo "Usage: ./test.sh <username>"
    exit 1
fi

# Assign the provided arguments to variables
username="$1"

# Echo username
echo $username