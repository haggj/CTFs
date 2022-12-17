# Who are you?

## Analysis
- Website tells us that we are not allowed to access the content if we are not using the PicoBrowser
- Hint 1 refers to the HTTP RFC -> setting the request headers could influence the behavior of the server

## Solution
We are receiving further hints by the server if we set the correct request headers.
This reveals several stages:

- Setting the `User-Agent` header to `PicoBrowser` leads to stage2. The server tells us: "I don't trust users visiting from another site."
- Setting the `Referer` header to `http://mercury.picoctf.net:1270/` leads to stage3. The server tells us: "Sorry, this site only worked in 2018."
- Setting the `Date` header to `Wed, 21 Oct 2018 07:28:00 GMT` leads to stage4. The server tells us: "I don't trust users who can be tracked."
- Setting the `DNT` header to `1` leads to stage5. The server tells us: "This website is only for people from Sweden."
- Setting the `X-Forwarded-For` header to `103.57.72.0` leads to stage5. The server tells us: "You're in Sweden but you don't speak Swedish?"
- Setting the `Accept-Language` header to `sv-sv` reveals the flag