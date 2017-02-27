# How to automate your installs using debconf

Use the visual tools to set up your client and ensure it is working properly, then use debconf utils to automate your selections.

   * Install the utils package `debconf-utils
   * Use debconf-get-selections to find every value you manully configured.  In this example, we'll use ldap, but you can do this for any
   install configured interactively by debconf.
``` 
root@client-6:/# debconf-get-selections | grep ^ldap
ldap-auth-config        ldap-auth-config/bindpw password
ldap-auth-config        ldap-auth-config/rootbindpw     password
ldap-auth-config        ldap-auth-config/binddn string  cn=proxyuser,dc=example,dc=net
ldap-auth-config        ldap-auth-config/dblogin        boolean false
ldap-auth-config        ldap-auth-config/move-to-debconf        boolean true
ldap-auth-config        ldap-auth-config/pam_password   select  md5
ldap-auth-config        ldap-auth-config/ldapns/base-dn string  dc=nti310,dc=local
ldap-auth-config        ldap-auth-config/ldapns/ldap-server     string  ldaps://10.128.0.12/
ldap-auth-config        ldap-auth-config/rootbinddn     string  cn=manager,dc=example,dc=net
ldap-auth-config        ldap-auth-config/override       boolean true
ldap-auth-config        ldap-auth-config/ldapns/ldap_version    select  3
ldap-auth-config        ldap-auth-config/dbrootlogin    boolean false
```
   * Use `debconf-set-selections` to configure those selections for automation purposes.
   * To test: `debconf-get-selections | grep ^ldap >> ldapselections` and then spin up a brand new, client instance.  Set the environmental varialbe
   that tells debian not to run autoconfig, perform the instlall and then unset the variable:
   
 ```
export DEBIAN_FRONTEND=noninteractive
apt-get --yes install libnss-ldap libpam-ldap ldap-utils nslcd
unset DEBIAN_FRONTEND
 ```
 
 
   
