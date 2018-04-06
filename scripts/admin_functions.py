import os
from datetime import datetime

from testsuite_app.models import *

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
    users = UserProfile.objects.all().order_by('is_superuser')
    for u in users:
        superuser = "Regular user"
        if u.is_superuser:
            superuser = "Super user"
        name = "{} {}".format(u.first_name, u.last_name)
        print ("{0:<40s}{1:<40s}{2:<40s}{3:<40s}".format(u.username, u.email, name, superuser))


def listrs():
    rses = ReadingSystem.objects.all().order_by("name")
    for rs in rses:
        print("{0} v. {1}, {2} v. {3} (ID={4})".format(rs.name, rs.version, rs.operating_system, rs.operating_system_version, rs.pk))

def getemails():
    users = UserProfile.objects.all()
    # SELECT DISTINCT on fields not supported by SQLite backend so we have to do it manually
    # luckily this is an isolated case with a small dataset, and one where we can afford to be a little slow
    distinct_emails = []
    for u in users:
        if u.email.lower() not in distinct_emails:
            distinct_emails.append(u.email.lower())
    emails = ", ".join(distinct_emails)
    print(emails)

def add_user(username, password, first_name, last_name, email, is_superuser):
    user = UserProfile.objects.create_user(username, email, password)
    user.first_name = first_name
    user.last_name = last_name
    user.is_superuser = is_superuser == 'True'
    user.save()
    email_text = """
Dear {} {},

Welcome to the Reading App testing website, epubtest.org! Here’s your account information:

username: {}
pwd: {}

Login here: http://epubtest.org/login/

You’ll find instructions here for getting the testsuite documents and filling out an accessibility evaluation:
http://epubtest.org/docs/instructions-for-accessibility-evaluators/

Note that you may have not been assigned an evaluation to fill out yet, as our moderators are still in the process of confirming the system(s) you will be testing. In the meantime, please feel free to use your login to familiarize yourself with the site and read the instructions.

The public front page of the site will be populated with data as evaluations are completed and made public. Your evaluation will not be public until you tell us it's ready, so feel free to experiment with the site, and let me know if you have any questions.

Best regards,

Marisa DeMeglio
DAISY Consortium
""".format(first_name, last_name, username, password)
    print("EMAIL TO USER")
    print("To:\n{}".format(email))
    print("Subj:\n{}".format("Reading App testing website information (epubtest.org)"))
    print(email_text)
    print("END EMAIL TO USER")

def set_superuser(username, is_superuser):
    user = UserProfile.objects.get(username=username)
    if user != None:
        user.is_superuser = is_superuser
        user.save()
        if is_superuser:
            print("User {} is now a superuser.".format(username))
        else:
            print("User {} is not a superuser anymore.".format(username))
    else:
        print("User {} not found.".format(username))
