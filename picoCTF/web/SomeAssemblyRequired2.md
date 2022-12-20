# Some Assembly Required 2

## Analysis
- Application which verifies if input flag is correct
- Flag must be included into JS source code (since no http request is executed)
- faced with obfuscated JS code that includes web assembly functions
  - Deobfuscation via http://jsnice.org/
  - Input string is copied character by character via web assembly function `copy_char`
  - Final string is then compared with flag (which is somehow masked)
- WebAssembly is hard to read, using decompilation techniques: https://github.com/WebAssembly/wabt
  - `wasm-decompile` used to decompile wasm into pseudocode

## Solution
- flag is masked somehow
- input string is copied to certain location via `copy_char`, which xors each character with the hardcoded value `8`
- xoring each character in the masked flag reveals a flag:
- Note: to make this work in python we must escape the non-ascii bytes correctly (e.g. `\x00` insead of `\00`).

```python
encoded_flag = b"xakgK\x5cNs((j:l9<mimk?:k;9;8=8?=0?>jnn:j=lu\x00\x00"
flag = ""

for char in encoded_flag:
    flag += chr(char ^ 8)
print(flag.strip())
```