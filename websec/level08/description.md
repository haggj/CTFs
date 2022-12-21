# Level08


## Analysis

- we can upload files to the server
- the server will include the file content if it is a valid gif file
- there are three checks in place to verifiy the input file:
  1. The file size can not exceed 5000 bytes
  2. The file must be a image (i.e. `getimagesize` must not return `false`)
  3. The file must be a valid gif (checked via `exif_imagetype`)

## Solution:
- we can insert a GIF file which contains valid php code
  - such a file will pass all checks
  - the server will execute the attached code because the uploaded file is included via `include_once`
- we can append the content of `run.php` (which lists all files in the current directory and print the file `flag.txt` one executed by the server) to the small gif file `small.gif`
- the resulting file `payload.gif` can be uploaded directly to the server to run the malicious code and obtain the flag