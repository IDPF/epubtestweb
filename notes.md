Design
=====
One evaluation per reading system


Permissions
======
Each user can add a reading system and evaluate it.
Another user can view their evaluation but not edit it.

TODO: introduce 'admin' users, who can edit everything


Etc
===

Annoying inline imports everywhere in Model functions:

    def get_top_level_categories(self):
        from category import Category

Why? Not sure.

