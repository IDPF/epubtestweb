from testsuite.models import *
from datetime import datetime
import epub_parser
from epub_id_check import EpubIdCheck

# entry point into importing new data: add_testsuites
# import testsuites from the YAML configuration file
def add_testsuites(epub_sourcedir, config_file):
    epub_sourcedir_path = os.path.normpath(sourcedir)
    config_file_path = os.path.normpath(config_file)
    print "\nProcessing {0} (config = {1})".format(epub_sourcedir_path, config_file_path)
    testsuites_config = yaml.load(open(norm_config_file).read())['TestSuites']
    for config_section in testsuites_config:
        add_testsuite(config_section, epub_sourcedir_path)

# look at each referenced epub in the testsuite config section
def add_testsuite(config_section, sourcedir):
    yaml_categories = config_section['Categories']
    testsuite_type = common.TESTSUITE_TYPE_DEFAULT
    if config_section['Type'] == "accessibility":
        testsuite_type = common.TESTSUITE_TYPE_ACCESSIBILITY
    old_testsuite = models.TestSuite.objects.get_most_recent_testsuite_of_type(testsuite_type)
    testsuite = create_testsuite(config_section)

    epub_id_checker = EpubIdCheck()
    epub_id_checker.process_epubs(sourcedir)
    for cat in yaml_categories:
        category = add_category(cat['Name'], cat['Id'], testsuite)
        for epubid in cat['EpubIds']:
            filename = epub_id_checker.get_filename_for_id(epubid)
            epubparser = epub_parser.EpubParser()
            epubparser.parse(filename, category, testsuite)

    num_tests = models.Test.objects.filter(testsuite = testsuite).count()
    print "This testsuite contains {0} tests".format(num_tests)
    if old_testsuite != None:
        migrate.migrate_data(old_testsuite)
    else:
        print "Nothing to migrate"
    print "Done importing testsuite."
    return testsuite

def generate_version_info():
    todays_date = datetime.today()
    version_date = "{0}-{1}-{2}".format(str(todays_date.year), str(todays_date.month).zfill(2), str(todays_date.day).zfill(2))
    same_date = TestSuite.objects.filter(version_date = version_date).order_by("-version_revision")
    version_revision = 1
    if len(same_date) != 0:
        version_revision = same_date[0].version_revision + 1
    return (version_date, version_revision)

def create_testsuite(config_section):
    version_date, version_revision = generate_version_info()
    print "Creating Test Suite version {0}-{1}, type: {2}".format(version_date, version_revision, config_section['Type'])

    # how many evaluations per reading system allowed for this testsuite
    allowed = common.TESTSUITE_ALLOW_ONE
    if config_section['Allow'] == "Many":
        allowed = common.TESTSUITE_ALLOW_MANY

    db_testsuite = TestSuite(version_date = version_date, 
        version_revision = version_revision, 
        testsuite_type = config_section['Type'],
        testsuite_id = config_section['Id'],
        name = config_section['Name'],
        allow = allowed)
    db_testsuite.save()
    return db_testsuite

def add_epub(epubid, title, description, category):
    db_epub = Epub(
        epubid = epubid,
        title = title,
        description = description,
        category = category)
    db_epub.save()
    return db_epub

def add_category(name, catid, testsuite):
    db_category = Category(
        name = name,
        testsuite = testsuite,
        catid = catid
    )
    db_category.save()
    return db_category

def add_test(name, description, category, required, testid, testsuite, xhtml, epub, is_advanced, allow_na, order_in_book):
    db_test = Test(
        name = name,
        description = description,
        category = category,
        required = required,
        testid = testid,
        testsuite = testsuite,
        xhtml = xhtml,
        epub = epub,
        allow_na = allow_na,
        order_in_book = order_in_book
    )
    db_test.save()

    # only accessible tests need metadata right now
    if testsuite.testsuite_type == common.TESTSUITE_TYPE_ACCESSIBILITY:
        metadata = TestMetadata(test = db_test, is_advanced = is_advanced)
        metadata.save()
    
    return db_test

def add_feature(featureid, name, category):
    db_feature = Feature(
        featureid = featureid,
        name = name, 
        category = category)
    db_feature.save()
    return db_feature

