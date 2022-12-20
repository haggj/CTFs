# Search Source

## Analysis
- Rather complex website is presented.
- The title indicates that the flag is somewhere within the source code
- Many files are included

## Solution
- Mirror the whole site via `wget -m http://...` to local machine
- Found flag using `grep -rni "picoCTF"` within `style.css`