# vault-door-1

## Analysis

- We are given a Java source code file which contains the obfuscated flag
- The `check_password` function expects a input and compares it character by character with the flag
- The comparison, however, is obfuscated because it is not in order

## Solution

- The following python snipped restores the flag from the given character-wise comparison:
````python

source = """   password.charAt(0)  == 'd' &&
               password.charAt(29) == '9' &&
               password.charAt(4)  == 'r' &&
               password.charAt(2)  == '5' &&
               password.charAt(23) == 'r' &&
               password.charAt(3)  == 'c' &&
               password.charAt(17) == '4' &&
               password.charAt(1)  == '3' &&
               password.charAt(7)  == 'b' &&
               password.charAt(10) == '_' &&
               password.charAt(5)  == '4' &&
               password.charAt(9)  == '3' &&
               password.charAt(11) == 't' &&
               password.charAt(15) == 'c' &&
               password.charAt(8)  == 'l' &&
               password.charAt(12) == 'H' &&
               password.charAt(20) == 'c' &&
               password.charAt(14) == '_' &&
               password.charAt(6)  == 'm' &&
               password.charAt(24) == '5' &&
               password.charAt(18) == 'r' &&
               password.charAt(13) == '3' &&
               password.charAt(19) == '4' &&
               password.charAt(21) == 'T' &&
               password.charAt(16) == 'H' &&
               password.charAt(27) == '5' &&
               password.charAt(30) == '2' &&
               password.charAt(25) == '_' &&
               password.charAt(22) == '3' &&
               password.charAt(28) == '0' &&
               password.charAt(26) == '7' &&
               password.charAt(31) == 'e'
"""

def get_position(line):
    return int(line[16:].split(")")[0])

def get_value(line):
    return line[-2]

splitted = [line.strip() for line in source.split("&&")]
splitted.sort(key=get_position)

flag = ''.join(map(get_value, splitted))
print("picoCTF{"+flag+"}")
````