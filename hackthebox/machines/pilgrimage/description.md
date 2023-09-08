# Pilgrimage

## User flag

1. Nmap reveals a git repo under `http://pilgrimage.htb/.git`.
2. Downloaded the repo using [git-dumper](https://github.com/arthaud/git-dumper).
3. The git repo contains the source code.
4. The application uses [magick](https://github.com/ropensci/magick), the used binary is part of the git repo (version 7.1.0).
5. This version of magick is vulnerable to [CVE-2022-44268](https://github.com/voidz0r/CVE-2022-44268), which allows to leak files from server ([lfi.py](lfi.py))
6. The source code shows the full path of a sqlite databse at `/var/db/pilgrimage`. Using the lfi script to download and store the database locally.
7. Found credentials for user `emily:abigchonkyboi123` in users table.

## System flag

1. Downloaded pspy64 to obesrve commands run on the system.
2. Detected a cronjob/script `malwarescan.sh` which observes all files in `/var/www/pilgrimage.htb/shrunk`. If any file in this folder is changed, the script checks if the changed file is malware. The script runs with root privileges.
3. The malware check uses `binwalk` version `2.3.3` which is vulnerable to [CVE-2022-4510](https://nvd.nist.gov/vuln/detail/CVE-2022-4510). This allows specifically crafted png files to trigger RCE.
4. Used [this repo](https://github.com/adhikara13/CVE-2022-4510-WalkingPath) to create malicious png which triggers RCE.
5. Upload malicious png to `/var/www/pilgrimage.htb/shrunk` to trigger the malware scan and exploit the vulnerability in `binwalk`.