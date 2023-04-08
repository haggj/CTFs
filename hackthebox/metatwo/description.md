https://0xdedinfosec.vercel.app/blog/hackthebox-metatwo-writeup

# Metatwo

## Enumeration

Machine has two open ports (80/http, 22/ssh).
Webserver is running WordPress `5.6.2`, but no login with default credentials.
Investigating the WordPress plugin running at endpoint `/event` reveals malicious plugin `bookingpress` which allows SQLi.


## User flag
- The malicious plugin allows SQLi ([CVE-2022-0739](https://wpscan.com/vulnerability/388cd42d-b61a-42a4-8604-99b812db2357)).
Used the malicious [raw http payload](sqli.req) and passed it to sqlmap.
This dumps the database including the users table.
- The password of user `manager` can be cracked via hashcat: `partylikearockstar`
The admin password was not cracked.
- After login as ``manager`` in turned out that we can upload files to WordPress.
Research shows that this WordPress version suffers from [CVE-2021-29447](https://github.com/motikan2010/CVE-2021-29447) which allows to read files from the server.
This repo also contains a python script to automate the exploit.
- Leaked user `jnelson`. NGINX config gives path to application which allows to read the wp config file `/var/www/metapress.htb/blog/wp-config.php`.
This file contains ftp credentials `metapress.htb/9NYS_ii@FyL_p5M2NvJ`.
- Login to ftp server. Found file `send_email.php` which contains a password for user `jnelson/Cb4_JmWM8zUZWMu@Ys`.
This allows ssh login as user `jnelson`.

## System flag

- Enumerating user directory shows that [passpie](https://github.com/marcwebbie/passpie) is used.
The database contains two entries: `root` and `jnelson`. 
The access to Passpie is protected by a password (login information of `jnelson` did not work).
Passpie follows this encryption protocol:
    - The master password encrypts GPG keys file (located at `~/.passpie/.keys`)
    - This GPG keys are used to encrypt the actual passwords. Passpie entries are stored in `~/.passpie/ssh` along with the GPG cipher and other information about the entry.

- The GPG keys file is encryted with a master password.
It can be cracked using john: 
    ```
    # extract data from encrypted keys
    john2gpg .keys > data
    # run john on data (no wordlists requried to break this)
    john data
    ```
  This gives the password `blink182`
- We can obtain the root password from the Passpie database:
    ```
    passpie copy --to stdout --passphrase blink182 root@ssh
    ```
