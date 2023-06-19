# File Inclusion

Users can upload files to the server. 
If the server does not sanitize/check the uploaded file, an attacker might be able to inject PHP code into the file.
If the attacker also knows the path of the uploaded file, he can execute the injected PHP code by loading the file.

## Low
The server does not check the uploaded file at all. 
By simply uploading a php file, we can execute shell commands.

## Medium
The server checks, if the uploaded file is a jpeg/png file by checking `$_FILES[ 'uploaded' ][ 'type' ];`.
This can be spoofed by an attacker by simply changing the content-type of the uploaded file to `image/jpeg` or `image/png`.

## High
The server also checks, if the file extension is `jpg` or `png` and checks the size of the uploaded file using the php function `getimagesize()`.
This can be bypassed by an attacker by simply uploading a file with the extension `php.jpg` or `php.png`.
To bypass the function `getimagesize()`, we can simply intercept the request and add the following magic bytes at the beginning of the actual file:
```
GIF89a;
<php>....</php>
```
Note, that this does not allow RCE, because the file will be interpreted as a image file and not as a PHP file.
You might be able to use a LFI vulnerability to load the uploaded file and execute the PHP code.

## Impossible
The uploaded file is re-encoded the provided jpg/png file using the php function `imagecreatefromjpeg()` or `imagecreatefrompng()`.