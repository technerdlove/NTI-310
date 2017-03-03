


edit `vim /var/lib/pgsql/data/pg_hba.conf` and add the line:

```
host    all             all             10.128.0/9              md5
```
If your project does not have a 10.128.0/9 subnet please use your subnet.


Next, edit `vim /var/lib/pgsql/data/postgresql.conf ` and change the listenaddress from localhost to *.  Later, durring our security and automation pass, we'll change this to the internal IP of the server.

```
#listen_addresses = 'localhost'          # what IP address(es) to listen on;
listen_addresses = '*'          # what IP address(es) to listen on;

```

restart postgres `systemctl restart  postgresql.service`

You should now be able to run your migration script without error.  You can test the port by telneting from your django server to 
your postgres server on the postgres port: `telnet 10.128.0.10 5432`

