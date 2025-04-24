import os
import pyminizip
import base64
import re
import shutil
import zipfile
import logging
import threading
from tkinter import *
from tkinter import ttk, filedialog, scrolledtext
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Base64 obfuscated lines
_ = lambda x: base64.b64decode(x.encode()).decode()
s1 = _("RW50ZXIgdGhlIGZvbGRlciBjb250YWluaW5nIHRoZSBwYXJ0aXRpb25lZCBmaWxlczog")
s2 = _("RW50ZXIgdGhlIGZvbGRlciB0byBleHRyYWN0IHRoZSBmaWxlcyB0bzog")
s3 = _("RGV0ZXJtaW5pbmcgbnVtYmVyIG9mIHBhcnRzLi4u")
s4 = _("UGFzc3dvcmQgZmlsZSBub3QgZm91bmQh")
s5 = _("RXh0cmFjdGluZyBwYXJ0cy4uLg==")
s6 = _("RmlsZXMgZXh0cmFjdGVkIHN1Y2Nlc3NmdWxseSB0byB7fS4=")
s7 = _("RXJyb3JzIG9jY3VycmVkIGR1cmluZyBleHRyYWN0aW9uLiBQbGVhc2UgY2hlY2sgdGhlIG91dHB1dCBmb2xkZXIu")
s8 = _("UHJlc3MgYW55IGtleSB0byBleGl0Li4u")

# Configure logging
l = os.path.join(os.getcwd(), "extraction_errors.log")
logging.basicConfig(filename=l, level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

class DecryptionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SECC8 Decrypter")
        self.root.configure(bg='black')
        self.setup_ui()
        self.create_log_handler()

    def ASCII_ART(self):
        return r"""
          .                                                      .
        .n                   .                 .                  n.
  .   .dP                  dP                   9b                 9b.    .
 4    qXb         .       dX                     Xb       .        dXp     t
dX.    9Xb      .dXb    __                         __    dXb.     dXP     .Xb
9XXb._       _.dXXXXb dXXXXbo.                 .odXXXXb dXXXXb._       _.dXXP
 9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP
  `9XXXXXXXXXXXXXXXXXXXXX'~   ~`OOO8b   d8OOO'~   ~`XXXXXXXXXXXXXXXXXXXXXP'
    `9XXXXXXXXXXXP' `9XX'   DIE    `98v8P'  HUMAN   `XXP' `9XXXXXXXXXXXP'
        ~~~~~~~       9X.          .db|db.          .XP       ~~~~~~~
                        )b.  .dbo.dP'`v'`9b.odb.  .dX(
                      ,dXXXXXXXXXXXb     dXXXXXXXXXXXb.
                     dXXXXXXXXXXXP'   .   `9XXXXXXXXXXXb
                    dXXXXXXXXXXXXb   d|b   dXXXXXXXXXXXXb
                    9XXb'   `XXXXXb.dX|Xb.dXXXXX'   `dXXP
                     `'      9XXXXXX(   )XXXXXXP      `'
                              XXXX X.`v'.X XXXX
                              XP^X'`b   d'`X^XX
                              X. 9  `   '  P )X
                              `b  `       '  d'
                               `             '""".strip('\n')

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='black')
        style.configure('TLabel', background='black', foreground='cyan')
        style.configure('TButton', background='#002b36', foreground='cyan')
        style.map('TButton', background=[('active', '#004445')])
        
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=BOTH, expand=True)

        # ASCII Art
        ascii_frame = ttk.Frame(main_frame)
        ascii_frame.pack(pady=5)
        ascii_art = Text(ascii_frame, bg='black', fg='cyan', width=78, height=18,
                        font=('Courier', 7), relief=FLAT)
        ascii_art.insert(END, self.ASCII_ART())
        ascii_art.configure(state='disabled')
        ascii_art.pack()

        # Input Fields
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=X, pady=10)

        ttk.Label(input_frame, text="Partitioned Files Folder:").grid(row=0, column=0, sticky=W)
        self.source_entry = ttk.Entry(input_frame, width=50)
        self.source_entry.grid(row=0, column=1, padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_source).grid(row=0, column=2)

        ttk.Label(input_frame, text="Extraction Destination:").grid(row=1, column=0, sticky=W, pady=5)
        self.dest_entry = ttk.Entry(input_frame, width=50)
        self.dest_entry.grid(row=1, column=1, padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_dest).grid(row=1, column=2)

        # Start Button
        self.start_btn = ttk.Button(main_frame, text="Start Decryption", command=self.start_process)
        self.start_btn.pack(pady=10)

        # Log Area
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill=BOTH, expand=True)
        self.log_area = scrolledtext.ScrolledText(log_frame, bg='black', fg='white', 
                                                 font=('Consolas', 10), wrap=WORD)
        self.log_area.pack(fill=BOTH, expand=True)
        self.log_area.tag_config('info', foreground='cyan')
        self.log_area.tag_config('warning', foreground='red')
        self.log_area.tag_config('success', foreground='green')
        self.log_area.tag_config('header', foreground='cyan', font=('Consolas', 12, 'bold'))

    def create_log_handler(self):
        self.log_handler = logging.Handler()
        self.log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logging.getLogger().addHandler(self.log_handler)
        logging.getLogger().setLevel(logging.INFO)

    def browse_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_entry.delete(0, END)
            self.source_entry.insert(0, folder)

    def browse_dest(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_entry.delete(0, END)
            self.dest_entry.insert(0, folder)

    def start_process(self):
        self.start_btn.config(state=DISABLED)
        self.log_area.delete(1.0, END)
        threading.Thread(target=self.run_decryption, daemon=True).start()

    def run_decryption(self):
        try:
            folder = self.source_entry.get()
            extract_to = self.dest_entry.get()
            self.handle_decryption(folder, extract_to)
        except Exception as ex:
            self.log_error("Fatal error", ex)
        finally:
            self.root.after(0, lambda: self.start_btn.config(state=NORMAL))

    def log_message(self, message, tag=None):
        self.log_area.configure(state='normal')
        self.log_area.insert(END, message + '\n', tag)
        self.log_area.configure(state='disabled')
        self.log_area.see(END)
        self.root.update_idletasks()

    def log_info(self, message):
        self.log_message("ℹ " + message, 'info')

    def log_warning(self, message):
        self.log_message("⚠ " + message + " ⚠", 'warning')

    def log_success(self, message):
        self.log_message("✔ " + message + " ✔", 'success')

    def log_header(self, message):
        self.log_message("\n" + "="*60 + "\n" + message.center(60) + "\n" + "="*60, 'header')

    def log_error(self, message, ex=None):
        error_msg = f"{message}: {str(ex)}" if ex else message
        logging.error(error_msg)
        self.log_warning(f"An error occurred. Details logged to {l}")

    def extract_archive(self, archive_path, output_dir):
        ext = os.path.splitext(archive_path)[1].lower()
        try:
            if ext == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zf:
                    zf.extractall(output_dir)
                self.log_info(f"Extracted {archive_path} as ZIP")

            elif ext == '.rar':
                try:
                    import rarfile
                    with rarfile.RarFile(archive_path) as rf:
                        rf.extractall(output_dir)
                    self.log_info(f"Extracted {archive_path} as RAR")
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
                    self.log_info(f"Extracted {archive_path} as 7Z")
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

    def handle_folder_rename(self, original_path):
        try:
            items = os.listdir(original_path)
            if len(items) == 1:
                item_path = os.path.join(original_path, items[0])
                if os.path.isdir(item_path):
                    self.log_info(f"Extracted contents found in: {item_path}")
                    return item_path
            return original_path
        except Exception as ex:
            self.log_error("Error handling extracted directory structure", ex)
            return original_path

    def handle_decryption(self, folder, extract_to):
        try:
            self.log_header("Starting Decryption Process")
            
            # Password file handling
            p = os.path.join(folder, "passwords.txt")
            if not os.path.isfile(p):
                self.log_warning(s4)
                self.log_error("Password file not found")
                return

            try:
                with open(p, 'r') as pw_file:
                    content = base64.b64decode(pw_file.read()).decode().split('\n')
                    original_filename = content[0]
                    passwords_list = content[1:]
                    self.log_info(f"Original filename: {original_filename}")
            except Exception as ex:
                self.log_error("Failed to read password file", ex)
                return

            # Part detection
            self.log_header("Determining Number of Parts...")
            try:
                zip_files = sorted(
                    [f for f in os.listdir(folder) if re.match(r".+_part\d+\.zip", f)],
                    key=lambda x: int(re.search(r"_part(\d+)\.zip", x).group(1))
                )
                num_parts = len(zip_files)
                self.log_info(f"Found {num_parts} parts")
            except Exception as ex:
                self.log_error("Failed to identify parts", ex)
                return

            if num_parts != len(passwords_list):
                self.log_warning(s4)
                self.log_error(f"Mismatch: {num_parts} parts vs {len(passwords_list)} passwords")
                return

            # Parts extraction
            self.log_header("Extracting Parts...")
            error_flag = False
            extract_dir = os.path.join(extract_to, "temp_parts")
            os.makedirs(extract_dir, exist_ok=True)

            for idx in range(num_parts):
                zip_path = os.path.join(folder, zip_files[idx])
                password = passwords_list[idx].split(': ')[1]
                self.log_info(f"Extracting {zip_files[idx]} with password: {password}")
                try:
                    pyminizip.uncompress(zip_path, password, extract_dir, 0)
                    self.log_info(f"Extracted {zip_files[idx]} successfully.")
                except Exception as ex:
                    self.log_error(f"Failed to extract {zip_files[idx]}", ex)
                    error_flag = True

            # File reconstruction
            self.log_header("Reconstructing Original File...")
            reconstructed_path = os.path.join(extract_to, original_filename)
            try:
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
                self.log_info(f"Reconstructed file saved as {reconstructed_path}")
            except Exception as ex:
                self.log_error("File reconstruction failed", ex)
                error_flag = True

            # Final extraction
            try:
                self.log_header("Extracting Final Archive...")
                extract_dir_final = os.path.join(extract_to, "extracted_contents")
                os.makedirs(extract_dir_final, exist_ok=True)
                
                self.extract_archive(reconstructed_path, extract_dir_final)
                final_dir = self.handle_folder_rename(extract_dir_final)
                
                if os.path.exists(reconstructed_path):
                    try:
                        os.remove(reconstructed_path)
                        self.log_info(f"Cleaned up temporary file: {reconstructed_path}")
                    except Exception as clean_ex:
                        self.log_warning(f"Couldn't delete temporary file: {clean_ex}")
                        self.log_info("You can safely delete this file manually later")

                if not error_flag:
                    self.log_success("\nEXTRACTION SUCCESSFUL!\n")
                    self.log_info(f"Final output location: {final_dir}")

            except RuntimeError as ex:
                self.log_warning("Dependency required!\n" + str(ex))
                self.log_info(f"Reconstructed file preserved at:\n{reconstructed_path}")
                self.log_info("You can either:")
                self.log_info("1. Install the missing dependency and try again")
                self.log_info("2. Extract it manually with appropriate software")
            except Exception as ex:
                self.log_error("Final extraction failed", ex)

            shutil.rmtree(extract_dir, ignore_errors=True)

        except Exception as ex:
            self.log_error("Unexpected error", ex)

if __name__ == "__main__":
    root = Tk()
    root.geometry("800x700")
    gui = DecryptionGUI(root)
    root.mainloop()
