# SECC8 - File Partitioning, Encryption, and Decryption Tool

**SECC8** is a Python-based tool designed to partition, encrypt, and decrypt large files. It is particularly useful for splitting large files into smaller, manageable parts and securing them with encryption. This tool was created for legitimate use cases, such as securely sharing large files or backing up sensitive data.

---

## **Important Notes**
- **You must install the following dependencies before using SECC8:**
  ```bash
  pip install colorama
  pip install rarfile
  pip install tqdm
  pip install tk
  ```

- **Disclaimer:**  
  This tool is intended for legal and ethical use only. As the author, I am **not liable** for any misuse or malicious activities conducted with this software. Use it responsibly.

---

## **How It Works**
SECC8 allows you to:
1. Partition large `.rar`, `.zip`, and `.7z` files into smaller chunks (e.g., 500MB each).
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

## **Current Version: 2.0**
The current version of SECC8 is functional but has some limitations:
- **Buggy:** Expect some issues during use.

## **Upcoming Updates**
SECC8 has a few more possible updates before being marked as completed. As of this descriptions update, our current priority is:
- *Checksum Verification and Capability:* Verify file integrities before attempting to recreate file. Also, if you are using an old version of the encrpyter that does not utilize the checksum method yet, newer versions of the decrpyter will retain compatability and be able to skip checksum verification.
- *Fully Encrypted Passwords File:* The plan to add encrypted JSON files to store passwords instead of the current simple base64 encryption.
- *Password Functionalities:* Ability to put a "Master Pass" that is needed in order to access the passwords file, enhancing security and ensuring nobody can access it without the key.
- *Localization:* Branches of the project will be made with localizations for other languages. After V3 is released, we will create a German, Russian, and Portugese localization. We would love for the community to create localizations for other langugaes to bring the community more together and ensure accuracy.
- *Promotion:* Less of a code update, but we plan to advertise the tool more in order to gain popularity and a user base.
- *Fully Open Source:* In an early stage of development, some parts of code were encrypted with base64 that really didn't need to be, as they were easily decryptable and they were not necessary to enhance security. With the release of V3 we plan to make practically all the code accessible to ensure people can read at their own leisure for peace of mind.
- *Collaboration:* We are currently reaching out to other coders to speed up development and get more ideas. If you would like to contribute, you can add me on discord with the button below:
  
[![Add Me on Discord](https://img.shields.io/badge/Discord-Add%20Me-blue?style=for-the-badge&logo=discord)](https://discord.com/users/1324459975464063067)
---

## **VirusTotal Scans**
Here are the VirusTotal links for the tool's (V1.0):
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
