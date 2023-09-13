from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import requests
import base64



'''
Computation of signature in server is vulnerable to length extension attacks.
The server uses a custom hash, where the padded input data is split into blocks.
Each block is encrypted via AES in ECB mode with the previous encrypted block as key.

The attacker can still compute and restore the internal state of the hash function.
In fact, the given hash is the internal state.
The attacker can then append data to the original data and compute the new hash without knowing the secret.
This is realized in length_extension().

The functions pad, compression_function and lj12_hash are copied from the server to locally test the exploit.
'''


BLOCK_LEN = 32
SECRET = 50*b"s"

iv = b"@\xab\x97\xca\x18\x1d\xac<\x1e\xc3xC\x9b\x1c\xc5\x1f\x8aD=\xec*\x16G\xe7\x89'\x80\xe4\xe6\xfc5l"


def pad(data : bytes):
    if len(data) % BLOCK_LEN == 0:
        return data

    pad_byte = bytes([len(data) % 256])
    pad_len = BLOCK_LEN - (len(data) % BLOCK_LEN)
    data += pad_byte * pad_len

    return data


def compression_function(data, key):
    if len(data) != BLOCK_LEN or len(key) != BLOCK_LEN:
        raise ValueError(f"Input for compression function is not {BLOCK_LEN} bytes long!")

    # AES is a safe compression function, right? Why not just use that?
    cipher = AES.new(key, AES.MODE_ECB)
    enc = cipher.encrypt(data)

    # let's confuse it up a bit more, don't want to make it too easy!
    enc = enc[::-1]
    enc = enc[::2] + enc[1::2]
    enc = enc[::3] + enc[2::3] + enc[1::3]


    return enc
     

def lj12_hash(data):
    padded = pad(data)


    blocks = [padded[x:x + BLOCK_LEN] for x in range(0, len(padded), BLOCK_LEN)]
    enc_block = iv

    for i in range(len(blocks)):
        enc_block = compression_function(blocks[i], enc_block)

    return enc_block.hex()


def length_extension(iv : str, data : str, append : str):
    faked_secret = b"s"*50

    initial_padded_data = pad(faked_secret + data.encode()) 
    forged_padded_data = pad(initial_padded_data + append.encode())
    to_encrypt = forged_padded_data[len(initial_padded_data):]


    blocks = [to_encrypt[x:x + BLOCK_LEN] for x in range(0, len(to_encrypt), BLOCK_LEN)]
    enc_block = bytes.fromhex(iv)

    for i in range(len(blocks)):
        enc_block = compression_function(blocks[i], enc_block)

    return initial_padded_data[50:].decode() + append, enc_block.hex()


def test_length_extension():

    key = b"k" * 32

    # original hash without knowledge of SECRET
    data = 'user_id=guest&isLoggedIn=False'
    hash = lj12_hash(SECRET + data.encode())

    # length extension without knowledge of SECRET
    forged_data, forged_hash = length_extension(hash, data, "&isLoggedIn=True")
    # verify forged data with knowledge of SECRET
    assert lj12_hash(SECRET + forged_data.encode()) == forged_hash


SERVER = "http://206.189.23.108:31509"
#SERVER = "http://127.0.0.1:1337"

def info(msg):
    print("[*] " + msg)

def success(msg):
    print('\033[92m' + "[+] " + msg + '\033[0m')

test_length_extension()

sess = requests.session()
sess.get(SERVER + "/")

data, sig = sess.cookies.get("login_info").split(".")

info("old data: " + data)
info("old sig : " + sig)


forged_data, forged_sig = length_extension(sig, data, "&isLoggedIn=True")

#forged_data = "user_id=guest&isLoggedIn=FalsePPPPPPPPPPPPPPPP&isLoggedIn=True"
forged_cookie = forged_data + "." + forged_sig

success(str(len(forged_data)))

info("forged data: " + str(forged_data))
info("forged sig: " + str(forged_sig))
success("forged cookie: " + forged_cookie)

info("Sending forged cookie...")
sess.cookies.clear()
sess.cookies.set("login_info", forged_cookie)
res = sess.get(SERVER + "/program", proxies={"http": "http://localhost:8080"})
with open("flag.pdf", "wb") as f:
    f.write(res.content)
    success("Done: Flag in flag.pdf :-)")

test_length_extension()

