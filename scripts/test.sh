#!/bin/bash

# Check if name is provided
if [ $# -ne 2 ]; then
    echo "Usage: ./test.sh <name>"
    exit 1
fi

# Assign the provided arguments to variables
name="$1"

# Echo name
echo $name