# Enumeration 

## nmap

Quick scan
```bash
nmap <ip> --top-ports 30
```

Default scan
```bash
nmap <ip> -sV -sC
```

Detailed scan
```bash
nmap <ip> -p-
```

## Directory enumeration
```
gobuster dir -u <url> -w <wordlist>
```

## Domain enumeration
```
gobuster dns -d <domain> -w <wordlist>
```

## Vhost enumeration

```
gobuster vhost -u <url> --apend-domain -w <wordlist>
```

[ffuf scans much faster using HOST header](http://ffuf.me/sub/vhost)