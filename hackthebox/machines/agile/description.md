# Agile

This is a writeup for the machine Agile from hackthebox.

# User flag
There are two vulnerabilities in the application:
1. Local file inclusion, which allows to investigate the application.
2. The application enables the Werkzeug debugger, which allows to execute arbitrary python code if the debugger pin can be reconstructed.

## 1. Local file inclusion
Service running at `superpass.htb` suffers from a local file inclusion vulnerability for authenticated users:
```
http://superpass.htb/download?fn=../../../../../../etc/passwd
```
This allows to extract the source code of the application, which is a flask application.
The script `fi_download.py` can be used to mirror/download the files from the server.
Interesting files to leak:
- `/etc/passwd`
- `/proc/self/environ`: yields config file path `/app/config_prod.json`
- `/app/config_prod.json`: yields sql credentials
- `/app/app/superpass/views/vault_views.py`
- `/app/app/superpass/app.py`

This allows to investigate the application and find the second vulnerability.


## 2. Werkzeug debugger
The application shows the Werkzeug debugger if exceptions are raised.
This debugger is initialized with `evalex` set to `True`.
This enables the exception evaluation feature (can be used to execute arbitrary python code).
To use this feature, the Werkzeug pin needs to be known (this pin gets printed to stdout during startup).
Since the stdout could not be leaked, the pin needs [to be reconstructed](https://www.bengrewell.com/cracking-flask-werkzeug-console-pin/).
This is realized in the script `werkzeug_pin.py`.
The following combination is successful: 

```python
('www-data', 'flask.app', 'wsgi_app', '/app/venv/lib/python3.10/site-packages/flask/app.py', '345052366754', 'ed5b159560f54721827644bc9b220d00superpass.service')
```

The provided python console can be used to leak credentials of the user `corum` in the superpass database: `corum/5db7caa1d13cc37c9fc2`

This enables ssh login and gives the user flag.

# Root flag

The following steps are required to obtain the root flag:
1. Leak the credentials of the user `edwards` in the superpass database.
2. Exploit `sudoedit` vulnerability to write to extract the root flag.

## 1. Leak credentials of user `edwards`

Besides the application in `/app/app` there is a second application in `/app/app-testing`.
The readme tells that a cronjob copies the files from `/app/app-testing` to `/app/app` if all tests pass.
There are credentials loaded from `/app/app_testing/tests/functional/creds.txt` during the tests.
They can neither be read by the user `corum` nor can they be leaked by the LFI vulnerability, because this has been patched.
The tests rely on selenium and start a chrome instance which has remote debugging enabled.
This allows to connect to the chrome instance running on the target during the tests:
- forward port `41829` from the htb host to your local machine:
   ```ssh -L 41829:localhost:41829 corum@superpass.htb```
- visit `http://localhost:41829/json` in your browser, which shows the link to the remote dev tools
- visit the link in your browser, to see the browser controlled by the unittests
- this leaks the system credentials for user edwards: `edwards/d07867c6267dcb5df0af`

## 2. Exploit `sudoedit` vulnerability

The user `edwards` is allowed to run `sudoedit` as `dev_admin` to edit two files (`config_test.json` and `creds.txt`).
This alone, however, is not helpful for privesc.
The system is vulnerable to [CVE-2023-22809](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-22809), which allows to write to arbitrary files as `dev_admin` by using `sudoedit` with the `EDITOR` environment variable set to `nano -- /path/to/file`.
This can be used to obtain the root flag:
1. A cronjob runs every minute and executes tests in `/app/app-testing`. This cronjob is owned by root.
2. The cronjob activates the virtual environment in `/app/venv` before the tests are run.
3. The script `/app/venv/bin/activate` can is writable by `dev_admin`.

We can modify the script `/app/venv/bin/activate` to copy the flag to a file in `/tmp`:

```bash
# command to exploit CVE-2023-22809 and modify /app/venv/bin/activate
EDITOR="nano -- /app/venv/bin/activate" sudoedit -u dev_admin /app/config_test.json

# command added to /app/venv/bin/activate
cat /root/root.txt > /tmp/root.txt && chmod 777 /tmp/root.txt;
```