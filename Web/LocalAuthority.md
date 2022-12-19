# Local Authority

## Analysis
- We are provided with a simple login form.
- Login attempts request `login.php` and response with invalid credentials for any login
- Source code of `login.php` reveals that the client verifies the password and not the server

## Solution
- `login.php` includes `security.js` which contains a function that verifies the provided credentials
- Username and password are stored in cleartext
- A login with the found credentials yields the flag