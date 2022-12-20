# Transformation

## Analysis

We are given a string containing Chinese characters.
We also received the python code which produced this string based on a given flag.

## Solution

The flag was split up into junks of two characters.
Bot characters are interpreted as integer values.
The numeric value of the first character is shifted by 8 digits to the left (binary shift).
The resulting value is added to the numeric value of the second character.
The resulting value is finally interpreted as character again.

The following python script decrypts the flag based on the described encryption:

```python

out = "灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸弰㑣〷㘰摽"

flag = ""
for i in range(len(out)):
    first = (ord(out[i]) >> 8)
    second = ord(out[i]) & 255
    flag += chr(first) + chr(second)

print(flag)
```