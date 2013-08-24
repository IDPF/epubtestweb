# useful database functions related to importing the testsuite

from testsuite_app.models import *
from testsuite_app.web_db_helper import *
from datetime import datetime

def generate_version_info():
    todays_date = datetime.today()
    version_date = "{0}-{1}-{2}".format(str(todays_date.year), str(todays_date.month).zfill(2), str(todays_date.day).zfill(2))
    same_date = TestSuite.objects.filter(version_date = version_date).order_by("-version_revision")
    version_revision = 1
    if len(same_date) != 0:
        version_revision = same_date[0].version_revision + 1
    return (version_date, version_revision)

def add_testsuite():
    version_date, version_revision = generate_version_info()
    print "Adding TestSuite version {0}-{1}".format(version_date, version_revision)
    ts = TestSuite(version_date = version_date, version_revision = version_revision)
    ts.save()
    return ts

def add_category(category_type, name, parent_category, testsuite):
    db_category = Category(
        category_type = category_type,
        name = name,
        parent_category = parent_category,
        testsuite = testsuite
    )
    db_category.save()
    return db_category

def add_test(name, description, parent_category, required, testid, testsuite, xhtml):
    db_test = Test(
        name = name,
        description = description,
        parent_category = parent_category,
        required = required,
        testid = testid,
        testsuite = testsuite,
        xhtml = xhtml
    )
    db_test.save()
    return db_test

def add_category_restriction(category, limit):
    limit_ = '1'
    for option in Category.CATEGORY_TYPE:
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
    for option in Category.CATEGORY_TYPE:
        if restriction == option[1]:
            return int(option[0])
    return 3 #the most relaxed restriction



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

    depth = get_depth(item)
    print "{0}{1}{2}".format("\t" * depth, prefix, item.description.encode('utf-8'))
