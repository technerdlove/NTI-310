# Installing secure ldap client
This document will take you through the installation of an ldap client using ldaps.  Please note that while ldaps uses SSL and is fairly secure once the connection has been established, it has been depricated in favor of the better-documented START_TLS option in ldap 3, which runs over a single port and toggles encryption by issuing the command 'START_TSL'.  For more info see the relevent mailing list clarifications here (http://www.openldap.org/lists/openldap-software/200305/msg00084.html) and here (http://www.openldap.org/lists/openldap-software/200201/msg00042.html).


Install ldap-utils, along with the ldap compatible versions of nss, ldap and nslcd.

```
apt-get -y install libnss-ldap libpam-ldap ldap-utils nslcd
```
You will be prompted to configure options for your ldap install.  Remember that for a secure installation using ldaps, you will need to use ldaps://10.128.0.12/ instead of ldapi or ldap.  If you are using starttls instead of ldaps you may use ldapi or ldap.  I prefer not to use a local database.  Creating a proxy user is a fine idea, just remember that your password will be stored in the server config, so don't give the user any permissions.  You'll want to at least allow a cert exchange, if not require it.

You can use (https://github.com/nic-instruction/NTI-310/blob/master/debconf.md) to automate configuration of these options later. 


Next, add ldap entries to nsswitch.conf
update: 
```
/etc/nsswitch.conf

passwd:         compat ldap
group:          compat ldap
shadow:         compat ldap

netgroup:       ldap
```

Finally, update /etc/ldap/ldap.conf with your config:

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


Your client should be securly configured now.  You can test your configuration using ldapsearch:

```
ldapsearch  -b "dc=nti310,dc=local"  -x -d 1 2>> output.txt
```

This will search ldap using your current system configuration, which by now should be on port 636 (ldaps) and will set the connection to dbug level 1.  `2>> output.txt` redirects your dbug output to a file called output.txt.  You'll see your users come through if the connection suceeds:

```

# Emily Dickinson, People, nti310.local
dn: cn=Emily Dickinson,ou=People,dc=nti310,dc=local
givenName: Emily
sn: Dickinson
cn: Emily Dickinson
uid: edickinson
userPassword:: *
uidNumber: 1000
gidNumber: 500
homeDirectory: /home/edickinson
loginShell: /bin/sh
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: top
# Walt Whitman, People, nti310.local
dn: cn=Walt Whitman,ou=People,dc=nti310,dc=local
givenName: Walt
sn: Whitman
cn: Walt Whitman
uid: wwhitman
userPassword:: *
uidNumber: 1001
gidNumber: 500
homeDirectory: /home/wwhitman
loginShell: /bin/sh
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: top
```

Then check the output.txt file to confirm your exchange used ssl over port 636:

```
ldap_create
ldap_sasl_bind
ldap_send_initial_request
ldap_new_connection 1 1 0
ldap_int_open_connection
ldap_connect_to_host: TCP 10.128.0.12:636
ldap_new_socket: 4
ldap_prepare_socket: 4
ldap_connect_to_host: Trying 10.128.0.12:636
ldap_pvt_connect: fd: 4 tm: -1 async: 0
attempting to connect: 
connect success
TLS: peer cert untrusted or revoked (0x42)
ldap_open_defconn: successful
ldap_send_server_request
ber_scanf fmt ({it) ber:
ber_scanf fmt ({i) ber:
ber_flush2: 14 bytes to sd 4
ldap_result ld 0x55c87d9bee20 msgid 1
wait4msg ld 0x55c87d9bee20 msgid 1 (infinite timeout)
wait4msg continue ld 0x55c87d9bee20 msgid 1 all 1
** ld 0x55c87d9bee20 Connections:
* host: 10.128.0.12  port: 636  (default)
  refcnt: 2  status: Connected
  last used: Tue Feb 28 01:33:31 2017
** ld 0x55c87d9bee20 Outstanding Requests:
 * msgid 1,  origid 1, status InProgress
   outstanding referrals 0, parent count 0
  ld 0x55c87d9bee20 request count 1 (abandoned 0)
** ld 0x55c87d9bee20 Response Queue:
   Empty
  ld 0x55c87d9bee20 response count 0
ldap_chkResponseList ld 0x55c87d9bee20 msgid 1 all 1
ldap_chkResponseList returns ld 0x55c87d9bee20 NULL
ldap_int_select
read1msg: ld 0x55c87d9bee20 msgid 1 all 1
ber_get_next
ber_get_next: tag 0x30 len 12 contents:
read1msg: ld 0x55c87d9bee20 msgid 1 message type bind
ber_scanf fmt ({eAA) ber:
read1msg: ld 0x55c87d9bee20 0 new referrals
read1msg:  mark request completed, ld 0x55c87d9bee20 msgid 1
request done: ld 0x55c87d9bee20 msgid 1
res_errno: 0, res_error: <>, res_matched: <>
ldap_free_request (origid 1, msgid 1)
ldap_parse_result
ber_scanf fmt ({iAA) ber:
ber_scanf fmt (}) ber:
ldap_msgfree
ldap_search_ext
```

At the very top of the output, you'll notice the connection goes through, despite the warning about a self-signed cert.

