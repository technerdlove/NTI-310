# How to automate your interactive installs using debconf

Use the visual tools to set up your client and ensure it is working properly, then use debconf utils to automate your selections.  We'll use the example of the ldap client configuration in this doc.

## Install your ldap client packages and configure as normal
Install your ldap client packages: `apt-get install libnss-ldap libpam-ldap ldap-utils nslcd debconf-utils` you will be taken into an ncurses gui and prompted for configuration details.  Complete the configuration for both the ldap-auth-config package and the nslcd client.

## Install debconf-utils
After autoconfig runs, it places the configuration files you altered at install under 'debconf' managagement.  Debconf is a system for managing configurations that comes from Debian (hence the name).  You can poke around `/var/cache/debconf/` for raw datafiles or use `man debconf` for more info.

   * Install the utils package `debconf-utils`
   * Use `debconf-get-selections` to find every value you manully configured durring the interactive install.  In this example, we'll use ldap, but you can do this for any interactive package.
   
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
   * We will be using `debconf-set-selections` to automate future installs.
   * To test: `debconf-get-selections | grep ^ldap >> ldapselections`.  Copy the new file ldapselections to a safe location, then then spin up a brand new, client instance.  
   
   
## Testing Your Automation on a New Client
1. Install debconf-utils
2. Set the environmental varialbe telling Debian not to run autoconfig
3. perform the instlall and then unset the variable
   
 ```
export DEBIAN_FRONTEND=noninteractive
apt-get --yes install libnss-ldap libpam-ldap ldap-utils nslcd debconf-utils
unset DEBIAN_FRONTEND
 ```
 
 You now have a completely clean install.  Use debconf to configure your files.
 
 `while read line; do echo "$line" | debconf-set-selections; done < ldap_debconf`
 
 Then check to make sure your changes made it into debconf: `debconf-get-selections | grep ^ldap`
 
 
 Remember that in the case of ldap, you will still need to manually configure files not managed by debconf such as `/etc/nsswitch.conf` and `/etc/ldap/ldap.conf`.  To complete your ldap install configuration, you'll need to set values for ldap-auth-config and nslcd
 
 ```
 root@client-6:~# debconf-get-selections | grep ^nslcd
nslcd   nslcd/ldap-bindpw       password
nslcd   nslcd/xdm-needs-restart error
nslcd   nslcd/disable-screensaver       error
nslcd   nslcd/ldap-base string  dc=nti310,dc=local
nslcd   nslcd/restart-failed    error
nslcd   nslcd/ldap-starttls     boolean false
nslcd   nslcd/ldap-sasl-mech    select
nslcd   nslcd/ldap-uris string  ldaps://10.128.0.12/
nslcd   nslcd/ldap-auth-type    select  none
nslcd   nslcd/ldap-sasl-authzid string
nslcd   libraries/restart-without-asking        boolean false
nslcd   nslcd/ldap-sasl-krb5-ccname     string  /var/run/nslcd/nslcd.tkt
nslcd   nslcd/ldap-sasl-secprops        string
nslcd   nslcd/ldap-reqcert      select  try
nslcd   nslcd/ldap-binddn       string
nslcd   nslcd/ldap-cacertfile   string  /etc/ssl/certs/ca-certificates.crt
nslcd   nslcd/ldap-sasl-authcid string
nslcd   nslcd/restart-services  string
nslcd   nslcd/ldap-sasl-realm   string
 ```
 
 
   
