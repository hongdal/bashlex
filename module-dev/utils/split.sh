#!/bin/bash

if [[ -z $2 ]]; then 
    echo "Usage: $0 <all-cd-pattern file> <dir-to-contain-outputs>"
    exit 1
fi

input="$1"
mkdir "$2"
count=0
while IFS= read -r var
do
  count=$((count+1))
  echo "$var" > "$2/$count.sh"
done < "$input"
