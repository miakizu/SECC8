import os
import pyminizip
import base64
import re
import shutil
import zipfile
import logging
from colorama import Fore, Style, init

# Base 64 obfuscated lines
init(autoreset=True)
_ = lambda x: base64.b64decode(x.encode()).decode()
s1 = _("RW50ZXIgdGhlIGZvbGRlciBjb250YWluaW5nIHRoZSBwYXJ0aXRpb25lZCBmaWxlczog")
s2 = _("RW50ZXIgdGhlIGZvbGRlciB0byBleHRyYWN0IHRoZSBmaWxlcyB0bzog")
s3 = _("RGV0ZXJtaW5pbmcgbnVtYmVyIG9mIHBhcnRzLi4u")
s4 = _("UGFzc3dvcmQgZmlsZSBub3QgZm91bmQh")
s5 = _("RXh0cmFjdGluZyBwYXJ0cy4uLg==")
s6 = _("RmlsZXMgZXh0cmFjdGVkIHN1Y2Nlc3NmdWxseSB0byB7fS4=")
s7 = _("RXJyb3JzIG9jY3VycmVkIGR1cmluZyBleHRyYWN0aW9uLiBQbGVhc2UgY2hlY2sgdGhlIG91dHB1dCBmb2xkZXIu")
s8 = _("UHJlc3MgYW55IGtleSB0byBleGl0Li4u")
l = os.path.join(os.getcwd(), "extraction_errors.log")
logging.basicConfig(filename=l, level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

ASCII_ART = f"""
{Fore.CYAN}
  ______ _ _      ______      _   _             
 |  ____(_) |    |  ____|    | | (_)            
 | |__   _| | ___| |__  __  _| |_ _ _ __   __ _ 
 |  __| | | |/ _ \\  __| \\ \\/ / __| | '_ \\ / _` |
 | |    | | |  __/ |____ >  <| |_| | | | | (_| |
 |_|    | |_|\\___|______/_/\\_\\\\__|_|_| |_|\\__, |
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

def print_header(t): 
    print(Fore.CYAN + "=" * 60 + "\n" + t.center(60) + "\n" + "=" * 60 + Style.RESET_ALL)
def print_warning(t): 
    print(Fore.RED + "⚠ " + t + " ⚠" + Style.RESET_ALL)
def print_success(t): 
    print(Fore.GREEN + "✔ " + t + " ✔" + Style.RESET_ALL)
def print_info(t): 
    print(Fore.BLUE + "ℹ " + t + Style.RESET_ALL)
def log_error(m, ex=None): 
    logging.error(f"{m}: {str(ex)}", exc_info=True) if ex else logging.error(m)
    print_warning(f"An error occurred. Details logged to {l}")

def extract_archive(archive_path, output_dir):
    ext = os.path.splitext(archive_path)[1].lower()
    try:
        if ext == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zf:
                zf.extractall(output_dir)
            print_info(f"Extracted {archive_path} as ZIP")

        elif ext == '.rar':
            try:
                import rarfile
                from rarfile import RarFile
                with RarFile(archive_path) as rf:
                    rf.extractall(output_dir)
                print_info(f"Extracted {archive_path} as RAR")
            except Exception as e:
                if "unrar not found" in str(e):
                    raise RuntimeError(
                        "RAR extraction requires unrar executable!\n"
                        "Download from: https://www.rarlab.com/rar_add.htm\n"
                        "Add to PATH or place unrar.exe in script directory"
                    )
                raise

        elif ext == '.7z':
            try:
                import py7zr
                with py7zr.SevenZipFile(archive_path, mode='r') as zf:
                    zf.extractall(output_dir)
                print_info(f"Extracted {archive_path} as 7Z")
            except ImportError:
                raise RuntimeError(
                    "7z support requires 'py7zr' package.\n"
                    "Install with: pip install py7zr"
                )

        else:
            supported = ['.zip', '.rar', '.7z']
            raise ValueError(
                f"Unsupported archive format: {ext}\n"
                f"Supported formats: {', '.join(supported)}\n"
                "You can manually extract the reconstructed file"
            )

    except Exception as ex:
        raise ex

def handle_folder_rename(original_path):
    try:
        items = os.listdir(original_path)
        # If only one directory exists in the extraction folder, use it as the final path
        if len(items) == 1:
            item_path = os.path.join(original_path, items[0])
            if os.path.isdir(item_path):
                print_info(f"Extracted contents found in: {item_path}")
                return item_path
        return original_path
    except Exception as ex:
        log_error("Error handling extracted directory structure", ex)
        return original_path

def handle_decryption(folder, extract_to):
    try:
        print_header("Starting Decryption Process")
        
        # Password file handling
        p = os.path.join(folder, "passwords.txt")
        if not os.path.isfile(p):
            print_warning(s4)
            log_error("Password file not found")
            return

        try:
            with open(p, 'r') as pw_file:
                content = base64.b64decode(pw_file.read()).decode().split('\n')
                original_filename = content[0]
                passwords_list = content[1:]
                print_info(f"Original filename: {original_filename}")
        except Exception as ex:
            log_error("Failed to read password file", ex)
            return

        # Part detection
        print_header("Determining Number of Parts...")
        try:
            zip_files = sorted(
                [f for f in os.listdir(folder) if re.match(r".+_part\d+\.zip", f)],
                key=lambda x: int(re.search(r"_part(\d+)\.zip", x).group(1))
            )
            num_parts = len(zip_files)
            print_info(f"Found {num_parts} parts")
        except Exception as ex:
            log_error("Failed to identify parts", ex)
            return

        if num_parts != len(passwords_list):
            print_warning(s4)
            log_error(f"Mismatch: {num_parts} parts vs {len(passwords_list)} passwords")
            return

        # Parts extraction
        print_header("Extracting Parts...")
        error_flag = False
        extract_dir = os.path.join(extract_to, "temp_parts")
        os.makedirs(extract_dir, exist_ok=True)

        for idx in range(num_parts):
            zip_path = os.path.join(folder, zip_files[idx])
            password = passwords_list[idx].split(': ')[1]
            print_info(f"Extracting {zip_files[idx]} with password: {password}")
            try:
                pyminizip.uncompress(zip_path, password, extract_dir, 0)
                print_info(f"Extracted {zip_files[idx]} successfully.")
            except Exception as ex:
                log_error(f"Failed to extract {zip_files[idx]}", ex)
                error_flag = True

        # File reconstruction
        print_header("Reconstructing Original File...")
        reconstructed_path = os.path.join(extract_to, original_filename)
        try:
            # Collect all temp_part_* files and sort by part number
            temp_files = sorted(
                [f for f in os.listdir(extract_dir) if f.startswith("temp_part_")],
                key=lambda x: int(x.split('_')[2])
            )
            
            if not temp_files:
                raise FileNotFoundError("No temporary part files found for reconstruction")
            
            with open(reconstructed_path, 'wb') as out_file:
                for temp_file in temp_files:
                    part_path = os.path.join(extract_dir, temp_file)
                    with open(part_path, 'rb') as in_file:
                        shutil.copyfileobj(in_file, out_file)
                    os.remove(part_path)
            print_info(f"Reconstructed file saved as {reconstructed_path}")
        except Exception as ex:
            log_error("File reconstruction failed", ex)
            error_flag = True

        # Final extraction
        try:
            print_header("Extracting Final Archive...")
            extract_dir_final = os.path.join(extract_to, "extracted_contents")
            os.makedirs(extract_dir_final, exist_ok=True)
            
            extract_archive(reconstructed_path, extract_dir_final)
            final_dir = handle_folder_rename(extract_dir_final)
            
            if os.path.exists(reconstructed_path):
                try:
                    os.remove(reconstructed_path)
                    print_info(f"Cleaned up temporary file: {reconstructed_path}")
                except Exception as clean_ex:
                    print_warning(f"Couldn't delete temporary file: {clean_ex}")
                    print_info("You can safely delete this file manually later")

            if not error_flag:
                print_success("\nEXTRACTION SUCCESSFUL!\n")
                print_info(f"Final output location: {final_dir}")

        except RuntimeError as ex:
            print_warning("Dependency required!\n" + str(ex))
            print_info(f"Reconstructed file preserved at:\n{reconstructed_path}")
            print_info("You can either:")
            print_info("1. Install the missing dependency and try again")
            print_info("2. Extract it manually with appropriate software")
        except Exception as ex:
            log_error("Final extraction failed", ex)

        shutil.rmtree(extract_dir, ignore_errors=True)

    except Exception as ex:
        log_error("Unexpected error", ex)

def main():
    print(ASCII_ART)
    print_header("SECC8 Decryption")
    try:
        folder = input(s1).strip('"')
        extract_to = input(s2).strip('"')
        handle_decryption(folder, extract_to)
    except Exception as ex:
        log_error("Fatal error", ex)
    input(s8)

if __name__ == "__main__":
    main()