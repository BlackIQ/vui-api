#!/bin/bash

# Get the list of users and store them in an array
users=($(cut -d: -f1 /etc/passwd))

# Print the list of users
for user in "${users[@]}"; do
    echo "$user"
done
