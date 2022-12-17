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

