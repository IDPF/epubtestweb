from testsuite_app.models import *
from . import epub_parser
from .epub_id_check import EpubIdCheck
import os
import yaml
from . import db_helper
from . import import_features

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
    old_testsuite = TestSuite.objects.get_most_recent_testsuite(testsuite_type)
    testsuite = create_testsuite(config_section)

    epub_id_checker = EpubIdCheck()
    epub_id_checker.process_epubs(sourcedir)
    for cat in yaml_categories:
        print(cat['Name'])
        category = db_helper.add_category(cat['Name'], cat['Id'], testsuite)
        for epubid in cat['EpubIds']:
            filename = epub_id_checker.get_filename_for_id(epubid)
            epubparser = epub_parser.EpubParser()
            epubparser.parse(filename, category, testsuite)

    import_features.import_features(config_section, testsuite)
    num_tests = Test.objects.filter(testsuite = testsuite).count()
    print("This testsuite contains {0} tests".format(num_tests))
    if old_testsuite != None:
        pass#migrate.migrate_data(old_testsuite)
    else:
        print("Nothing to migrate")

    print("Done importing testsuite.")
    return testsuite

def create_testsuite(config_section):
    # how many evaluations per reading system allowed for this testsuite
    allow_many_evaluations = config_section["AllowManyEvaluations"]
    testsuite_type = common.TESTSUITE_TYPE_DEFAULT
    if config_section['Type'] == "accessibility":
        testsuite_type = common.TESTSUITE_TYPE_ACCESSIBILITY
    return db_helper.add_testsuite(testsuite_type, config_section['Id'], config_section['Name'], allow_many_evaluations)

