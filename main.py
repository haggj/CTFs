out = "灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸弰㑣〷㘰摽"

flag = ""
for i in range(len(out)):
    first = (ord(out[i]) >> 8)
    second = ord(out[i]) & 255
    flag += chr(first) + chr(second)

print(flag)
#
# flag = "abcd"
# print([flag[i] + flag[i+1] for i in range(0, len(flag), 2)])
#
# out = ''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])
# print(out)