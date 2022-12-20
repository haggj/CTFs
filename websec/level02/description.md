# Level02 

- Challenge faced a more sophistiacted SQL injection
- Same setup than in level01, but multiple keywords are filtered
- Solved by writing a blind SQL injection: guessing the password of user 1 character by character using the ``LIKE`` operator
- this avoids unions of multiple sql statements