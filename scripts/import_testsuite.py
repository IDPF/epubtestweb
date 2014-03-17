# useful database functions related to importing the testsuite

from testsuite_app.models import *
from datetime import datetime
from testsuite_app.models import common

def generate_version_info():
    todays_date = datetime.today()
    version_date = "{0}-{1}-{2}".format(str(todays_date.year), str(todays_date.month).zfill(2), str(todays_date.day).zfill(2))
    same_date = TestSuite.objects.filter(version_date = version_date).order_by("-version_revision")
    version_revision = 1
    if len(same_date) != 0:
        version_revision = same_date[0].version_revision + 1
    return (version_date, version_revision)

def create_testsuite(ts_type):
    version_date, version_revision = generate_version_info()
    print "Creating TestSuite version {0}-{1}".format(version_date, version_revision)
    ts_type_ = common.TESTSUITE_TYPE_DEFAULT
    if ts_type == "Accessibility":
        print "accessible testsuite"
        ts_type_ = common.TESTSUITE_TYPE_ACCESSIBILITY
    ts = TestSuite(version_date = version_date, version_revision = version_revision, testsuite_type = ts_type_)
    ts.save()
    return ts

def add_category(category_type, name, parent_category, testsuite, source, flag=False):
    db_category = Category(
        category_type = category_type,
        name = name,
        parent_category = parent_category,
        testsuite = testsuite,
        source = source,
        temp_flag = flag,
    )
    db_category.save()
    return db_category

def add_test(name, description, parent_category, required, testid, testsuite, xhtml, source, access_type, is_advanced):
    db_test = Test(
        name = name,
        description = description,
        parent_category = parent_category,
        required = required,
        testid = testid,
        testsuite = testsuite,
        xhtml = xhtml,
        source = source
    )
    db_test.save()

    # only accessible tests need metadata right now
    if access_type != "":
        metadata = TestMetadata(test = db_test, access_type = access_type, is_advanced = is_advanced)
        metadata.save()
    
    return db_test

def add_category_restriction(category, limit):
    limit_ = '1'
    for option in common.CATEGORY_TYPE:
        if option[1] == limit:
            limit_ = option[0]
            break
    db_category_restriction = CategoryRestriction(
        category = category,
        category_display_depth_limit = limit_
    )
    db_category_restriction.save()
    return db_category_restriction

def category_restriction_to_int(restriction):
    for option in common.CATEGORY_TYPE:
        if restriction == option[1]:
            return int(option[0])
    return 3 #the most relaxed restriction

def migrate_data(previous_testsuite):
    "look for any tests that haven't changed since the last import and copy reading system results over"
    print "Looking for data to migrate"
    reading_systems = ReadingSystem.objects.all()
    for rs in reading_systems:
        old_evaluation = rs.get_evaluation_for_testsuite(previous_testsuite)
        new_evaluation = Evaluation.objects.create_evaluation(rs)
        
        print "Migrating data for {0} {1} {2}".format(rs.name, rs.version, rs.operating_system)
        results = new_evaluation.get_all_results(new_evaluation.get_default_result_set())
        print "Processing {0} results".format(results.count())
        flag_evaluation = False
        for result in results:
            try:
                old_test_version = Test.objects.get(testsuite = old_evaluation.testsuite, testid = result.test.testid)
            except Test.DoesNotExist:
                # the test may be new
                print "No previous version of test {0} was found".format(result.test.testid)
                result.test.flagged_as_new = True
                result.test.save()
                #new_evaluation.flagged_for_review = True
                continue

            # if the ID (checked above) and xhtml for the test matches, then copy over the old result
            if result.test.xhtml == old_test_version.xhtml:
                # print "Copying previous result for {0}".format(old_test_version.testid)
                previous_result = old_evaluation.get_result_by_testid(result.test.testid)
                result.result = previous_result.result
                result.notes = previous_result.notes
                result.save()
            else:
                print "Test {0} has changed from the previous test suite".format(result.test.testid)
                result.test.flagged_as_changed = True
                result.test.save()
                #new_evaluation.flagged_for_review = True
        new_evaluation.save()


# debug functions

def print_db(parent_category):
    categories = Category.objects.filter(parent_category = parent_category)
    for c in categories:
        print_item(c)
        print_db(c)

    tests = Test.objects.filter(parent_category = parent_category)
    for t in tests:
        print_item(t)

# item is a Test or Category
def print_item(item):
    prefix = ""
    if type(item) == Test:
        prefix = "Test: "

    print "{0}{1}{2}".format("\t" * item.depth, prefix, item.description.encode('utf-8'))
