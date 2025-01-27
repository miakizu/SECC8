# SECC8 - File Partitioning, Encryption, and Decryption Tool

**SECC8** is a Python-based tool designed to partition, encrypt, and decrypt large files. It is particularly useful for splitting large files into smaller, manageable parts and securing them with encryption. This tool was created for legitimate use cases, such as securely sharing large files or backing up sensitive data.

---

## **Important Notes**
- **You must install the following dependencies before using SECC8:**
  ```bash
  pip install colorama
  pip install rarfile
  pip install tqdm
  ```

- **Disclaimer:**  
  This tool is intended for legal and ethical use only. As the author, I am **not liable** for any misuse or malicious activities conducted with this software. Use it responsibly.

---

## **How It Works**
SECC8 allows you to:
1. Partition large `.rar`, '.zip', and '.7z' files into smaller chunks (e.g., 500MB each).
2. Encrypt the partitioned files.
3. Decrypt and reassemble the files into their original form.

### Example Use Case:
1. You have a 100GB file named `crazyman.rar` located in `C:\when`.
2. You use SECC8 to partition `crazyman.rar` into 500MB parts and save them to `C:\now`.
3. You upload each 500MB file **along with the `PASSWORDS.txt` file** to a file-sharing service like MultiUp.
4. You provide instructions to the recipient on how to decrypt and extract the files.
5. The recipient downloads all 500MB files **and the `PASSWORDS.txt` file**.
6. The recipient uses SECC8's decryption tool to extract the contents of `crazyman.rar`.

---

## **Current Version: 1.0**
The current version of SECC8 is functional but has some limitations:
- **Buggy:** Expect some issues during use.
- **No GUI:** The tool is command-line only.
- **Limited File Support:** Only `.rar` files are supported for partitioning and encryption.

---

## **Planned Updates**
- Support for additional file formats
- Ability to partition and encrypt folders directly (eliminating the need to manually compress folders into archive files first).
- Improved error logging for easier debugging.
- A sleek and user-friendly GUI.

---

## **VirusTotal Scans**
For your peace of mind, here are the VirusTotal links for the tool's components (V1.0):
- **Decrypter:** [VirusTotal Scan](https://www.virustotal.com/gui/file/743c43db4e878466fe080092e1480e593f0f72b74be707fe4d1cd4faa064cec5)
- **Encrypter:** [VirusTotal Scan](https://www.virustotal.com/gui/file/b254baa4d0c8a431774944a1f1b8d363a6b0961a35597864b0d73b5b94175491)

---

## **Getting Started**
1. pip install required dependencies
2. use the partencrypter.py to encrypt a big rar file into smaller parts
3. upload parts and decrypter.py to necessary locations
4. instruct the recipient to use the decrypter to unpack their file

---

## **Final Note**
This tool was created as a fun project, and while it may have been written in a less-than-sober state, it has been tested and refined to the best of my ability. Feedback and contributions are welcome!
