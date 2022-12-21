# Level28

## Analysis
- we can upload a file to the server
- the uploaded file will be stored in a temporary directory and its MD5-hash is compared to the file `flag.php`, which stores the flag
- if the hashes are identical, the provided file will be included and the flag will be delivered
- if the hashes are not identical, the server waits for 1s and then deletes the uploaded file from the temporary directory


## Solution
- the user-provided file stays on the server for 1s
- in this time period, it is accessible and can deliver the flag if it has the following content:
- the url to access the file depends on your current public IP and stays constant for several requests

```html
 <?php
include("../flag.php");
echo $flag;
?>
```

- we now must be quick enough to access the file before the original request finishes and deletes the file again
- this is realized with the attached python script (`exploit.py`), which extracts the flag:

```