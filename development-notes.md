Design
=====
There are many evaluations per reading system.
Only one shows up in UI. The others are maintained in the DB for history's sake.

When the testsuite has been updated, run import:
		./run.sh import ~/epub-testsuite/content/30

This creates a new testsuite version, along with new evaluations. These new evaluations are partially populated with data from the previous evaluations, depending on how much of the testsuite has changed.

Question: How does the public homepage change when the testsuite is updated?

1. The RS evaluation is now partial, and some categories have a score of 0
2. The RS evaluation is now partial and new or changed items are scored as if they were N/A (score may actually improve in this case)
3. The partial RS evaluation lives internally and the old evaluation is used as the public one. The trouble with this is that it makes it difficult to compare reading systems, as they may be based on different test suite versions.

In the future: allow managing more than one evaluation from the UI.

Scoring
======
Right now, scoring is very simple. Each category score is calculated by dividing the tests passed by the total number of applicable tests. If there are zero applicable tests, the category is scored as "0". 

TODO: address the following issues with scoring:

1. A required test that is marked "N/A" should count as a "Fail"
2. If there are zero applicable tests in a category, and they are all optional, we should mark that category as "N/A" rather than give it a value.
3. Should the score be based only on required tests? Then optional tests that pass are bonus points, and ones that fail are not counted against the overall score.

Permissions
======
Each user can add a reading system and evaluate it.
Users can view all entries but may only edit their own.

TODO: Do we need 'admin' users, who can edit everything?

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


Etc
===

Annoying inline imports everywhere in Model functions:

    def get_top_level_categories(self):
        from category import Category

Why? Not sure. Doesn't work when they are just declared at the top of the file.

