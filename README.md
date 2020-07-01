epubtestweb
========

This repository contains the code for the old epubtest.org site. This site has changed substantially and this codebase is no longer relevant. The archives for the old site can be found at https://daisy.github.io/old-epub3-support-grid.


For end-users
==============

Instructions for evaluating reading systems
------------------------------------

See the instructions [here](http://epubtest.org/testsuite/)

Notes about using the website
-----------------------------

1. You don't have to complete the whole evaluation at once.
2. When an evaluation is marked "Published", it appears on the public homepage for the testing website.
3. The testsuite changes from time to time, and the forms on the website are correspondingly updated. You can go back and edit your evaluation, and the evaluation form will tell you which items require attention.
4. You can send another site member a link to your evaluation and they can view it; otherwise, links to your evaluations are not exposed to other users except for administrators.


For admins
==========

Installing the website
----------------
Requirements: Python 3, Django 1.9

These are good instructions for getting it running on AWS:
http://pragmaticstartup.wordpress.com/2011/04/02/non-techie-guide-to-setting-up-django-apache-mysql-on-amazon-ec2/

After setup, remember to run collectstatic to move Django's admin interface files to the right place.


Initializing the DB for the first time
---------------------------------
If you already have a file `testsuite.db`, this will ERASE any existing data! Backup accordingly.

Run these commands from `testsuite.site/`:
`./manage migrate`

Run these commands from `scripts/`:

`./runmain.sh import PATH/TO/epub-testsuite/content/30 testsuite.yaml`
`./runmain.sh copy-users`

(Where the old database containing user profile info is in the same directory as the current database, but is named `testsuite-old.db`.)

Now you have a database that works with the website but is empty. If you need to import evaluation and reading system data, use the `import-data` command to load from XML.

Adding users
------------
Once you have [added an administrative user](https://docs.djangoproject.com/en/dev/ref/django-admin/#createsuperuser), use the built-in django admin site to add additional users:
`http://your-url.com/admin`


Updating the test suite
---------------
When there is a new version of the testsuite available, just run the import command again:
`./runmain.sh import PATH/TO/epub-testsuite/content/30`

All current evaluations will get ported over. Results will be cleared for any new or changed tests, and when users log in, they will see an alert informing them to update their evaluation(s).

Overview of user permissions
-------------
Django's default users system has the following types of users (roughly speaking):

* superusers: the highest level of permissions. Superusers may add new users and have total control over reading systems and evaluations.
* staff users: these are regular users with access to the /admin backend site. Once in that site, these users may change their own password but  nothing more.

Testsuite categorization
-------------
The rules
* follow the existing formatting of the epubs
* organize into categories/features by using `testsuite.yaml`
* one epub may appear in more than one category, but not across testsuites
* a feature's ID must be unique within its testsuite



