import os
import secrets
import string
import pyminizip
import base64
import shutil
import patoolib
import time
import threading
import tkinter as tk
import random
import math
import hashlib
from tkinter import ttk, filedialog, messagebox, scrolledtext

# DEVELOPMENT VERSION

class FilePartitionerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File Partitioner")
        self.root.geometry("800x700")
        self.root.configure(bg='black')

        # ttk styles for dark theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background='black', foreground='white')
        self.style.configure('TFrame', background='black')
        self.style.configure('TLabel', background='black', foreground='white')
        self.style.configure('TEntry', fieldbackground='black', foreground='white')
        self.style.configure('TButton', background='#333333', foreground='white')
        self.style.map('TButton', 
                      background=[('active', '#444444'), ('disabled', '#222222')],
                      foreground=[('disabled', '#666666')])
        self.style.configure('Horizontal.TProgressbar', 
                           troughcolor='black',
                           background='green',
                           lightcolor='green',
                           darkcolor='green')

        # main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # animated ASCII Art
        self.ascii_base = self.get_ascii_art().split('\n')
        self.animation_step = 0
        self.glow_phase = 0
        self.particles = []
        self.logo_label = tk.Label(self.main_container, 
                                 text='\n'.join(self.ascii_base), 
                                 font=("Courier", 9), 
                                 fg="#FF0000",
                                 bg='black',
                                 justify=tk.LEFT)
        self.logo_label.pack(pady=10, fill=tk.X)
        self.start_animation()
        
        # input controls container
        self.controls_frame = ttk.Frame(self.main_container)
        self.controls_frame.pack(pady=20, fill=tk.X, expand=True)
        
        # create controls
        self.create_input_controls()
        
        # Progress bar
        self.progress = ttk.Progressbar(self.main_container, 
                                      orient=tk.HORIZONTAL, 
                                      length=400, 
                                      mode='determinate')
        self.progress.pack(pady=10)
        
        # Log output
        self.log_area = scrolledtext.ScrolledText(self.main_container, 
                                                height=10, 
                                                wrap=tk.WORD,
                                                font=('Consolas', 9),
                                                bg='black',
                                                fg='white',
                                                insertbackground='white')
        self.log_area.pack(pady=10, fill=tk.BOTH, expand=True)

    def get_ascii_art(self):
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

    def start_animation(self):
        self.animate_ascii()

    def animate_ascii(self):
        # calculate glowing color
        self.glow_phase = (self.glow_phase + 0.15) % (2 * math.pi)
        glow_intensity = int((math.sin(self.glow_phase) + 1) * 127)
        main_color = f"#{min(255, 0x88 + glow_intensity):02X}0000"
        highlight_color = f"#FF{min(255, 0x66 + glow_intensity):02X}00"

        modified_lines = []
        eye_states = ['oo', 'OO', 'ÔÔ', 'ØØ', '00']
        particle_chars = ['✧', '✦', '✵', '❋', '❂', '✺']
        die_variants = ['DIE', 'DÏE', 'D!E', 'DÌE', 'DÎE']
        human_variants = ['HUMAN', 'HÜMAN', 'HUM4N', 'HÛMAN', 'HŪMAN']

        # add new particles
        if random.random() < 0.4:
            self.particles.append({
                'x': random.randint(0, 70),
                'y': 0,
                'char': random.choice(particle_chars),
                'life': random.randint(10, 20)
            })

        # process each line
        for y, line in enumerate(self.ascii_base):
            line_chars = list(line)
            
            # Update particles
            for part in self.particles[:]:
                if part['y'] == y and 0 <= part['x'] < len(line_chars):
                    line_chars[part['x']] = part['char']
                    part['y'] += 1
                    part['life'] -= 1
                    if part['life'] <= 0:
                        self.particles.remove(part)
            
            # Animate special elements
            line_str = ''.join(line_chars)
            if 'DIE' in line_str:
                line_str = line_str.replace('DIE', die_variants[self.animation_step % len(die_variants)])
            if 'HUMAN' in line_str:
                line_str = line_str.replace('HUMAN', human_variants[self.animation_step % len(human_variants)])
            if '()' in line_str:
                line_str = line_str.replace('()', eye_states[self.animation_step % len(eye_states)])
            
            modified_lines.append(line_str)

        # Update label with glowing colors
        self.logo_label.config(
            text='\n'.join(modified_lines),
            fg=highlight_color if self.animation_step % 2 else main_color
        )
        
        self.animation_step += 1
        self.root.after(100, self.animate_ascii)

    def create_input_controls(self):
        self.create_input_row("Input File/Folder:", self.browse_file, self.browse_folder)
        self.create_input_row("Output Directory:", self.browse_output)
        self.create_part_size_row()
        self.create_process_button()

    def create_input_row(self, label_text, *buttons):
        frame = ttk.Frame(self.controls_frame)
        frame.pack(pady=5, fill=tk.X, expand=True)
        
        label = ttk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT, padx=5)
        
        entry = ttk.Entry(frame, width=50)
        entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        for btn_command in buttons:
            btn = ttk.Button(frame, text=btn_command.__name__.replace('_', ' ').title(), 
                           command=btn_command)
            btn.pack(side=tk.LEFT, padx=2)
        
        if "File" in label_text:
            self.input_path = entry
        else:
            self.output_dir = entry

    def create_part_size_row(self):
        frame = ttk.Frame(self.controls_frame)
        frame.pack(pady=5, fill=tk.X, expand=True)
        
        label = ttk.Label(frame, text="Partition Size (MB):")
        label.pack(side=tk.LEFT, padx=5)
        
        self.part_size = ttk.Entry(frame, width=10)
        self.part_size.pack(side=tk.LEFT, padx=5)

    def create_process_button(self):
        frame = ttk.Frame(self.controls_frame)
        frame.pack(pady=10)
        
        self.process_btn = ttk.Button(frame, text="Process", command=self.start_processing)
        self.process_btn.pack()

    def browse_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.input_path.delete(0, tk.END)
            self.input_path.insert(0, path)

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.input_path.delete(0, tk.END)
            self.input_path.insert(0, path)

    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir.delete(0, tk.END)
            self.output_dir.insert(0, path)

    def log_message(self, message, color="white"):
        self.log_area.configure(state='normal')
        self.log_area.tag_config(color, foreground=color)
        self.log_area.insert(tk.END, message + "\n", color)
        self.log_area.configure(state='disabled')
        self.log_area.see(tk.END)
        self.root.update_idletasks()

    def generate_password(self, length=12):
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(chars) for _ in range(length))

    def _generate_checksum(self, file_path):
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def archive_folder(self, folder_path, output_dir):
        try:
            self.log_message("Archiving folder...", "blue")
            archive_name = f"{os.path.basename(folder_path)}_{int(time.time())}.rar"
            archive_path = os.path.join(output_dir, archive_name)
            patoolib.create_archive(archive_path, [folder_path], program='rar')
            return archive_path
        except Exception as e:
            self.log_message(f"Archive creation failed: {str(e)}", "red")
            self.log_message("Make sure you have RAR installed and in PATH", "orange")
            return None

    def partition_file(self, file_path, output_dir, chunk_size_mb):
        try:
            part_num = 1
            passwords = []
            checksums = []
            original_filename = os.path.basename(file_path)
            total_size = os.path.getsize(file_path)
            
            with open(file_path, 'rb') as file:
                while True:
                    chunk = file.read(chunk_size_mb * 1024 * 1024)
                    if not chunk:
                        break
                    
                    password = self.generate_password()
                    passwords.append(password)
                    
                    temp_file = os.path.join(output_dir, f"temp_part_{part_num}")
                    with open(temp_file, 'wb') as temp:
                        temp.write(chunk)
                    
                    checksum = self._generate_checksum(temp_file)
                    checksums.append(checksum)
                    
                    zip_file = os.path.join(output_dir, f"{os.path.splitext(original_filename)[0]}_part{part_num}.zip")
                    pyminizip.compress(temp_file, None, zip_file, password, 5)
                    os.remove(temp_file)
                    
                    self.progress['value'] = (file.tell() / total_size) * 100
                    part_num += 1
                    self.root.update_idletasks()

            passwords_with_metadata = [original_filename]
            for i, (p, cs) in enumerate(zip(passwords, checksums), 1):
                passwords_with_metadata.append(f"Part {i}: {p}|{cs}")
            
            passwords_encoded = base64.b64encode("\n".join(passwords_with_metadata).encode()).decode()
            with open(os.path.join(output_dir, "passwords.txt"), 'w') as pw_file:
                pw_file.write(passwords_encoded)
            
            self.log_message(f"Processed file split into {part_num - 1} ZIP parts. Passwords in passwords.txt", "green")
            messagebox.showinfo("Success", "Processing completed successfully!")
            
        except Exception as e:
            self.log_message(f"Error: {str(e)}", "red")
            messagebox.showerror("Error", str(e))
        finally:
            self.process_btn.config(state=tk.NORMAL)
            self.progress['value'] = 0

    def start_processing(self):
        input_path = self.input_path.get()
        output_dir = self.output_dir.get()
        
        if not input_path or not output_dir:
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        try:
            chunk_size = int(self.part_size.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid partition size")
            return
        
        if not os.path.exists(input_path):
            messagebox.showerror("Error", "Path not found!")
            return
        
        os.makedirs(output_dir, exist_ok=True)
        
        self.process_btn.config(state=tk.DISABLED)
        self.log_message("Starting processing...", "blue")
        
        threading.Thread(target=self.process_files, args=(input_path, output_dir, chunk_size), daemon=True).start()

    def process_files(self, input_path, output_dir, chunk_size):
        if os.path.isdir(input_path):
            archive_path = self.archive_folder(input_path, output_dir)
            if not archive_path:
                return
            file_to_process = archive_path
        else:
            file_to_process = input_path
        
        self.partition_file(file_to_process, output_dir, chunk_size)
        
        if os.path.isdir(input_path):
            try:
                os.remove(file_to_process)
                self.log_message("Temporary archive cleaned up", "blue")
            except Exception as e:
                self.log_message(f"Warning: Could not clean up temporary archive: {str(e)}", "orange")

if __name__ == "__main__":
    root = tk.Tk()
    app = FilePartitionerApp(root)
    root.mainloop()