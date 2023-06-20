# SQL Injection

The input of the user is used to directly construct a SQL statement.


## Low
No check at all, simply use the following snippet to list all users:
```bash
# list all users
' or 1=1 -- 
# show passwords of users
' or 1=1 UNION SELECT first_name, password FROM users -- 
```

## Medium
The SQL injection is now triggered via POST request.
Additionally, the server uses the php function `mysql_real_escape_string()` to escape the input.
This function escapes the following characters: `\x00, \n, \r, \, ', " and \x1a`.
This can be bypassed by using the following payload, because the SQL query does not contain quotes:
```bash
2 or 1=1 -- 
2 or 1=1 UNION SELECT first_name, password FROM users -- 
```


## High
The server offers a second web page, where the logged-in user can specify a user id.
This user id is stored in the session of the logged-in user.
If the user visits the page `http://10.10.61.182/vulnerabilities/sqli/`, the server will load the user id from the session and use it in the SQL query.
This allows us to inject SQL code into the user id, which will be executed by the server:
```bash
' or 1=1 -- 
```


## Impossible
The server uses prepared statements to construct the SQL query.
This prevents the user input from being interpreted as SQL code.