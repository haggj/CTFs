# File Inclusion

Server loads a file specified by the ```page``` parameter.
This might allow an attacker to load arbitrary files from the server.

## Low
The server does not check the ```page``` parameter at all.
The following link loads the ```/etc/passwd``` file:
```bash
http://10.10.155.108/vulnerabilities/fi/?page=../../../../../../../etc/passwd
```


## Medium
The server checks, if the input string contains the substring ```../```.
But this check is not recursive, so the following link loads the ```/etc/passwd``` file:
```bash
http://10.10.155.108/vulnerabilities/fi/?page=..././..././..././..././..././..././..././..././etc/passwd
```

Instead of ```../``` we use ```..././```.
The server then replaces the ```../``` with an empty string, so after the replacement we receive ``../``.
A recursive check of the existence of ```../``` would have detected this.

## High
The page parameter must now start with ```file```.
We can obtain arbitrary files by specifying a file URI:
```bash
file:///etc/passwd
```

## ImpossibleSam
The server white-lists the files, which are allowed to be loaded.