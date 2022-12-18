encoded_flag = b"xakgK\x5cNs((j:l9<mimk?:k;9;8=8?=0?>jnn:j=lu\x00\x00"
flag = ""

for char in encoded_flag:
    flag += chr(char ^ 8)
print(flag.strip())
