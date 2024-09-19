#!/bin/bash

# Prompt for the domain name
read -p "Enter domain to scan: " domain

# 1. Run waymore.py
echo "Running waymore.py for $domain"
python waymore.py -i $domain -mode U -xcc

# 2. XSS scan
echo "Running XSS scan on $domain"
cat results/$domain/waymore.txt | grep "=" | uro | nuclei -t /home/g0x0kakashi/fuzz/xss/reflected-xss.yaml -fuzz

# 3. Open Redirect scan
echo "Running Open Redirect scan on $domain"
cat results/$domain/waymore.txt | grep "=" | uro | nuclei -t /home/g0x0kakashi/fuzz/redirect/open-redirect.yaml -fuzz

# 4. LFI scan
echo "Running LFI scan on $domain"
cat results/$domain/waymore.txt | grep "=" | uro | nuclei -t /home/g0x0kakashi/fuzz/lfi/linux-lfi-fuzz.yaml -fuzz

echo "Scan completed for $domain"
