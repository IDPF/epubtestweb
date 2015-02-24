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
    if ts_type == common.TESTSUITE_TYPE_ACCESSIBILITY:
        print "accessibility testsuite"
    ts = TestSuite(version_date = version_date, version_revision = version_revision, testsuite_type = ts_type)
    ts.save()
    return ts

def add_category(category_type, name, desc, parent_category, testsuite, source):
    db_category = Category(
        category_type = category_type,
        name = name,
        parent_category = parent_category,
        testsuite = testsuite,
        source = source,
        desc = desc
    )
    db_category.save()
    return db_category

def add_test(name, description, parent_category, required, testid, testsuite, xhtml, source, is_advanced, allow_na):
    db_test = Test(
        name = name,
        description = description,
        parent_category = parent_category,
        required = required,
        testid = testid,
        testsuite = testsuite,
        xhtml = xhtml,
        source = source,
        allow_na = allow_na
    )
    db_test.save()

    # only accessible tests need metadata right now
    if testsuite.testsuite_type == common.TESTSUITE_TYPE_ACCESSIBILITY:
        metadata = TestMetadata(test = db_test, is_advanced = is_advanced)
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
    testsuite = None
    if previous_testsuite.testsuite_type == common.TESTSUITE_TYPE_DEFAULT:
        testsuite = TestSuite.objects.get_most_recent_testsuite()
    else:
        testsuite = TestSuite.objects.get_most_recent_accessibility_testsuite()
    
    for rs in reading_systems:
        old_result_sets = rs.get_result_sets_for_testsuite(previous_testsuite)
        for old_rset in old_result_sets:
            new_result_set = ResultSet.objects.create_result_set(rs, testsuite, old_rset.user)
            new_result_set.copy_metadata(old_rset)

            
            print "Migrating data for {0} {1} {2}".format(rs.name.encode('utf-8'), rs.version.encode('utf-8'), rs.operating_system.encode('utf-8'))
            results = new_result_set.get_results()
            print "Processing {0} results".format(results.count())
            
            for result in results:
                try:
                    old_test_version = Test.objects.get(testsuite = previous_testsuite, testid = result.test.testid)
                except Test.DoesNotExist:
                    # the test may be new
                    print "No previous version of test {0} was found".format(result.test.testid)
                    result.test.flagged_as_new = True
                    result.test.save()
                    continue

                # if the ID (checked above) and xhtml for the test matches, then copy over the old result
                if result.test.xhtml == old_test_version.xhtml:
                    # print "Copying previous result for {0}".format(old_test_version.testid)
                    previous_result = old_rset.get_result_for_test_by_id(result.test.testid)
                    result.result = previous_result.result
                    result.notes = previous_result.notes
                    result.save()
                else:
                    print "Test {0} has changed from the previous test suite".format(result.test.testid)
                    result.test.flagged_as_changed = True
                    result.test.save()
            new_result_set.save()


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
