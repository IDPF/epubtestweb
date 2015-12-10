import os
from testsuite_app import models
from testsuite_app.models import common, UserProfile
from testsuite_app import helper_functions
from testsuite_app import export_data

from django.contrib.sessions.models import Session
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


def listusers():
    users = models.UserProfile.objects.all()
    for u in users:
        print ("{0}\t\t\t\t{1} {2}".format(u.username, u.first_name.encode('utf-8'), u.last_name.encode('utf-8')))


def list_logged_in_users():
    # Query all non-expired sessions
    sessions = Session.objects.filter(expire_date__gte=datetime.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    users = UserProfile.objects.filter(id__in=uid_list)

    for u in users:
        print(u.username)

def listrs():
    rses = models.ReadingSystem.objects.all()
    for rs in rses:
        print("{0}: {1}".format(rs.name, rs.pk))

def getemails():
    users = models.UserProfile.objects.all()
    # SELECT DISTINCT on fields not supported by SQLite backend so we have to do it manually
    # luckily this is an isolated case with a small dataset, and one where we can afford to be a little slow
    distinct_emails = []
    for u in users:
        if u.email.lower() not in distinct_emails:
            distinct_emails.append(u.email.lower())
    emails = ", ".join(distinct_emails)
    print(emails)
