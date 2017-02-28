Install ldap-utils, along with the ldap compatible versions of nss, ldap and nslcd.

```
apt-get -y install libnss-ldap libpam-ldap ldap-utils nslcd
```
You will be prompted to configure options for your ldap install.  Remember that for a secure installation using ldaps, you will need to use ldaps://10.128.0.12/ instead of ldapi or ldap.  If you are using starttls instead of ldaps you may use ldapi or ldap.  I prefer not to use a local database.  Creating a proxy user is a fine idea, just remember that your password will be stored in the server config, so don't give the user any permissions.  You'll want to at least allow a cert exchange, if not require it.

You can use (https://github.com/nic-instruction/NTI-310/blob/master/debconf.md) to automate configuration of these options later. 


update: 
```
/etc/nsswitch.conf

passwd:         compat ldap
group:          compat ldap
shadow:         compat ldap
```


update:
```
/etc/ldap/ldap.conf


BASE    dc=nti310,dc=local
URI     ldaps://10.128.0.12/

# add TLS_REQCERT allow at the bottom

TLS_REQCERT allow
```

where dc=nti310,dc=local your base search path and ldaps://10.128.0.12/ points to your ldap server.  Note that google provides internal dns for your project, so you may also point to an instance name instead of an IP, for example: ldaps://ldap-a/ 

restart nslcd
`/etc/init.d/nslcd restart`
