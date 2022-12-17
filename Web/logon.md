# logon

## Analysis

- We are presented with a simple login form
- One can log in with any user but not with username `Joe`
- User is logged in after refresh -> checking cookies
  - there are three cookies stored once a user is logged-in: ```admin```, ```user```, `passwored`

## Solution

- modifying the cookie `admin` to `True` and refreshing the page delivers the flag