Design
=====
There are many evaluations per reading system.
Only one shows up in UI. The others are maintained in the DB for history's sake.

When the testsuite has been updated, run import:
		./run.sh import ~/epub-testsuite/content/30

This creates a new testsuite version, along with new evaluations. These new evaluations are partially populated with data from the previous evaluations, depending on how much of the testsuite has changed. Assuming these evaluations now contain some unanswered tests, they are flagged accordingly (see below in "Scoring").

Scoring
======
Test results are "Supported"/"Not supported"/"No answer given"

Score: percent of passed tests, regardless of optional or required.

If there are results for which no answer has been given, for whatever reason (could be that the test suite was upgraded), flag eval as "incomplete" and indicate on all pages that this is the case.


Permissions
======
Each user can add a reading system and evaluate it.
Reading systems have visibility states: public, owner-only, and members-only
Admin users can access anything.
Admins are the only ones who can set public visibility.


Autosaving
=====
The edit evaluation form autosaves every 30 seconds *if* a value has changed.


Top-level categories
=====
Category types are as follows:

1. Top level ("External")
2. EPUBs ("Epub")
3. Nav document (nested list items) ("Internal")

A category restriction says to what depth to show categories. For some tests, it would be too verbose to show all their categories, so we can restrict them by saying show the tests under only their "External" category or "Epub"-level category.

Testing
======
Do the following to run the supplied unit tests:

`$export PYTHONPATH=${PYTHONPATH}:$PWD/../testsuite-site/:$PWD/../`

edit settings.py and comment-out `django_evolution` from the `INSTALLED_APPS` list

`$cd testsuite-site/`
`$python manage.py test`

