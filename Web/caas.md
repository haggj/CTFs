# caas

## Analysis
- We can call a endpoint containing a message, which will be *cowsaid*
- The provided `index.js` shows that the server calls a binary `/usr/games/cowsay` via exec with the provided string
- This allows to run arbitrary commands on the server

## Solution
- Calling the cowsay endpoint with `message && ls` appends the output of the `ls` command to the output
- This shows that the server has a file `falg.txt`
- Calling the cowsay endpoint with `message && cat falg.txt` delivers the flag