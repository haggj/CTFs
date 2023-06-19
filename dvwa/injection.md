# Injection

User input is used to execute command on the server.

## Low
No input sanitization at all. Run arbitrary commands:
```bash
; whoami
; ls /
```


## Medium
Input characters `&&` and ``;`` are filtered.
But it is allowed to use `&` to send the ping command to the background and define another command:

```bash
& whoami
& ls /
```

## High
Many input characters are filtered.
But instead of only ```|```, the blacklist filters ```|<space>```. 
So the following still works:

```bash
|whoami
|ls /
```

## Impossible
The server checks if the input ip is actually an IP address by splitting the string at `.` and checking if the resulting array has 4 elements and if each element is numeric.
This makes it much harder to inject commands because we need to enter something like:
```bash
<numeric>.<numeric>.<numeric>.<numeric>
```
