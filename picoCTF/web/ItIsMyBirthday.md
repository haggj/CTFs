# It is my Birthday

## Analysis
- Due to the description we need to provide two pdf files having the same MD5 hashes.
- We can not upload any other files than pdf
- However, the check seems not to include the magic numbers - only the extensions seems to be checked

## Solution
- MD5 collisions can be computed quite fast: https://www.mathstat.dal.ca/~selinger/md5collision/
- Downloading the provided binaries (which have the same MD5 hashes) and simply changing their extension suffices to obtain the flag