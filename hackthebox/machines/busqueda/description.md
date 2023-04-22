# Busqueda
Writeup of Busqueda challenge provided by hackthebox.

# User flag
The websites wraps [searchor 2.4.0](https://github.com/ArjunSharda/Searchor) to build search urls.
This version suffers from a [remote code execution](https://github.com/ArjunSharda/Searchor/pull/130) vulnerability in its cli.
This allows an attacker to run arbitrary python commands and to receive a reverse shell (see [reverse_shell.py](reverse_shell.py)).

The web application is stored in `/var/www/app`. 
This directory contains a git repository, which can be used to leak the following information:
- There is a gitea server running at `gitea.searcher.htb`
- The user `cody` uses password `jh1usoih2bkjaspwe92` to authenticate against this server

This password also allows ssh login to the user `svc/jh1usoih2bkjaspwe92`, which yields the user flag.

# Root flag
The user `svc` is allowed to run the following commands as root without password:

```
sudo /usr/bin/python3 /opt/scripts/system-checkup.py
```

It is not possible to see the source code of this script.
However, by executing it we get help information. The script allows us to examine running docker containers.
We can list running docker containers and inspect them (`docker ps` and `docker inspect`).
The results of the inspect commands are stored in [gitea.json](gitea.json) and [mysql.json](mysql.json).
They yields some credentials for the servers:
- found database credentials: `gitea/yuiu1hoiu4i5ho1uh`
- mysql root password: `jI86kGUuj87guWr3RyF` 

Further investigated the gitea server, which has a user `administrator`.
We can login to this user using the credentials `administrator/yuiu1hoiu4i5ho1uh`.
This gives access to the source code of all scripts in `/opt/scripts`.
The script `system-checkup.py` contains the following code:
```python
...
    elif action == 'full-checkup':
        try:
            arg_list = ['./full-checkup.sh']
            print(run_command(arg_list))
            print('[+] Done!')
        except:
            print('Something went wrong')
            exit(1)
...
```

We can create an arbitrary script `full-checkup.sh` in any directory, which extracts the root flag.
Then, we can invoke it by running:

```bash
# cd into the directory of the malicious full-checkup.sh
cd ...
# run privileged command to invoke the malicious script
sudo /usr/bin/python3 /opt/scripts/system-checkup.py full-checkup
```

Since this script is executed as root, it can read the root flag.