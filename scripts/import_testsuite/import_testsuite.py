from testsuite_app.models import *
from . import epub_parser
from .epub_id_check import EpubIdCheck
import os
import yaml
from . import db_helper
from . import migrate

# entry point into importing new data: add_testsuites
# import testsuites from the YAML configuration file
def add_testsuites(epub_sourcedir, config_file):
    epub_sourcedir_path = os.path.normpath(epub_sourcedir)
    config_file_path = os.path.normpath(config_file)
    print("\nProcessing {0} (config = {1})".format(epub_sourcedir_path, config_file_path))
    testsuites_config = yaml.load(open(config_file_path).read())['TestSuites']

    for config_section in testsuites_config:
        add_testsuite(config_section, epub_sourcedir_path)

# look at each referenced epub in the testsuite config section
def add_testsuite(config_section, sourcedir):
    yaml_categories = config_section['Categories']
    testsuite_type = common.TESTSUITE_TYPE_DEFAULT
    if config_section['Type'] == "accessibility":
        testsuite_type = common.TESTSUITE_TYPE_ACCESSIBILITY

    migrator = None

    # remove the old testsuite, categories, features
    old_testsuite = TestSuite.objects.get_testsuite(testsuite_type)
    if old_testsuite != None:
        migrator = migrate.MigrateData()
        migrator.pre_migrate(old_testsuite)


    testsuite = create_testsuite(config_section)
    # associate the new testsuite before deleting the old one
    if migrator != None:
        migrator.update_testsuite(testsuite)
    if old_testsuite != None:
        old_testsuite.delete() # this also deletes attached objects

    epub_id_checker = EpubIdCheck()
    epub_id_checker.process_epubs(sourcedir)
    for cat in yaml_categories:
        for epubid in cat['EpubIds']:
            if Epub.objects.filter(epubid = epubid).exists():
                continue
            filename = epub_id_checker.get_filename_for_id(epubid)
            epubparser = epub_parser.EpubParser()
            epubparser.parse(filename, testsuite)


    import_features_and_categories(config_section, testsuite)
    num_tests = Test.objects.filter(testsuite = testsuite).count()
    print("This testsuite contains {0} tests".format(num_tests))
    if migrator != None:
        migrator.migrate()

    print("Done importing testsuite.")

    return testsuite

def create_testsuite(config_section):
    # how many evaluations per reading system allowed for this testsuite
    allow_many_evaluations = config_section["AllowManyEvaluations"]
    testsuite_type = common.TESTSUITE_TYPE_DEFAULT
    if config_section['Type'] == "accessibility":
        testsuite_type = common.TESTSUITE_TYPE_ACCESSIBILITY
    return db_helper.add_testsuite(testsuite_type, config_section['Id'], config_section['Name'], allow_many_evaluations)

# to be called after the epubs are imported into the database
# config_section = top-level testsuite YAML config section
def import_features_and_categories(config_section, testsuite):
    categories = config_section['Categories']
    for category in categories:
        if 'SuperCategory' in category:
            db_category = db_helper.add_category(category['Name'], category['Id'], category['SuperCategory'], testsuite)
        else:
            db_category = db_helper.add_category(category['Name'], category['Id'], "", testsuite)
        for feature in category['Features']:
            db_feature = db_helper.add_feature(feature['Id'], feature['Name'], db_category, testsuite)

            for testid in feature['TestIds']:
                db_test = testsuite.get_test_by_id(testid)
                if db_test == None:
                    print("Warning: test {0} not found in database.".format(testid))
                else:
                    db_test.feature = db_feature
                    db_test.category = db_category
                    db_test.save()

    feature_sanity_check(testsuite)


# check that all database tests have features assigned to them
def feature_sanity_check(testsuite):
    tests = testsuite.get_tests()
    for test in tests:
        if test.feature == None:
            print("Warning: test {0} does not belong to a feature.".format(test.test_id))


def print_testsuite_structure(testsuite):
    print("*******************")
    print(testsuite.name)
    categories = testsuite.get_categories()
    for cat in categories:
        print("Category: {}".format(cat.name))
        features = cat.get_features()
        for feat in features:
            print("Feature: {}".format(feat.name))
            tests = feat.get_tests()
            print("Tests: {}".format(tests))
    print("*******************")
