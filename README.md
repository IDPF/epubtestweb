epubtestweb
========

For end-users
==============

Instructions for evaluating reading systems
------------------------------------

See the instructions [here](http://epubtest.org/testsuite/)

Notes about using the website
-----------------------------

1. The evaluation form automatically saves every 30 seconds.
2. The "percent complete" at the top will refresh when the page loads.
3. You don't have to complete the whole evaluation at once.
4. When an evaluation is marked "Public", it appears on the public homepage for the testing website.
5. The testsuite changes from time to time, and the forms on the website are correspondingly updated. If you login and see on the "Manage" page that an evaluation requires review, it means that some tests have been added or changed and that you should re-evaluate your reading system for those tests. Be sure to re-download [testsuite publications](http://epubtest.org/testsuite/) before re-evaluating the reading system, as the tests themselves may have been updated.


For admins
==========

Installing the website
----------------
Requirements: Python 2.7, Django 1.5 or 1.6, lxml, pyyaml

These are good instructions for getting it running on AWS:
http://pragmaticstartup.wordpress.com/2011/04/02/non-techie-guide-to-setting-up-django-apache-mysql-on-amazon-ec2/

After setup, remember to run collectstatic to move Django's admin interface files to the right place.


Initializing the DB for the first time
---------------------------------
If you already have a file `testsuite.db`, this will ERASE any existing data! Backup accordingly.

Run these commands from `import_testsuite_data/`:

`./newdb.sh`
`./runmain.sh import PATH/TO/epub-testsuite/content/30`

If you have a previous database with users that you want to copy over, be sure to configure it in settings.py under the entry `previous`. Then run this command:

`./runmain.sh copy-users`

If you want to add a sample reading system and random evaluation results for it, run this command:

`./runmain.sh add-rs ReadingSystemName`


Adding users
------------
Once you have [added an administrative user](https://docs.djangoproject.com/en/dev/ref/django-admin/#createsuperuser), use the built-in django admin site to add additional users:
`http://your-url.com/admin`


Updating the test suite
---------------
When there is a new version of the testsuite available, just run the import command again:
`./runmain.sh import PATH/TO/epub-testsuite/content/30`

All current evaluations will get ported over.

Overview of user permissions
-------------
Django's default users system has the following types of users (roughly speaking):

* superusers: the highest level of permissions. Superusers may add new users and have total control over reading systems and evaluations.
* staff users: these are regular users with access to the /admin backend site. Once in that site, these users may change their own password but  nothing more.
* regular users: these users can add reading systems and create internal evaluations.


