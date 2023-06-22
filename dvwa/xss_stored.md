# XSS Stored

User input is stored in the database.
This allows an attacker to inject arbitrary JavaScript code.
If the user input is included in the DOM of the page without sanitization, this yields a XSS vulnerability.

## Low
No input sanitization at all. Include any JS code directly into the message of the guestbook:
```bash
<script>alert(1)</script>
```


## Medium
Server sanitizes the input of the guestbook message. 
It also replaces the substring ```<script>``` with an empty string in the name field.
But since this check is not recursive, we can pass the following name as POST parameter:
```bash
txtName=<<script>script>alert(1111)</script>
```

## High
Server sanitizes the input of the guestbook message. 
It also performs recursive substitutions of the substring ```<script>``` in the name field.
But we can still use other XSS techniques which do not rely on the ```<script>``` tag.
E.g. we can use the ```onload``` event to execute arbitrary JS code.
The following payload can be used as POST parameter:
```bash
txtName=ab<body onload=alert(1)></body>
```


## Impossible
Server sanitizes the input of the guestbook message and name.
It uses the PHP function ```htmlspecialchars``` to escape all HTML characters in the input.