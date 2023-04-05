# Web weather app

## Description
The web weather app is a simple web application.
It suffers from two vulnerabilities:
- The application is vulnerable to a SQL injection (`/register`).
- The application suffers from a SSRF via request splitting (`api/weather`), [details](https://www.rfk.id.au/blog/entry/security-bugs-ssrf-via-request-splitting).

## Solution
We can not directly exploit the SQL injection, since the application does only allow requests originating from `127.0.0.1` to call the `/register` endpoint.
However, we can exploit the SSRF vulnerability to send a request to the `/register` endpoint.
This is done by using a technique called reqeust splitting:
- Due to invalid character encoding in node version <= 8, unicode characters will be passed down to where the raw http requests are sent to the wire.
- Before they are sent into the TCP connection they are ``latin1`` decoded. This decoding ignores the upper byte. E.g. ``0x00ff`` will be decoded to ``0xff``.
- This allows the attacker to control the raw HTTP request. As a result, the attacker can define arbitrary HTTP requests sent via the vulnerable server.

The script `exploit.py` exploits this vulnerability and crafts a POST request to the `/register` endpoint.
This requests contains a SQL injection which resets the password of the user `admin` to `admin`.
Finally, we can log in as `admin` and retrieve the flag.

