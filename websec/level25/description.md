# Level25

## Analysis
- we can provide a filename with the query parameter `page`
- the server then includes the file `<page>.txt` to the output
- the flag seems to be placed in `flag.txt`, but the server does not allow any query parameter to contain the string `flag`

## Solution
- if we  manage to skip the check, we could simply include the file `flag.txt`
- the php docs state, that the `parse_url` function might return `false` for misformed urls
  - this would us allow to skip the check and to successfully read the flag
  - the issue [here](https://stackoverflow.com/questions/47807529/how-to-avoid-php-parse-url-return-false-when-parse-sa-12b-12-3-3-41233-whi) shows that `pares_url` returns `false` if a port is appended to the last query parameter
- thus, the following url delivers the flag: `http://websec.fr/level25/index.php?page=flag&:8000`