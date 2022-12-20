# Web Gauntlet 2

## Analysis

- Login mask provided along with filter information
- Seems to be a nice SQL injection since the server response with the vulnerable SQL query
- To perform our injection, we can not use the filtered strings (e.g. `or`, `and` `admin`, ...)
- We must log in as `admin`
- We can escape the string and write SQLite commands using the `'` character, e.g. `aaa' or username='abcd`
- Finally, we can provide two payloads: `WHERE username='<payload1>' AMD username='<payload2>'`

## Solution

First part: Specify user `admin` while the string `admin` is filtered
- SQLite provides the string concat operator `||`
- instead of inputting `admin` as username we can insert `adm'||'in`
- `payload1` = `adm'||'in`

Second part: Invalidating the logic of `AND username='<payload1>'` while we can not comment out this part (due to the provided filters)
- we could append the operator `IS NOT`: `AND username='' IS NOT '''`
- `payload2` = `' IS NOT '`

Finally, we receive the flag by checking `filter.php`