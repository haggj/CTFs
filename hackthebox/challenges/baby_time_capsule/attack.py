import socket
import json
from Crypto.Util.number import long_to_bytes

from functools import reduce


def chinese_remainder(m, a):
    sum = 0
    prod = reduce(lambda acc, b: acc * b, m)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


def load_capsule():

    n = []
    a = []

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('209.97.140.29', 30988))

    for _ in range(3):
        s.recv(1024)
        s.send(b'Y\n')
        capsule = json.loads(s.recv(1024))
        a.append(int(capsule['time_capsule'], 16))
        n.append(int(capsule['pubkey'][0], 16))

    return n, a

def iroot(k, n):
    u, s = n, n+1
    while u < s:
        s = u
        t = (k-1) * s + n // pow(s, k-1)
        u = t // k
    return s

n, a = load_capsule()
print("Loaded values, compute CRT...")

x = chinese_remainder(n, a)
print(x)
print(long_to_bytes(iroot(5, x),16))
