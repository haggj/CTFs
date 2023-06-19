# CSRF

Assume an attacker who sends a malicious link to a victim.
If the victim clicks on the link it opens a website.
The attacker assumes, that the victim is logged in on the website and therefore, the browser of the victim stores some authentication information in a cookie.
If the victim clicks on the link, it will send an authenticated request to the server.

Alternatively, the attacker can also create a malicious webpage, which automatically sends a request to the server, if the victim opens the page.
This also allows the attacker to specify the request method (GET or POST).
There are different ways to mitigate CSRF attacks:
- **SOP**:Modern browsers implement the Same-Origin-Policy (SOP), which prevents the browser from sending requests to a different origin. This is realized by performing a preflight request (HTTP OPTIONS requests). If the server answers with the correct CORS headers, the browser will send the actual request. If the server does not answer with the correct CORS headers, the browser will not send the actual request. A server should only answer with the correct CORS headers, if the preflight request is sent by a whitelisted origin.
- **CSRF-Token**: The server sends a token to the client, which must be included in the request. The server checks if the token is valid. This prevents CSRF attacks, because the attacker does not know the token (but the attacker might extract the token by performing a GET requests, which again can be mitigated with SOP).
- **SameSite-Cookie**: The server sets the SameSite attribute of the authentication cookie to ```strict```. This prevents the browser from sending the cookie to the server, if the request is not sent from the same origin. This prevents CSRF attacks, because the attacker does not know the cookie.

## Low
Change the password of a logged-in user to ```test```:

```
http://10.10.127.147/vulnerabilities/csrf/?password_new=test&password_conf=test&Change=Change#
```


## Medium
The server checks, if the ``HTTPP-REFERER`` header is equal to the current server hostname.
This means, that the tool used to send the http request, must set the ```HTTPP-REFERER``` header accordingly.
However, if a victim clicks to the link, the browser will open and send the request with the correct ``HTTPP-REFERER`` header.

By intercepting the requests via burp and modifying the ``HTTPP-REFERER`` header, we can see that the server does not accept requests with a different ``HTTPP-REFERER`` header

## High
The server now expects a token in the request.
The expected token is sent to the client as a hidden input form field.
The client must include this token in a request to the server.
This means, that the attacker also needs to know the token when the malicious link is clicked.

An attacker could still extract the token by performing a GET request to the server if the server whitelists the origin of the attacker-controlled website:
- The attacker creates a malicious website, which sends a GET request to the server.
- The server answers with the token.
- The attacker extracts the token.
- The attacker sends a malicious request to the server with the extracted token.

## ImpossibleSam
The server now expects the user to enter its current password.
This means that the attacker also needs to know the current password of the user in order to change the password.

If the user has a weak password, the attacker could try to brute-force the password using a wordlist.
