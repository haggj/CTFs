# Injection

## Analysis

- nmap scan reveals open ports `8080` and `22`
  - ssh version `OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)`
  - webserver running ``

### Webserver
- signup/login do not work
- allows image upload `http://10.10.11.204:8080/upload`
- images can be viewed `http://10.10.11.204:8080/show_image?img=Chart%20Title.png`
  - this suffers from directory traversal: `http://10.10.11.204:8080/show_image?img=../../../../../../../../../../../etc/passwd`
    - requested file is included into response!
  - uploaded images are deleted after few minutes


## Solution

### User flag

- found three users, which are allowed to log in to the machine: ``phil``, ``frank`` and ``root``
- found `pom.xml` of spring project: `http://10.10.11.204:8080/show_image?img=../../../pom.xml`
  - reveals that spring cloud function ``3.2.2`` was used
  - this spring version is vulnerable to [RCE](https://www.lunasec.io/docs/blog/spring-rce-vulnerabilities/#cve-2022-22963)
  - stable shell can be obtained by the attacker script in [this repo](https://github.com/iliass-dahman/CVE-2022-22963-POC)
- password for user `phil` can be found in `/home/frank/.m2/settings.xml`: `DocPhillovestoInject123`
- user flag in `/home/phil/user.txt`

### Root flag
- tool `pspy` showed, that machine is running [ansible](https://www.ansible.com/) to automate tasks
- the folder containing the playbooks `/opt/automation/tasks` is writable by group `staff`
- the scripts stored there are executed every 2 minutes
- the following task copies the root flag to the directory of the user:
```yaml
- hosts: localhost
  become: yes
  tasks:
  - name: copy flag
    copy:
      src: /root/root.txt
      dest: /home/phil/root
      mode: 0777
```


DocPhillovestoInject123