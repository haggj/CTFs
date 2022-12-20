# keygenme-py

## Analysis

This challenge provides a python script.
Upon execution, we only can use a limited version unless we enter a correct key.
Checking the source code revels that part of the flag are hidden.

## Solution

In order to enter a correct license key, the user must input the flag.
The  hidden parts of the flag can be restored with the following python snipped.
It hashes the username specified in the python code, and assembles the resulting character in the correct way (as given by the key verification function):

```python
import hashlib
hash = hashlib.sha256("PRITCHARD".encode()).hexdigest()
print(a[4]+a[5]+a[3]+a[6]+a[2]+a[7]+a[1]+a[8])
```