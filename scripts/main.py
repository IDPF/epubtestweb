import argparse
import os
import yaml
from testsuite_app import models
from testsuite_app import export_data

from admin_functions import *
from import_testsuite import import_testsuite

import refactor_functions

from django.contrib.sessions.models import Session
from datetime import datetime
from import_migration_data import import_migration_data

def export(outfile):
    print ("Exporting data")
    xmldoc = export_data.export_all_current_reading_systems(None)
    xmldoc.write(outfile)
    print ("Data exported to {}".format(outfile))

def import_data(infile):
    print ("Importing from {}".format(infile))
    import_migration_data(infile)
    print ("Done")

def main():
    import django
    django.setup()
    
    argparser = argparse.ArgumentParser(description="epubtest.org command line")
    subparsers = argparser.add_subparsers(help='commands')
    import_parser = subparsers.add_parser('import', help='Import a testsuite into the database')
    import_parser.add_argument("source", action="store", help="Folder containing EPUBs")
    import_parser.add_argument("config", action="store", default="categories.yaml", help="categories config file")
    import_parser.set_defaults(func = lambda args: import_testsuite.add_testsuites(args.source, args.config))

    export_parser = subparsers.add_parser('export', help="Export evaluation data for all reading systems")
    export_parser.add_argument("file", action="store", help="store the xml file here")
    export_parser.set_defaults(func = lambda args: export(args.file))

    listrs_parser = subparsers.add_parser('listrs', help="List all reading systems and their IDs")
    listrs_parser.set_defaults(func = lambda args: listrs())

    emails_parser = subparsers.add_parser('emails', help="List user emails")
    emails_parser.set_defaults(func = lambda args: getemails())

    listusers_parser = subparsers.add_parser("listusers", help="list all users")
    listusers_parser.set_defaults(func = lambda args: listusers())

    list_logged_in_users_parser = subparsers.add_parser("list-logged-in-users", help="list logged in users")
    list_logged_in_users_parser.set_defaults(func = lambda args: list_logged_in_users())

    import_data_parser = subparsers.add_parser("import-data", help="Import evaluation data in XML format")
    import_data_parser.add_argument("file", action="store", help="XML file containing data to import")
    import_data_parser.set_defaults(func = lambda args: import_data(args.file))

    args = argparser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
