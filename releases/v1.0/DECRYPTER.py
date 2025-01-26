import os, pyminizip, base64, re, shutil, rarfile, logging
from colorama import Fore, Style, init; init()
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
logging.basicConfig(filename=l, level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
a = lambda t: print(Fore.CYAN + "=" * 60 + "\n" + t.center(60) + "\n" + "=" * 60 + Style.RESET_ALL)
b = lambda t: print(Fore.RED + "⚠ " + t + " ⚠" + Style.RESET_ALL)
c = lambda t: print(Fore.GREEN + "✔ " + t + " ✔" + Style.RESET_ALL)
d = lambda t: print(Fore.BLUE + "ℹ " + t + Style.RESET_ALL)
e = lambda m, x=None: (logging.error(f"{m}: {str(x)}", exc_info=True) if x else logging.error(m), b(f"An error occurred. Details have been logged to {l}."))
def f(r, x):
    try:
        with rarfile.RarFile(r) as rf: rf.extractall(path=x)
        d(f"Extracted {r} to {x}.")
    except Exception as ex: e(f"Failed to extract {r}", ex)
def g(x):
    try:
        i = os.listdir(x)
        if len(i) == 1 and os.path.isdir(os.path.join(x, i[0])):
            n = os.path.join(os.path.dirname(x), i[0])
            os.rename(x, n)
            d(f"Renamed {x} to {n}.")
            return n
        else:
            n = os.path.join(os.path.dirname(x), "contents")
            os.rename(x, n)
            d(f"Renamed {x} to {n}.")
            return n
    except Exception as ex: e("Failed to rename folder", ex)
    return x
def h(fld, ext):
    try:
        p = os.path.join(fld, "passwords.txt")
        if not os.path.isfile(p):
            b(s4)
            e("Password file not found")
            return
        with open(p, 'r') as pw:
            u = base64.b64decode(pw.read()).decode().split('\n')
            d("Decoded passwords: " + ", ".join(u))
        a("Determining Number of Parts...")
        d(s3)
        z = sorted([x for x in os.listdir(fld) if re.match(r".+_part\d+\.zip", x)], key=lambda x: int(re.search(r"_part(\d+)\.zip", x).group(1)))
        n = len(z)
        if n != len(u):
            b(s4)
            e("Number of parts does not match number of passwords")
            return
        if not os.path.exists(ext): os.makedirs(ext)
        a("Extracting Parts...")
        d(s5)
        err = False
        for i in range(n):
            zf = os.path.join(fld, z[i])
            pw = u[i].split(': ')[1]
            d(f"Extracting {z[i]} with password: {pw}")
            try:
                pyminizip.uncompress(zf, pw, ext, 0)
                d(f"Extracted {z[i]} successfully.")
            except Exception as ex:
                e(f"Failed to extract {z[i]}", ex)
                err = True
        a("Reconstructing the Original File...")
        try:
            o = os.path.join(ext, "reconstructed_file.rar")
            with open(o, 'wb') as of:
                for i in range(1, n + 1):
                    pf = os.path.join(ext, f"{os.path.splitext(z[0])[0].rsplit('_part', 1)[0]}_part{i}_data")
                    with open(pf, 'rb') as inf: shutil.copyfileobj(inf, of)
                    os.remove(pf)
            d(f"Reconstructed file saved as {o}.")
            b("\nDO NOT CLOSE. NOT FINISHED.\n")
            xf = os.path.join(ext, "extracted_contents")
            if not os.path.exists(xf): os.makedirs(xf)
            f(o, xf)
            nf = g(xf)
            os.remove(o)
            d(f"Deleted {o} as it is no longer needed.")
            if not err: c("\nEXTRACTION SUCCESSFUL!\n")
        except Exception as ex:
            e("Failed to reconstruct the original file", ex)
            err = True
        if err: b(s7)
        else: d(s6.format(nf))
    except Exception as ex: e("An unexpected error occurred", ex)
def main():
    try:
        a("SECT8 Decrypter")
        fld = input(s1).strip('"')
        ext = input(s2).strip('"')
        h(fld, ext)
    except Exception as ex: e("An unexpected error occurred", ex)
    input(s8)
if __name__ == "__main__": main()
