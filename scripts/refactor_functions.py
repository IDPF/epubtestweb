import os
from testsuite_app.models import common
from testsuite_app import helper_functions
from testsuite_app import export_data

from django.contrib.sessions.models import Session
from testsuite_app.models import UserProfile
from testsuite_app.models import Evaluation
from datetime import datetime

# settings.py must contain a definition for the 'previous' database in order for this to work
def copy_users():
    new_users = UserProfile.objects.using('previous').all()
    current_users = UserProfile.objects.using('default').all()
    usernames = [u.username for u in current_users]
    for u in new_users:
        if u.username not in usernames:
            print("New user found {0}".format(u.username))
            u.pk = None
            u.save(using='default')

        else:
            print("skipping duplicate {0}".format(u.username))
    print("Copied users from old database.")
    num_users = UserProfile.objects.using('default').all().count()
    print("Total number of users is now: {0}".format(num_users))

def import_json(filepath):
    pass
