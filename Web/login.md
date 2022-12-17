# login

## Analysis
- We are presented a simple login form
- We must input a correct username to check the password
- Networking tab indicates that the frontend does not request the backend if submit button is clicked
- Checking source code reveals `index.js` which contains username and password verification

## Solution
- Username and password are not presented in cleartext, but they are compared with the base64-encoded input.
- Thus, we can simply base64-decode the provided strings to obtain the valid credentials (password is the flag)