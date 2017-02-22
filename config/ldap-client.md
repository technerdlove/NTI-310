```
apt-get -y install libnss-ldap libpam-ldap ldap-utils nscd
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
URI     ldap://10.128.0.12:389/
```
