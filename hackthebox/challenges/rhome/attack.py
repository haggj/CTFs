from Crypto.Util.number import isPrime, long_to_bytes, getPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from random import randint
from hashlib import sha256
from sympy import factorint
from sympy.ntheory import discrete_log
import socket
import time

SERVER = ("206.189.23.108", 30305)

def info(message):
    print(f"[+] {message}")

def attack(p, g, A, B):
    '''
    We can attack the DH protocol because of the way the generator g is chosen.
    It is not a primitive root of p, which means that the order of g is not p-1.
    As a result, the possibly generated values of g (= order of g) are smaller than p-1.
    In this scenario, the order of g always seems to be q, which is not known but can be computed by factoring p-1.
    The small order of g allows us to compute the discrete log of A and B efficiently.
    NOTE: There is no need to compute the order of g explicitly, but it speeds up the computation of `discrete_log`.
    '''
    # 1. Find prime factors of p-1
    factors = factorint(p-1)
    info("Prime factors are: " + str(list(factors.keys())))

    # 2 . Find order of g
    for factor in factors.keys():
        if pow(g, factor, p) == 1:
            order_of_g = factor
            info("Order of g is: " + str(order_of_g))
            break
    
    # 3. Find discrete log of A and B
    a = discrete_log(p, A, g, order_of_g)
    info("Discrete log of A is: " + str(a))

    # 4. Compute shared secret
    ss = pow(B, a, p)
    info("Shared secret is: " + str(ss))
    return ss

def decrypt(ss, ct):
    key = sha256(long_to_bytes(ss)).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    pt = cipher.decrypt(bytes.fromhex(ct))
    return unpad(pt, 16)


# Connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER)
time.sleep(1)
s.recv(4096)
info("Connected to server")

# Get parameters
s.send(b"1\n")
time.sleep(1)
params = s.recv(4096).split(b"\n")
p = int(params[0].split(b" = ")[1].strip())
g = int(params[1].split(b" = ")[1].strip())
A = int(params[2].split(b" = ")[1].strip())
B = int(params[3].split(b" = ")[1].strip())
info("p = " + str(p))
info("g = " + str(g))
info("A = " + str(A))
info("B = " + str(B))

# Get encrypted flag
s.send(b"3\n")
time.sleep(1)
data = s.recv(2048).split(b"\n")
encrypted_flag = data[0].split(b" = ")[1].decode()
info("Encrypted flag: " + str(encrypted_flag))

# Compute shared secret
ss = attack(p, g, A, B)
info("Shared secret: " + str(ss))

# Decrypt flag
flag = decrypt(ss, encrypted_flag)
info("Flag: " + str(flag))