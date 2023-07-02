#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./add.sh <name>"
    exit 1
fi

name="$1"


echo $name