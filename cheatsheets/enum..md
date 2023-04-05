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

## SQLInjection
Basic injections to test for strings:
- `bla' or 1=1; -- `
- `bla" or 1=1; -- `
- `bla' or 1=1; # `
- `bla" or 1=1; # `

Use sqlmap the following way if the string is closed via `"` ([details](https://github.com/sqlmapproject/sqlmap/wiki/Usage#custom-injection-payload))
```
sqlmap http://host.de/?para=anything --prefix'"'
```