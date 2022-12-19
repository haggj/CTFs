# logon

## Analysis

- We are presented with a simple login form
- One can log in with any user but not with username `Joe`
- User is logged in after refresh -> checking cookies
  - there are three cookies stored once a user is logged-in: ```admin```, ```user```, `password`

## Solution

- modifying the cookie (of an arbitrary logged-in user) `admin` to `True` and refreshing the page delivers the flag