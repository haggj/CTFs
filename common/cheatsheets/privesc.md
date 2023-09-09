# Privilege Escalation

## Tools

**Linux smart enumeration**

https://github.com/diego-treitos/linux-smart-enumeration

**Pspy**

https://github.com/DominicBreuker/pspy


## Hash cracking

**Hash-identifier**
```bash
# Identify hash type
hash-identifier <hash>
```

**John the Ripper**
```bash
# Cracking passwords in hash.txt with rockyou.txt
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt [--format=raw-md5]
# Show cracked passwords
john hash.txt --show [--format=raw-md5]
```

**Hashcat**
```bash
# Cracking passwords in hash.txt with rockyou.txt
hashcat hash.txt /usr/share/wordlists/rockyou.txt -a 0 [-m 0]
# Show cracked passwords
hashcat --show hash.txt [-m 0]
```
```