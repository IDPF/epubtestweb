import argparse
import os
import yaml
import parser
import import_db_helper
import dummy
from testsuite_app import web_db_helper, models

def add_dummy_data(args):
    dummy.add_data()

def clear_dummy_data(args):
    dummy.clear_data()

def print_testsuite(args):
    #import_db_helper.print_db(None)
    rs = models.ReadingSystem.objects.get(id=1)
    web_db_helper.get_reading_system_performance_summary(rs)

# look at each referenced epub in the categories.yaml file
# parse it and put the data under a category header
def import_testsuite(args):
    print "Processing {0}".format(args.source)
    testsuite = import_db_helper.add_testsuite()

    yaml_categories = yaml.load(open("categories.yaml").read())['Categories']

    for cat in yaml_categories:
        new_category = import_db_helper.add_category('1', cat['Name'], None, testsuite)
        #import_db_helper.add_category_restriction(new_category, cat['CategoryDisplayDepthLimit'])
        for epub in cat['Files']:
            fullpath = os.path.join(args.source, epub)
            if os.path.isdir(fullpath):
                # this will add a new testsuite
                epub_parser = parser.EpubParser()
                epub_parser.parse(fullpath, new_category, testsuite, cat['CategoryDisplayDepthLimit'])

    # TODO: look for any tests that haven't changed since the last import
    # and copy reading system results over
    # the reason we re-import the tests at all is because the category structure may have changed

def add_user(args):
    user = models.UserProfile.objects.create_user(args.username, args.email, args.password)
    user.first_name = args.firstname
    user.last_name = args.lastname
    user.is_superuser = False
    user.default_evaluation_type = "1"
    user.organization = args.organization
    user.save()

    return (user)

def add_eval(args):
    user = models.UserProfile.objects.all()[0]
    if user == None:
        print "No user; could not create evaluation."
        return

    rs = dummy.add_reading_system()
    dummy.add_evaluation(user, rs)
    print "Data added."

def main():
    argparser = argparse.ArgumentParser(description="Collect tests")
    subparsers = argparser.add_subparsers(help='commands')
    import_parser = subparsers.add_parser('import', help='Import a testsuite into the database')
    import_parser.add_argument("source", action="store", help="Folder containing EPUBs")
    import_parser.set_defaults(func = import_testsuite)

    print_parser = subparsers.add_parser('print', help="Print (some) contents of the database")
    print_parser.set_defaults(func = print_testsuite)

    add_dummy_parser = subparsers.add_parser('dummy', help="Add dummy data to the database")
    add_dummy_parser.set_defaults(func = add_dummy_data)

    clear_dummy_parser = subparsers.add_parser('clear', help="Clear dummy data from the database")
    clear_dummy_parser.set_defaults(func = clear_dummy_data)

    add_user_parser = subparsers.add_parser('add-user', help="Add a new user")
    add_user_parser.add_argument('username', action="store", help="username")
    add_user_parser.add_argument('password', action="store", help="password")
    add_user_parser.add_argument('email', action="store", help="email")
    add_user_parser.add_argument('--firstname', action="store", help="first name", default="")
    add_user_parser.add_argument('--lastname', action="store", help="last name", default="")
    add_user_parser.add_argument('--organization', action="store", help="organization", default="")
    add_user_parser.set_defaults(func = add_user)

    add_eval_parser = subparsers.add_parser('add-evaluation', help="Add a new evaluation")
    add_eval_parser.set_defaults(func = add_eval)


    args = argparser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
