#!/bin/bash

# Parse options
while getopts "l:" opt; do
  case ${opt} in
    l )
      URL_LIST_FILE=$OPTARG
      ;;
    \? )
      echo "Usage: $0 -l url_list_file"
      exit 1
      ;;
  esac
done

# Check if URL list file is provided
if [ -z "$URL_LIST_FILE" ]; then
  echo "Usage: $0 -l url_list_file"
  exit 1
fi

# Read the URL list file line by line
while IFS= read -r url; do
  echo "Running ffuf for URL: $url"
  ffuf -c -w fuzz.txt -u "$url/FUZZ" -mc 200
done < "$URL_LIST_FILE"
