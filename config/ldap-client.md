```
apt-get -y install libnss-ldap libpam-ldap ldap-utils nslcd
```


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
```

where dc=nti310,dc=local your base search path and ldaps://10.128.0.12/ points to your ldap server.  Note that google provides internal dns for your project, so you may also point to an instance name instead of an IP, for example: ldaps://ldap-a/ 
