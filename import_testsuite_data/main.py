import argparse
import os
import yaml
import epub_parser
import import_testsuite
from testsuite_app import models
from testsuite_app.models import common
from testsuite_app import helper_functions
from testsuite_app import export_data
from random import randrange

def print_testsuite():
    rs = models.ReadingSystem.objects.get(id=1)
    res = helper_functions.get_results_as_nested_categories(rs)
    for r in res:
        helper_functions.print_item_summary(r)

def clear_data():
    models.UserProfile.objects.all().delete()
    models.ReadingSystem.objects.all().delete()

# look at each referenced epub in the categories.yaml file
# parse it and put the data under a category header
def add_testsuite(sourcedir, config_file):
    norm_sourcedir = os.path.normpath(sourcedir)
    norm_config_file = os.path.normpath(config_file)
    print "\nProcessing {0} (config = {1})".format(norm_sourcedir, norm_config_file)
    old_testsuite = models.TestSuite.objects.get_most_recent_testsuite()
    testsuite = import_testsuite.create_testsuite()
    yaml_categories = yaml.load(open(norm_config_file).read())['Categories']

    for cat in yaml_categories:
        new_category = import_testsuite.add_category('1', cat['Name'], None, testsuite, None)
        for epub in cat['Files']:
            fullpath = os.path.join(norm_sourcedir, epub)
            if os.path.isdir(fullpath):
                # this will add a new testsuite
                epubparser = epub_parser.EpubParser()
                epubparser.parse(fullpath, new_category, testsuite, cat['CategoryDisplayDepthLimit'])
            else:
                print "Not a directory: {0}".format(fullpath)

    import_testsuite.migrate_data(old_testsuite)
    print "Done importing testsuite."

def add_user(username, email, password, firstname, lastname):
    user = models.UserProfile.objects.create_user(username, email, password)
    user.first_name = firstname
    user.last_name = lastname
    user.is_superuser = False
    user.save()
    return user

def add_rs(name):
    user = models.UserProfile.objects.all()[0]
    rs = models.ReadingSystem(
        locale = "US",
        name = name,
        operating_system = "OSX",
        sdk_version = "N/A",
        version = "1.0",
        user = user,
        visibility = common.VISIBILITY_PUBLIC,
    )
    rs.save() # save now to generate an initial evaluation
    
    geneval(rs.pk)

    return rs

# settings.py must contain a definition for the 'previous' database in order for this to work
def copy_users():
    users = models.UserProfile.objects.using('previous').all()
    for u in users:
        u.save(using='default')
    print "Copied users from old database."

def rollback():
    "roll back to the previous testsuite version, or just remove eval data if there is no previous version"
    ts = models.TestSuite.objects.get_most_recent_testsuite()
    evals = models.Evaluation.objects.filter(testsuite = ts)
    for e in evals:
        e.delete()
    ts.delete()

def export(outfile):
    xmldoc = export_data.export_all_current_evaluations(None)
    xmldoc.write(outfile)
    print "Data exported to {0}".format(outfile)

def listrs():
    rses = models.ReadingSystem.objects.all()
    for rs in rses:
        print "{0}: {1}".format(rs.name, rs.pk)

def geneval(rspk):
    try:
        rs = models.ReadingSystem.objects.get(id=rspk)
    except models.ReadingSystem.DoesNotExist:
        return
    evaluation = rs.get_current_evaluation()
    # generate result data
    results = evaluation.get_all_results()
    for r in results:
        r.result = str(randrange(1, 3))
        r.save()
    evaluation.save()

def getemails():
    users = models.UserProfile.objects.all()
    # SELECT DISTINCT on fields not supported by SQLite backend so we have to do it manually
    # luckily this is an isolated case with a small dataset, and one where we can afford to be a little slow
    distinct_emails = []
    for u in users:
        if u.email not in distinct_emails:
            distinct_emails.append(u.email)
    emails = ", ".join(distinct_emails)
    print emails

def main():
    argparser = argparse.ArgumentParser(description="Collect tests")
    subparsers = argparser.add_subparsers(help='commands')
    import_parser = subparsers.add_parser('import', help='Import a testsuite into the database')
    import_parser.add_argument("source", action="store", help="Folder containing EPUBs")
    import_parser.add_argument("config", action="store", default="categories.yaml", help="categories config file")
    import_parser.set_defaults(func = lambda(args): add_testsuite(args.source, args.config))

    print_parser = subparsers.add_parser('print', help="Print (some) contents of the database")
    print_parser.set_defaults(func = lambda(args): print_testsuite())

    clear_data_parser = subparsers.add_parser('clear', help="Clear user and reading system data from the database")
    clear_data_parser.set_defaults(func = lambda(args): clear_data())

    add_user_parser = subparsers.add_parser('add-user', help="Add a new user")
    add_user_parser.add_argument('username', action="store", help="username")
    add_user_parser.add_argument('password', action="store", help="password")
    add_user_parser.add_argument('email', action="store", help="email")
    add_user_parser.add_argument('--firstname', action="store", help="first name", default="")
    add_user_parser.add_argument('--lastname', action="store", help="last name", default="")
    add_user_parser.set_defaults(func = lambda(args): add_user(args.username, args.email, args.password, args.firstname, args.lastname))

    add_rs_parser = subparsers.add_parser('add-rs', help="Add a new reading system")
    add_rs_parser.add_argument('name', action="store", help="reading system name")
    add_rs_parser.set_defaults(func = lambda(args): add_rs(args.name))

    copy_users_parser = subparsers.add_parser('copy-users', help="Copy all users")
    copy_users_parser.set_defaults(func = lambda(args): copy_users())

    rollback_parser = subparsers.add_parser('rollback', help="Roll back to the previous testsuite")
    rollback_parser.set_defaults(func = lambda(args): rollback())

    export_parser = subparsers.add_parser('export', help="Export evaluation data for all reading systems")
    export_parser.add_argument("file", action="store", help="store the xml file here")
    export_parser.set_defaults(func = lambda(args): export(args.file))

    geneval_parser = subparsers.add_parser('geneval', help="Generate random evaluation data for the given reading system")
    geneval_parser.add_argument("rs", action="store", help="reading system ID")
    geneval_parser.set_defaults(func = lambda(args): geneval(args.rs))

    listrs_parser = subparsers.add_parser('listrs', help="List all reading systems and their IDs")
    listrs_parser.set_defaults(func = lambda(args): listrs())

    emails_parser = subparsers.add_parser('emails', help="List user emails")
    emails_parser.set_defaults(func = lambda(args): getemails())

    args = argparser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
