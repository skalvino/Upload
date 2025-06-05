#!/bin/bash

# Function to display usage
usage() {
  echo -e "\e[33mUsage: $0 [-d domain] [-l list.txt]\e[0m"
  exit 1
}

# Parse command line arguments
while getopts ":d:l:" opt; do
  case $opt in
    d)
      domain=$OPTARG
      ;;
    l)
      list_file=$OPTARG
      ;;
    *)
      usage
      ;;
  esac
done

# Check if neither domain nor list file is provided
if [ -z "$domain" ] && [ -z "$list_file" ]; then
  usage
fi

# Function to perform scans
scan_domain() {
  local domain=$1
  echo -e "\e[34mScanning $domain\e[0m"

  # 1. Run waymore.py
  echo -e "\e[1;49;32mRunning waymore.py for $domain\e[0m"
  python waymore.py -i "$domain" -mode U -xcc

  # 2. XSS scan
  echo -e "\e[1;49;32mRunning XSS scan on $domain\e[0m"
  cat "results/$domain/waymore.txt" | grep "=" | qsreplace | uro | nuclei -silent -t /home/rihamhammoud93/fuzz/xss/reflected-xss.yaml -fuzz

  # 3. Open Redirect scan
  echo -e "\e[1;49;32mRunning Open Redirect scan on $domain\e[0m"
  cat "results/$domain/waymore.txt" | grep "=" | qsreplace | uro | nuclei -silent -t /home/rihamhammoud93/fuzz/redirect/open-redirect.yaml -fuzz

  echo -e "\e[1;49;33mScan completed for $domain\e[0m"
}

# If a list file is provided, scan domains from the list
if [ -n "$list_file" ]; then
  if [ ! -f "$list_file" ]; then
    echo -e "\e[31mFile $list_file not found!\e[0m"
    exit 1
  fi

  while read -r domain_from_list; do
    # Skip empty lines and comments
    [[ -z "$domain_from_list" || "$domain_from_list" =~ ^# ]] && continue
    scan_domain "$domain_from_list"
  done < "$list_file"

else
  # If no list file, scan the single domain
  scan_domain "$domain"
fi

echo -e "\e[33mAll scans completed.\e[0m"
