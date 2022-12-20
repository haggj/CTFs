# Most Cookies

## Analysis
- We receive a cookie, which was issued by flask (https://overiq.com/flask-101/sessions-in-flask/)
- Those cookies contain the session data, however, they are signed with a secret only knows by the server
- The session cookie stores the value `{'very_auth': 'blank'}`

## Solution
- Using the tool `flask-unsign` described here: https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/flask
- This allows us to check if a weak password was used by performing a bruteforce attack 
- Bruteforce attack succeeds -> cookies are signed with the secret `fortune`
- Crafting a new cookie with the payload `{'very_auth': 'admin'}` delivers the flag