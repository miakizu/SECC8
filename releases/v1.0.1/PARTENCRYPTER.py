import os
import secrets
import string
import pyminizip
import base64
from tqdm import tqdm
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Base64-decoded strings for messages
s1 = base64.b64decode("RmlsZSBub3QgZm91bmQh".encode()).decode()
s2 = base64.b64decode("UGFydGl0aW9uaW5nIGZpbGU=".encode()).decode()
s3 = base64.b64decode("RW50ZXIgdGhlIHBhdGggdG8gdGhlIGZpbGUgeW91IHdhbnQgdG8gcGFydGl0aW9uOiA=".encode()).decode()
s4 = base64.b64decode("V2hlcmUgd291bGQgeW91IGxpa2UgdGhlIGZpbGVzIHRvIGJlIHNhdmVkPyA=".encode()).decode()
s5 = base64.b64decode("RW50ZXIgdGhlIHBhcnRpdGlvbiBzaXplIChpbiBNQik6 IA==".encode()).decode()
s6 = base64.b64decode("RmlsZSBzcGxpdCBpbnRvIHt9IFpJUCBwYXJ0cy4gUGFzc3dvcmRzIHNhdmVkIGluIHBhc3N3b3Jkcy50eHQgKEJhc2U2NCBlbmNvZGVkKS4=".encode()).decode()






# THIS CODE IS ABSOLUTELY SHIT. REPORT ANY AND ALL ERRORS IN GITHUB REPO.
# You are on version 1.0











# ASCII Art for the title
ASCII_ART = f"""
{Fore.CYAN}
  ______ _ _      ______      _   _             
 |  ____(_) |    |  ____|    | | (_)            
 | |__   _| | ___| |__  __  _| |_ _ _ __   __ _ 
 |  __| | | |/ _ \\  __| \\ \\/ / __| | '_ \\ / _` |
 | |    | | |  __/ |____ >  <| |_| | | | | (_| |
 |_|    |_|_|\\___|______/_/\\_\\\\__|_|_| |_|\\__, |
                                            __/ |
                                           |___/ 
{Style.RESET_ALL}
"""

# Function to generate a random password
generate_password = lambda l=12: ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(l))

def partition_file(file_path, output_dir, chunk_size_mb):
    part_num, passwords = 1, []
    if not os.path.isfile(file_path):
        print(f"{Fore.RED}{s1}{Style.RESET_ALL}")
        return

    total_size = os.path.getsize(file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.splitext(os.path.basename(file_path))[0]

    with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"{Fore.YELLOW}{s2}{Style.RESET_ALL}", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size_mb * 1024 * 1024)
                if not chunk:
                    break

                password = generate_password()
                passwords.append(password)

                # Create a temporary file for the chunk
                temp_file = os.path.join(output_dir, f"{base_name}_part{part_num}_data")
                with open(temp_file, 'wb') as temp:
                    temp.write(chunk)

                # Define the ZIP file name
                zip_file = os.path.join(output_dir, f"{base_name}_part{part_num}.zip")
                # Compress the temporary file into the ZIP
                pyminizip.compress(temp_file, None, zip_file, password, 5)
                # Delete the temporary file
                os.remove(temp_file)

                pbar.update(len(chunk))
                part_num += 1

    # Save passwords to passwords.txt
    passwords_encoded = base64.b64encode("\n".join([f"Part {i}: {p}" for i, p in enumerate(passwords, 1)]).encode()).decode()
    with open(os.path.join(output_dir, "passwords.txt"), 'w') as pw_file:
        pw_file.write(passwords_encoded)

    print(f"{Fore.GREEN}{s6.format(part_num - 1)}{Style.RESET_ALL}")

    # Prompt the user to exit
    input(f"{Fore.BLUE}Type anything to exit...{Style.RESET_ALL}")

def main():
    print(ASCII_ART)
    file_path = input(f"{Fore.BLUE}{s3}{Style.RESET_ALL}").strip('"')
    output_dir = input(f"{Fore.BLUE}{s4}{Style.RESET_ALL}").strip('"')
    chunk_size_mb = int(input(f"{Fore.BLUE}{s5}{Style.RESET_ALL}").strip())
    partition_file(file_path, output_dir, chunk_size_mb)

if __name__ == "__main__":
    main()
