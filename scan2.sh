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

# Check if either domain or list file is provided
if [ -z "$domain" ] && [ -z "$list_file" ]; then
  usage
fi

# Function to perform scans
scan_domain() {
  local domain=$1
  echo -e "\e[34mScanning $domain\e[0m"

  # 1. Run waymore.py
  echo -e "\e[32mRunning waymore.py for $domain\e[0m"
  python waymore.py -i $domain -mode U -xcc

  # 2. XSS scan
  echo -e "\e[32mRunning XSS scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | uro | nuclei -t /home/g0x0kakashi/fuzz/xss/reflected-xss.yaml -fuzz

  # 3. Open Redirect scan
  echo -e "\e[32mRunning Open Redirect scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | uro | nuclei -t /home/g0x0kakashi/fuzz/redirect/open-redirect.yaml -fuzz

  # 4. LFI scan
  echo -e "\e[32mRunning LFI scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | uro | nuclei -t /home/g0x0kakashi/fuzz/lfi/linux-lfi-fuzz.yaml -fuzz

  echo -e "\e[34mScan completed for $domain\e[0m"
}

# Scan a single domain if provided
if [ -n "$domain" ]; then
  scan_domain "$domain"
fi

# Scan domains from the list file if provided
if [ -n "$list_file" ]; then
  if [ ! -f "$list_file" ]; then
    echo -e "\e[31mFile $list_file not found!\e[0m"
    exit 1
  fi

  domains=$(cat "$list_file")
  for domain in $domains; do
    scan_domain "$domain"
  done
fi

echo -e "\e[33mAll scans completed.\e[0m"
