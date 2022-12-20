# Shop

## Analysis

- we can interact with a *shop* via command line
- we can not obtain the flag because we only have 40 coins, but the flag costs 100 coins
- the challenge provides us with the binary source file

## Solution

- `file source` gives the information that we are faced with a 32-bit ELF binary
- `strings source` does not yield the flag
- Playing around with the application gives the insight that one can buy a negative amount of articles
- This increases the number of available coins, e.g. buying -10 apples yield additional 150 coins
- This allows us to obtain the flag, which is encoded into integers and can be restored using python:
```python
encoded ="112 105 99 111 67 84 70 123 98 52 100 95 98 114 111 103 114 97 109 109 101 114 95 98 97 54 98 56 99 100 102 125"
flag = "".join(chr(int(value)) for value in encoded.split(" "))
print(flag)
```