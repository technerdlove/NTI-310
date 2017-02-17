# Step by step guide to making phpldapadmin use ssl

Automating these steps should be fairly easy.  A few echo's and searches and replaces should do the trick.  Use the -subj
flag to automate ssl cert creation.

This tutorial is a synthesis of two other tutorials plus some of my commands.  You can find them here:    
   * (https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-openldap-and-phpldapadmin-on-an-ubuntu-14-04-server)
   * (https://www.digitalocean.com/community/tutorials/how-to-create-an-ssl-certificate-on-apache-for-centos-7)
They do a fairly good job of explaining the 'why' of what we're doing.  Also take a look at the apache/ssl section of your book.


### First get rid of anonymous logins:

/etc/phpldapadmin/config.php
$servers->setValue('login','anon_bind',false);
(instead of true)
There is also a commented out section with anon_bind true, copy it and change to annonbind false, then uncomment your false.




```
yum install mod_ssl

 mkdir /etc/ssl/private
 chmod 700 /etc/ssl/private
 sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out
 /etc/ssl/certs/apache-selfsigned.crt
 openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
 cat /etc/ssl/certs/dhparam.pem | tee -a /etc/ssl/certs/apache-selfsigned.crt
 ```
 
 Then open the ssl.conf file:
 
 vi /etc/httpd/conf.d/ssl.conf


Under `"<VirtualHost _default_:443>"` add 

```
Alias /phpldapadmin /usr/share/phpldapadmin/htdocs
Alias /ldapadmin /usr/share/phpldapadmin/htdocs
DocumentRoot "/usr/share/phpldapadmin/htdocs"
ServerName ldap-automate-c:443
```

in `/etc/httpd/conf.d/ssl.conf`

Manual Unit Test: [Then test and make sure your cert is working by restarting apache and hitting the page as https.
You will recive an error about an insecure cert.  It is insecure... it's self signed.  If we purchaced a domain name and got
cert issued, we wouldn't get this warning.]


### Update Cypher Suite

Open `/etc/httpd/conf.d/ssl.conf` again we're going to force it to use a more secure cypher suite.
Comment out:

```
# SSLProtocol all -SSLv2
. . .
# SSLCipherSuite HIGH:MEDIUM:!aNULL:!MD5:!SEED:!IDEA
```

After the virtualhost is closed with `</VirtualHost>`, paste in:

```
# Begin copied text
# from https://cipherli.st/
# and https://raymii.org/s/tutorials/Strong_SSL_Security_On_Apache2.html

SSLCipherSuite EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH
SSLProtocol All -SSLv2 -SSLv3
SSLHonorCipherOrder On
# Disable preloading HSTS for now.  You can use the commented out header line that includes
# the "preload" directive if you understand the implications.
#Header always set Strict-Transport-Security "max-age=63072000; includeSubdomains; preload"
Header always set Strict-Transport-Security "max-age=63072000; includeSubdomains"
Header always set X-Frame-Options DENY
Header always set X-Content-Type-Options nosniff
# Requires Apache >= 2.4
SSLCompression off 
SSLUseStapling on 
SSLStaplingCache "shmcb:logs/stapling-cache(150000)" 
# Requires Apache >= 2.4.11
# SSLSessionTickets Off
```
