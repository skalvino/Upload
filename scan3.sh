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
  echo -e "\e[1;49;32mRunning waymore.py for $domain\e[0m"
  python waymore.py -i $domain -mode U -xcc

  # 2. XSS scan
  echo -e "\e[1;49;32mRunning XSS scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -t /home/g0x0kakashi/fuzz/xss/reflected-xss.yaml -fuzz

  # 3. Open Redirect scan
  echo -e "\e[1;49;32mRunning Open Redirect scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -t /home/g0x0kakashi/fuzz/redirect/open-redirect.yaml -fuzz

  # 4. LFI scan
  echo -e "\e[1;49;32mRunning LFI scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -t /home/g0x0kakashi/fuzz/lfi/linux-lfi-fuzz.yaml -fuzz
  
  # 5. RFI scan
  echo -e "\e[1;49;32mRunning RFI scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -t /home/g0x0kakashi/fuzz/rfi/rfi.yaml -fuzz  
  
  # 6. SQLi Time-Base scan
  echo -e "\e[1;49;32mRunning SQLi Time-Base scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -t /home/g0x0kakashi/fuzz/sqli/sqli.yaml -fuzz  

  # 7. SQLi Error-Base scan
  echo -e "\e[1;49;32mRunning SQLi Error-Base scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -t /home/g0x0kakashi/fuzz/sqli/error-based-skalvin.yaml -fuzz    

  # 8. RCE With Payload-1 scan
  echo -e "\e[1;49;32mRunning RCE With Payload-1 scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -t /home/g0x0kakashi/fuzz/rce/rce1.yaml -fuzz

  # 9. RCE With Payload-2 scan
  echo -e "\e[1;49;32mRunning RCE With Payload-2 scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -t /home/g0x0kakashi/fuzz/rce/rce2.yaml -fuzz

  # 10. RCE With Payload-3 scan
  echo -e "\e[1;49;32mRunning RCE With Payload-3 scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -t /home/g0x0kakashi/fuzz/rce/rce3.yaml -fuzz

  # 11. RCE With Payload-4 scan
  echo -e "\e[1;49;32mRunning RCE With Payload-4 scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -t /home/g0x0kakashi/fuzz/rce/rce4.yaml -fuzz

  # 12. RCE With Payload-5 scan
  echo -e "\e[1;49;32mRunning RCE With Payload-5 scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -t /home/g0x0kakashi/fuzz/rce/rce5.yaml -fuzz

  # 13. RCE With Payload-6 scan
  echo -e "\e[1;49;32mRunning RCE With Payload-6 scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -t /home/g0x0kakashi/fuzz/rce/rce6.yaml -fuzz

  # 14. RCE With Payload-6 scan
  echo -e "\e[1;49;32mRunning RCE With Payload-6 scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -t /home/g0x0kakashi/fuzz/rce/rce6.yaml -fuzz

  # 15. CVE-2014-4942 scan
  echo -e "\e[1;49;32mRunning CVE-2014-4942 scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -id CVE-2014-4942

  # 16. CVE-2018-20608 scan
  echo -e "\e[1;49;32mRunning CVE-2018-20608 scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -id CVE-2018-20608
  
  # 17. CVE-2020-5776 scan
  echo -e "\e[1;49;32mRunning CVE-2020-5776 scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -id CVE-2020-5776
  
  # 18. CVE-2021-3293 scan
  echo -e "\e[1;49;32mRunning CVE-2021-3293 scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -id CVE-2021-3293
  
  # 19. CVE-2021-37704 scan
  echo -e "\e[1;49;32mRunning CVE-2021-37704 scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -id CVE-2021-37704

  # 20. CVE-2022-0885 scan
  echo -e "\e[1;49;32mRunning CVE-2022-0885 scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -id CVE-2022-0885

  # 21. CVE-2022-32028 scan
  echo -e "\e[1;49;32mRunning CVE-2022-32028 scan on $domain\e[0m"
  cat results/$domain/waymore.txt | grep "=" | qsreplace | uro | nuclei -id CVE-2022-32028
  
  echo -e "\e[1;49;33mScan completed for $domain\e[0m"
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
