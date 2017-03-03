# Connecting postgres and Django

So, you have a posgres server installed and configured.  You've configured your project1 database, your project1 user and your django instance can run the test server.  You've edited your django settings.py using https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-centos-7 to point to your remote pg server but when you start to migrate, it is telling you the posgres server is unavailable.  This tutorial will shouw you how to make your pg server available on the network, taking traffic from your internal IP range but not external, and how to set up phpmyadmin so you can view your database visually.


##  Configuring postgres to listen for remote connections

Your next step is to connect your django server to your posgres server and migrate 


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

## Running your django migration

You should now be able to run your migration script without error.  You can test the port by telneting from your django server to 
your postgres server on the postgres port: `telnet 10.128.0.10 5432`


Go back to your django server, remember that your should be running as the user who owns `/opt/django/project1` directory, in my case, that user is nicolebade.  Also remember that you need to source your virtualenv: `source /opt/django/django-env/bin/activate` to use the correct python instance.

change directory (`cd`) into `/opt/django/project1` and start your migration to postgres.  Your output should look like somthing like this

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

## Creating your django admin user

```
(django-env) [nicolebade@django-staging project1]$ python manage.py createsuperuser
Username (leave blank to use 'nicolebade'): admin
Email address: root@localhost
Password: 
Password (again): 
Superuser created successfully.
```
Note: you can automate this step using
```
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | ./manage.py shell
```
Please use somthing more createive than pass for your password outside of the testing environment.


## Installing phpmyadmin

**** this part isn't ready yet!*****

phpmyadmin will allow you to access your database info through a webpage.  It is also a good way for beginners to learn to construct queries and has some nifty data export features.  It goes without saying, that in a production environment this application should be entirely internal and should not be accessible outside the firewall.  It's your data :).

```
yum install httpd php php-pgsql
yum -y install phpmyadmin

```
Edit `/etc/httpd/conf.d/phpMyAdmin.conf `, by default traffic is restricted to localhost which is more secure.  If you want to, you can install firefox on your local instance and xforward that session to browse your db that way.  On a normal network, you would restrict this to the internal network.  For our purposes, you will want to restrict it to your IP address and the IP of the school or open up permissions for later restriction.  The relevent lines are here:

```
#   <IfModule mod_authz_core.c>
    # Apache 2.4
#     <RequireAny>
#       Require ip 127.0.0.1
#       Require ip ::1
#     </RequireAny>
#   </IfModule>
   <IfModule !mod_authz_core.c>
     # Apache 2.2
     Order Deny,Allow
     Deny from All
     Allow from 127.0.0.1
     Allow from ::1
   </IfModule>
</Directory>
<Directory /usr/share/phpMyAdmin/setup/>
#   <IfModule mod_authz_core.c>
     # Apache 2.4
#     <RequireAny>
#       Require ip 127.0.0.1
#       Require ip ::1
#     </RequireAny>
#   </IfModule>
   <IfModule !mod_authz_core.c>
     # Apache 2.2
     Order Deny,Allow
     Deny from All
     Allow from 127.0.0.1
     Allow from ::1
   </IfModule>
</Directory>
```

Tell SELINUX to allow http to connect to postgres
`setsebool -P httpd_can_network_connect_db 1`

In this example, I commented them out the restriction lines (opening all of the data on my test site to the whims of the world) which I would not, repeate would not do in any sort of even mildly production environment but am doing as a step before securing the server.  I restarted apache `service httpd restart` and am now able to log into phpmyadmin. http://myserverip/phpmyadmin.



```



