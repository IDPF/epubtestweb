from testsuite_app.models import *
import os
from datetime import datetime

def generate_version_info():
    todays_date = datetime.today()
    version_date = "{0}-{1}-{2}".format(str(todays_date.year), str(todays_date.month).zfill(2), str(todays_date.day).zfill(2))
    same_date = TestSuite.objects.filter(version_date = version_date).order_by("-version_revision")
    version_revision = 1
    if len(same_date) != 0:
        version_revision = same_date[0].version_revision + 1
    return (version_date, version_revision)

def add_testsuite(testsuite_type, testsuite_id, name, allow_many_evaluations):
    version_date, version_revision = generate_version_info()
    print("Creating Test Suite version {0}-{1}, type: {2}".format(version_date, version_revision, testsuite_type))
    db_testsuite = TestSuite(version_date = version_date, 
        version_revision = version_revision, 
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

def add_test(name, description, category, required, test_id, testsuite, xhtml, epub, is_advanced, allow_na, order_in_book):
    if Test.objects.already_exists(test_id):
        print("WARNING: Test {0} already exists. Skipping.".format(test_id))
        return None
    
    db_test = Test(
        name = name,
        description = description,
        category = category,
        required = required,
        test_id = test_id,
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
        feature_id = featureid,
        name = name, 
        category = category)
    db_feature.save()
    return db_feature

def add_epub(epubid, title, description, category, filename):
        db_epub = Epub(
            epubid = epubid,
            title = title,
            description = description,
            category = category,
            filename = os.path.basename(filename))
        db_epub.save()
        return db_epub
