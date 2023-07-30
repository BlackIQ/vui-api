#!/bin/bash

# Check if both username and password are provided
if [ $# -ne 2 ]; then
    echo "Usage: ./create.sh <username> <password>"
    exit 1
fi

# Assign the provided arguments to variables
username="$1"
password="$2"

# Create the user
useradd -r -s /bin/false "$username"

# Set the password for the user
echo "$username:$password" | chpasswd
