# Secure Signing

The server is a simple web application which allows to sign a message with a secret flag.
The signed message can then be verified by the server.

Ths user provided message is signed by the following pseudo code. 
```
SHA256(message xor flag)
``````
The user can provide arbitrary messages. 
If the user only sends one byte, the flag will be cut off after the first byte.
This allows to brute force the flag byte by byte:
1. Send a message with one zero byte.
2. The server computes `SHA256(0x00 xor flag[0])` which is equal to `SHA256(flag[0])`.
3. The attacker can simply brute force the first byte of the flag by locally hashing all possible bytes and comparing the result with the server response.
4. If the first byte is found, the attacker can repeat the process for the second byte and so on.