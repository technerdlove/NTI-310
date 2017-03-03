


edit `vim /var/lib/pgsql/data/pg_hba.conf` and add the line:

```
host    all             all             10.128.0/9              md5
```
If your project does not have a 10.128.0/9 subnet please use your subnet.


Next, edit `vim /var/lib/pgsql/data/postgresql.conf ` and change the listenaddress from localhost to *.  Later, durring our security and automation pass, we'll change this to the internal IP of the server.

```
#listen_addresses = 'localhost'          # what IP address(es) to listen on;
listen_addresses = '*'                   # what IP address(es) to listen on;

```

restart postgres `systemctl restart  postgresql.service`

You should now be able to run your migration script without error.  You can test the port by telneting from your django server to 
your postgres server on the postgres port: `telnet 10.128.0.10 5432`


Go back to your django server, remember that your should be running as the user who owns `/opt/django/project1` directory, in my case, that user is nicolebade.  Also remember that you need to source your virtualenv: `source /opt/django/django-env/bin/activate` to use the correct python instance.


```
(django-env) [nicolebade@django-staging project1]$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying sessions.0001_initial... OK
```
