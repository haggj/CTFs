
def decryption(ct):
    pt = []
    for char in ct:
        # compute the inverse of 123 modulo 256: pow(123, -1, 256)
        dec = ((char - 18) * pow(123, -1, 256)) % 256
        pt.append(dec)
    return bytes(pt)

ct = bytes.fromhex(open('msg.enc', 'r').read())
print(decryption(ct))



