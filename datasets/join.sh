#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <subtlds> <tlds>"
    exit 1
fi

list1_file=$1
list2_file=$2

mapfile -t list1 < "$list1_file"
mapfile -t list2 < "$list2_file"

for item1 in "${list1[@]}"; do
    for item2 in "${list2[@]}"; do
        echo "$item1.$item2"
    done
done
