from testsuite_app.models import *
import os
from datetime import datetime


def add_testsuite(testsuite_type, testsuite_id, name, allow_many_evaluations):
    todays_date = datetime.today()
    version_date = "{0}-{1}-{2}".format(str(todays_date.year), str(todays_date.month).zfill(2), str(todays_date.day).zfill(2))
    print("Creating Test Suite version {}, type: {}".format(version_date, testsuite_type))
    db_testsuite = TestSuite(version_date = version_date, 
        testsuite_type = testsuite_type,
        testsuite_id = testsuite_id,
        name = name,
        allow_many_evaluations = allow_many_evaluations)
    db_testsuite.save()
    return db_testsuite

def add_category(name, category_id, testsuite):
    db_category = Category(
        name = name,
        testsuite = testsuite,
        category_id = category_id,
    )
    db_category.save()
    return db_category

def add_test(name, description, required, test_id, testsuite, xhtml, epub, order_in_book):
    db_test = Test(
        name = name,
        description = description,
        required = required,
        test_id = test_id,
        testsuite = testsuite,
        xhtml = xhtml,
        epub = epub,
        order_in_book = order_in_book
    )
    db_test.save()

    return db_test

def add_feature(featureid, name, category, testsuite):
    db_feature = Feature(
        feature_id = featureid,
        name = name, 
        category = category,
        testsuite = testsuite)
    db_feature.save()
    return db_feature

def add_epub(epubid, title, description, testsuite, filename):
    # see if it exists already
    epub = Epub.objects.filter(epubid = epubid, testsuite = testsuite)
    if len(epub) > 0:
        return epub[0]

    db_epub = Epub(
        epubid = epubid,
        title = title,
        description = description,
        testsuite = testsuite,
        filename = os.path.basename(filename))
    db_epub.save()
    return db_epub
