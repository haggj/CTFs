# Precious

## Analysis

- nmap scan reveals open ports `80` and `22`
  - ssh version `OpenSSH 8.2p1 Ubuntu 4ubuntu0.5`
  - webserver running `nginx 1.18.0`
    - nothing interesting on default webpage
    - dirbuster found tiny file manger `http://soccer.htb/tiny/`
      - login with default creds `admin/admin@123`
      - vulnerabilites found


## Solution

### User flag

- We can upload any php files, but they are deleted after a few minutes.
- Uploaded a simply php webshell to receive a reverse shell. 
  This task is automated in `stage1_shell.py`. 
  Logged in as ``www-data`` but this does not yield a flag.
  Digging around the nginx config files shows that there is another service running at `http://soc-player.soccer.htb`
- This second server allows to register a account.
  A logged-in user is allowd to retrieve ticket ids using a websocket connection.
  This websocket connection suffers from a SQL injection (i.e. `1 or 1=1` returns a valid result).
  We are facing a blind SQL injection.
- There are two approaches of extracting data:
  - First, manually enumerate the databse. This is done in `blind_sql.py`
  - Second, use `sqlmap` to exploit the vulnerability. 
    This requires some sort of intermediate server, since `sqlmap` can not talk to websockets by default.
    See [this post](https://rayhan0x01.github.io/ctf/2021/04/02/blind-sqli-over-websocket-automation.html) for details.
    To realize this attack, first start `sqlmap_server.py` and then launch `sqlmap -u http://localhost:8081?a=1 --dump`
  - Both ways yield the password for user `player`: `PlayerOftheMatch2022`
- This password allows to log in via ssh and gives the user flag.


### System flag
- Found binary `doas` with suid bit set. Enumerated settings and found that `player` is allowed to run `dstat` commands as root.
- `dstat` allows to specify python plugins which can be exploited to spawn a shell (see gtfobins)
- The following commandy yield a root shell:

```bash
echo 'import os; os.execv("/bin/sh", ["sh"])' > /usr/local/share/dstat/dstat_xxx.py
doas /usr/bin/dstat --xxx
```
