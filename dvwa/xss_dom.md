# XSS DOM

User input is included in the DOM of the page. This allows an attacker to inject arbitrary JavaScript code.

## Low
No input sanitization at all. Include any JS code directly into the `default` parameter:
```bash
http://10.10.250.7/vulnerabilities/xss_d/?default=<script>alert(1)</script>
```


## Medium
If the input contains the substring ```<script```, the server redirects the request to `?default=English`.
We can still inject JS code by using the following payload.
It is crucial to first close the ```<select>``` tag, otherwise the injected data will be modified/escaped.
```bash
http://10.10.250.7/vulnerabilities/xss_d/?default=</select><body onload=alert(1)>
```

## High
The allowed default parameters are now white-listed.
However, there is another problem with the code.
Although the server checks the value of the parameter ``default``, all characters after the value of ``default`` are included into the DOM.
This logic can be seen in the frontend JS code. 
The whole string after "default=" is included into the DOM.
E.g. the following URL will include the string ```English&a<script>alert(1)</script>``` into the DOM:
```bash
http://10.10.250.7/vulnerabilities/xss_d/?default=English&a=<script>alert(1)</script>
```


## Impossible
The injection is now prevented by the frontend.
While the url is still cut off after ``default=``, the received string is not URL decoded.
Hence, no HTML characters can be injected.
