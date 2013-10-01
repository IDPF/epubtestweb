Design
=====
Many evaluations per reading system.
Only one shows up in UI. The others are maintained in the DB for history's sake.

When updating test suite: create new test suite record, create new tests, create new categories.

Make a new evaluation and copy the previous eval's results for tests that are unchanged.

How does the public homepage change? Options:

1. The RS evaluation is now partial, and some categories have a score of 0
2. The RS evaluation is now partial and new or changed items are scored as if they were N/A (score may actually improve in this case)
3. The partial RS evaluation lives internally and the old evaluation is used as the public one. The trouble with this is that it makes it difficult to compare reading systems, as they may be based on different test suite versions.

In the future: allow managing more than one evaluation from the UI.



Permissions
======
Each user can add a reading system and evaluate it.
Users can view all entries but may only edit their own.

Do we need 'admin' users, who can edit everything?

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

