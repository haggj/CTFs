# Blind SQL Injection

The server suffers from SQL injection vulnerabilities, but the user does not only receive binary feedback from the server
(e.g. if a user with the requested ID exists or not).
This information can be used to extract information from the database.

The script `blind_sqli.py` can be used to extract the password of the users from the database.
It can be adjusted to extract other information as well.
For different security levels, different payloads are used and different requests (GET, POST, etc) are required.
The techniques are the same as for the SQL injection vulnerabilities.

## Low
Use the following payload to perform a blind SQL injection:
```bash
f"22' or (first_name = '{first_name}' and password like '{extracted+char}%'); -- "
```
