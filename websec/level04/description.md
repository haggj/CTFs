# Level04

- We are faced with a serialization vulnerability
- The server reads a cookie `leet_hax0r` deserializes its base64-decoded content
- The server makes user of the class ```SQL``` which owns a `__destruct` method which is called upon destruction
  - During destruction the server queries the database with the query stored in the ``SQL`` object
  - The resulted query is presented to the server, as long as it has a `username` column
- The code in `index.php` crafts a ```SQL``` object which contains a query which delivers the flag by querying the password of the user
- If the crafted object is base64-encoded and put into the cookie `leet_hax0r`, the server deleivers the flag