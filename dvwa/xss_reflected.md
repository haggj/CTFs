# XSS Reflected

User input is included in the DOM of the page. 
This allows an attacker to inject arbitrary JavaScript code.
In this scenario, the PHP server parses the GET parameter ``default`` and includes it into the DOM.

## Low
No input sanitization at all. Include any JS code directly into the `default` parameter:
```bash
http://10.10.220.77/vulnerabilities/xss_r/?name=<script>alert(1)</script>
```


## Medium
If the input contains the substring ```<script>```, the server replaces it with an empty string.
But this replacement is not recursive, so the following URL works:
```bash
http://10.10.220.77/vulnerabilities/xss_r/?name=<<script>script>alert(1)</script>
```

## High
The server uses a regex to check, if the input contains the substring ```<script>``` or any recursive versions.
But we can still use other XSS techniques which do not rely on the ```<script>``` tag.
E.g. we can use the ```onload``` event to execute arbitrary JS code:
```bash
http://10.10.220.77/vulnerabilities/xss_r/?name=<body onload=alert(1)>
```


## Impossible
The server escapes all HTML characters in the input by utilizing the PHP function ```htmlspecialchars```.
