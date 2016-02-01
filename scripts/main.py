import argparse
import os

from testsuite_app import helper_functions
from admin_functions import *
from import_testsuite import import_testsuite

from django.contrib.sessions.models import Session

from import_evaluation_data import import_evaluation_data

def import_data(infile):
    print ("Importing from {}".format(infile))
    import_evaluation_data(infile)
    print ("Done")

def refresh_scores():
    # this shouldn't need to be called
    print ("Refreshing scores")
    helper_functions.force_score_refresh()

def refresh_percent_complete():
    print("Refreshing percent complete")
    helper_functions.force_percent_complete_refresh()

def flag_items():
    import random
    # set result.flagged to true on some result objects
    results = Result.objects.all().order_by('?')[:100]
    for result in results:
        result.flagged = True
        result.save()


def clear_flags():
    from testsuite_app.models import Result
    # reset result.flagged to false on all result objects
    results = Result.objects.all()
    for result in results:
        result.flagged = False
        result.save()


def main():
    
    argparser = argparse.ArgumentParser(description="epubtest.org command line")
    subparsers = argparser.add_subparsers(help='commands')
    import_parser = subparsers.add_parser('import', help='Import a testsuite into the database')
    import_parser.add_argument("source", action="store", help="Folder containing EPUBs")
    import_parser.add_argument("config", action="store", default="testsuite.yaml", help="structure config file")
    import_parser.set_defaults(func = lambda args: import_testsuite.add_testsuites(args.source, args.config))
    
    listrs_parser = subparsers.add_parser('listrs', help="List all reading systems and their IDs")
    listrs_parser.set_defaults(func = lambda args: listrs())

    emails_parser = subparsers.add_parser('emails', help="List user emails")
    emails_parser.set_defaults(func = lambda args: getemails())

    listusers_parser = subparsers.add_parser("listusers", help="list all users")
    listusers_parser.set_defaults(func = lambda args: listusers())

    import_data_parser = subparsers.add_parser("import-data", help="Import evaluation data in XML format")
    import_data_parser.add_argument("file", action="store", help="XML file containing data to import")
    import_data_parser.set_defaults(func = lambda args: import_data(args.file))

    scores_parser = subparsers.add_parser("score", help="Refresh all scores")
    scores_parser.set_defaults(func = lambda args: refresh_scores())

    percent_complete_parser = subparsers.add_parser("percent-complete", help="Refresh percent complete")
    percent_complete_parser.set_defaults(func = lambda args: refresh_percent_complete())

    copy_users_parser = subparsers.add_parser("copy-users", help="Refresh all scores")
    copy_users_parser.set_defaults(func = lambda args: copy_users())

    add_user_parser = subparsers.add_parser("add-user", help="Add a new user")
    add_user_parser.add_argument("username", action="store", help="unique username")
    add_user_parser.add_argument("password", action="store", help="password")
    add_user_parser.add_argument("first_name", action="store", help="first name")
    add_user_parser.add_argument("last_name", action="store", help="last name")
    add_user_parser.add_argument("is_superuser", action="store", help="True/False")
    add_user_parser.add_argument("email", action="store", help="email")
    add_user_parser.set_defaults(func = lambda args: add_user(args.username, args.password, \
        args.first_name, args.last_name, args.email, args.is_superuser))

    flag_items_parser = subparsers.add_parser("flag", help="For testing only. Randomly flag results.")
    flag_items_parser.set_defaults(func = lambda args: flag_items())

    unflag_items_parser = subparsers.add_parser("unflag", help="Reset all flags to false.")
    unflag_items_parser.set_defaults(func = lambda args: clear_flags())

    args = argparser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
