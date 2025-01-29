import os
import secrets
import string
import pyminizip
import base64
from tqdm import tqdm
from colorama import Fore, Back, Style, init
import shutil
import patoolib
import time

init(autoreset=True)

# Updated base64 encoded strings
s1 = base64.b64decode("UGF0aCBub3QgZm91bmQh".encode()).decode()  
s2 = base64.b64decode("UGFydGl0aW9uaW5nIGZpbGU=".encode()).decode()
s3 = base64.b64decode("RW50ZXIgdGhlIHBhdGggdG8gdGhlIGZpbGUvZm9sZGVyIHlvdSB3YW50IHRvIHByb2Nlc3M6IA==".encode()).decode()
s4 = base64.b64decode("T3V0cHV0IGRpcmVjdG9yeTog".encode()).decode()
s5 = base64.b64decode("UGFydGl0aW9uIHNpemUgKE1CKTog".encode()).decode()
s6 = base64.b64decode("UHJvY2Vzc2VkIGZpbGUgc3BsaXQgaW50byB7fSBaSVAgcGFydHMuIFBhc3N3b3JkcyBpbiBwYXNzd29yZHMudHh0".encode()).decode()
s7 = base64.b64decode("QXJjaGl2aW5nIGZvbGRlci4uLg==".encode()).decode()

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
{Fore.BLUE}
          {Fore.CYAN}*{Fore.BLUE}     {Fore.CYAN}*{Fore.BLUE}     {Fore.CYAN}*{Fore.BLUE}
        {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}
      {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}
    {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}
  {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}
{Fore.WHITE}
        /| ________________________________________________________
O|===|* >________________________________________________________>
        \\|
{Fore.BLUE}
          {Fore.CYAN}*{Fore.BLUE}     {Fore.CYAN}*{Fore.BLUE}     {Fore.CYAN}*{Fore.BLUE}
        {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}
      {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}
    {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}
  {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}   {Fore.CYAN}*{Fore.BLUE}
{Style.RESET_ALL}
"""

generate_password = lambda l=12: ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(l))

def archive_folder(folder_path, output_dir):
    if not os.path.isdir(folder_path):
        return None

    print(f"{Fore.YELLOW}{s7}{Style.RESET_ALL}")
    archive_name = f"{os.path.basename(folder_path)}_{int(time.time())}.rar"
    archive_path = os.path.join(output_dir, archive_name)
    
    try:
        patoolib.create_archive(archive_path, [folder_path], program='rar')
    except Exception as e:
        print(f"{Fore.RED}Archive creation failed: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Make sure you have RAR installed and in PATH{Style.RESET_ALL}")
        return None
    
    return archive_path

def partition_file(file_path, output_dir, chunk_size_mb):
    part_num, passwords = 1, []
    original_filename = os.path.basename(file_path)
    total_size = os.path.getsize(file_path)
    
    with tqdm(total=total_size, unit='B', unit_scale=True, desc=f"{Fore.YELLOW}{s2}{Style.RESET_ALL}", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size_mb * 1024 * 1024)
                if not chunk:
                    break

                password = generate_password()
                passwords.append(password)

                temp_file = os.path.join(output_dir, f"temp_part_{part_num}")
                with open(temp_file, 'wb') as temp:
                    temp.write(chunk)

                zip_file = os.path.join(output_dir, f"{os.path.splitext(original_filename)[0]}_part{part_num}.zip")
                pyminizip.compress(temp_file, None, zip_file, password, 5)
                os.remove(temp_file)

                pbar.update(len(chunk))
                part_num += 1

    passwords_with_metadata = [original_filename] + [f"Part {i}: {p}" for i, p in enumerate(passwords, 1)]
    passwords_encoded = base64.b64encode("\n".join(passwords_with_metadata).encode()).decode()
    with open(os.path.join(output_dir, "passwords.txt"), 'w') as pw_file:
        pw_file.write(passwords_encoded)

    print(f"{Fore.GREEN}{s6.format(part_num - 1)}{Style.RESET_ALL}")

def main():
    print(ASCII_ART)
    input_path = input(f"{Fore.BLUE}{s3}{Style.RESET_ALL}").strip('"')
    output_dir = input(f"{Fore.BLUE}{s4}{Style.RESET_ALL}").strip('"')
    chunk_size_mb = int(input(f"{Fore.BLUE}{s5}{Style.RESET_ALL}").strip())

    if not os.path.exists(input_path):
        print(f"{Fore.RED}{s1}{Style.RESET_ALL}")
        return

    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)

    # Archive folder if input is directory
    if os.path.isdir(input_path):
        archive_path = archive_folder(input_path, output_dir)
        if not archive_path:
            return
        file_to_process = archive_path
    else:
        file_to_process = input_path

    # Process the file (original or archived)
    partition_file(file_to_process, output_dir, chunk_size_mb)

    # Clean up temporary archive
    if os.path.isdir(input_path):
        try:
            os.remove(file_to_process)
        except:
            pass

    input(f"{Fore.BLUE}Press Enter to exit...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()