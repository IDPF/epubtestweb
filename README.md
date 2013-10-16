epubtestweb
========

For end-users
==============

Instructions for evaluating reading systems
------------------------------------

1. Make a local copy of the [testsuite repository](https://github.com/mgylling/epub-testsuite)
2. Build EPUBs from the testsuite by running `build.bat` or `build.sh`
3. Start your reading system application
4. Login to the website
5. From the "Manage" page, add a new reading system, if yours isn't already listed
6. Enter all relevant details
7. From the "Manage" page, choose "Evaluate"
8. The evaluation form is divided into categories, such as "Content Documents", "Styling", "Scripting", etc. Each category refers to one or more EPUBs.
9. Go back to your reading system and open the first EPUB referenced by the evaluation form.
10. Each EPUB contains a series of tests, marked by identifiers such as "iframe-010", "img-010", "img-020", etc. Follow the instructions in the EPUB for each test to determine if it passes or fails (or is not applicable). 
11. Record the result in the evaluation form, using the dropdown box to the right of each test description.

Notes about using the website
-----------------------------

1. The evaluation form automatically saves every 30 seconds.
2. The "percent complete" at the top will refresh when the page loads.
3. You don't have to complete the whole evaluation at once.
4. When an evaluation is marked "Public", it appears on the public homepage for the testing website.
5. The testsuite changes from time to time, and the forms on the website are correspondingly updated. If you login and see on the "Manage" page that an evaluation requires review, it means that some tests have been added or changed and that you should re-evaluate your reading system for those tests. Be sure to update your local copy of the testsuite EPUBs before re-evaluating the reading system.


For admins
==========

Initializing the DB for the first time
---------------------------------


Adding users
------------


Updating the test suite
---------------

