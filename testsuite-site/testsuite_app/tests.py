from django.test import TestCase
from testsuite_app.models import Category, ReadingSystem, Result, Score, Test, TestSuite, UserProfile, ResultSet
from testsuite_app.helper_functions import generate_timestamp
from scripts import main
import os
from testsuite_app.models import common
from datetime import datetime
from decimal import Decimal
import yaml

"""
IMPORTANT NOTE: comment out 'django_evolution' from the list of INSTALLED_APPS in settings.py; 
it interferes with the unit testing
"""

def get_testsuite_v1_path():
    path = os.path.abspath(__file__)
    return os.path.normpath(os.path.join(path, "../../../test_data/testsuite_v1"))

def get_testsuite_v2_path():
    path = os.path.abspath(__file__)
    return os.path.normpath(os.path.join(path, "../../../test_data/testsuite_v2"))

def get_config_path():
    path = os.path.abspath(__file__)
    return os.path.normpath(os.path.join(path, "../../../test_data/categories.yaml"))

def add_ts_v1():
    path = get_testsuite_v1_path()
    config_path = get_config_path()
    testsuites = yaml.load(open(config_path).read())['TestSuites']

    main.add_testsuite(testsuites[0], get_testsuite_v1_path())

def add_ts_v2():
    path = get_testsuite_v2_path()
    config_path = get_config_path()
    testsuites = yaml.load(open(config_path).read())['TestSuites']

    main.add_testsuite(testsuites[0], get_testsuite_v2_path())

def add_user():
    main.add_user("testuser", "test@example.com", "password", "FirstName", "LastName")

def add_rs():
    # assume a user was already added
    user = UserProfile.objects.all()[0]
    rs = ReadingSystem(
        locale = "US",
        name = "Reader",
        operating_system = "OSX",
        notes = "NOTES",
        version = "2.0",
        user = user,
    )
    rs.save() 
    return rs

def add_result_set(rs):
    testsuite = TestSuite.objects.get_most_recent_testsuite()
    result_set = ResultSet.objects.create_result_set(rs, testsuite, rs.user)
    result_set.save()
    result_set.add_metadata("assistive_technology", common.INPUT_TYPE_KEYBOARD, False, False)
    return result_set

def fill_out_evaluation(result_set):
    results = result_set.get_results()
    r0 = results[0]
    r1 = results[1]
    r2 = results[2]
    r0.result = common.RESULT_SUPPORTED
    r0.notes = "Test note"
    r1.result = common.RESULT_NOT_SUPPORTED
    r2.result = common.RESULT_SUPPORTED
    r0.save()
    r1.save()
    r2.save()
    result_set.save()


class ImportTestSuite(TestCase):
    def setUp(self):
        add_ts_v1()        

    def test_number_of_testsuites(self):
        "Test that there is one testsuite"
        self.assertEqual(TestSuite.objects.all().count(), 1)

    def test_testsuite_version(self):
        "Test that the testsuite version is correct"
        # the date is correct
        todays_date = datetime.today()
        self.assertEqual(TestSuite.objects.all()[0].version_date, datetime.today().date())
        self.assertEqual(TestSuite.objects.all()[0].version_revision, 1)

    def test_number_of_objects(self):
        "Test that there are 3 tests and 4 categories"
        self.assertEqual(Test.objects.all().count(), 3)
        self.assertEqual(Category.objects.all().count(), 4)

    def test_category_objects(self):
        "Test that the categories are correct"
        ts = TestSuite.objects.all()[0]
        # top-level category
        top_level_cat = Category.objects.get(parent_category = None)
        self.assertNotEqual(top_level_cat, None)
        self.assertEqual(top_level_cat.name, "Top-level category")
        self.assertEqual(top_level_cat.category_type, common.CATEGORY_EXTERNAL) 
        self.assertEqual(top_level_cat.testsuite, ts)
        self.assertEqual(top_level_cat.source, None)

        # ebook-level category
        epub_cat = Category.objects.get(parent_category = top_level_cat)
        self.assertNotEqual(epub_cat, None)
        self.assertEqual(epub_cat.name, "EPUBTEST.ORG test content")
        self.assertEqual(epub_cat.category_type, common.CATEGORY_EPUB)
        self.assertEqual(epub_cat.testsuite, ts)
        self.assertEqual(epub_cat.source, 'epub')

        # nav.xhtml categories
        nav_cats = Category.objects.filter(parent_category = epub_cat)
        self.assertEqual(nav_cats.count(), 1)
        self.assertEqual(nav_cats[0].parent_category, epub_cat)
        self.assertEqual(nav_cats[0].name, "Test Category")
        self.assertEqual(nav_cats[0].category_type, common.CATEGORY_INTERNAL)
        self.assertEqual(nav_cats[0].testsuite, ts)
        self.assertEqual(nav_cats[0].source, 'epub')
        
        nav_subcats = Category.objects.filter(parent_category = nav_cats[0])
        self.assertEqual(nav_subcats.count(), 1)
        self.assertEqual(nav_subcats[0].parent_category, nav_cats[0])
        self.assertEqual(nav_subcats[0].name, "Test Sub-Category")
        self.assertEqual(nav_subcats[0].category_type, common.CATEGORY_INTERNAL)
        self.assertEqual(nav_subcats[0].testsuite, ts)
        self.assertEqual(nav_subcats[0].source, 'epub')

    def test_test_objects(self):
        "Test that the tests are correct"
        tests = Test.objects.all()

        ts = TestSuite.objects.all()[0]
        top_level_cat = Category.objects.get(parent_category = None)
        epub_cat = Category.objects.get(parent_category = top_level_cat)
        nav_cats = Category.objects.filter(parent_category = epub_cat)
        nav_subcats = Category.objects.filter(parent_category = nav_cats[0])

        self.assertEqual(tests.count(), 3)
        self.assertEqual(tests[0].name, "Test 001")
        self.assertEqual(tests[0].testid, "test-001")
        self.assertEqual(tests[0].parent_category, nav_cats[0])
        self.assertEqual(tests[0].required, True)
        self.assertEqual(tests[0].testsuite, ts)
        self.assertEqual(tests[0].description, "Tests things.")
        self.assertEqual(tests[0].xhtml, 
            """<section xmlns="http://www.w3.org/1999/xhtml" id="test-001" class="ctest"><h3><span class="nature">[REQUIRED]</span><span class="test-id">test-001</span> EPUB Test 001</h3><p class="desc">Tests things.</p></section>""")
        self.assertEqual(tests[0].flagged_as_new, False)
        self.assertEqual(tests[0].flagged_as_changed, False)
        self.assertEqual(tests[0].depth, 3) # category > epub > toc heading > test
        self.assertEqual(tests[0].source, 'epub')

        self.assertEqual(tests[1].name, "Test 002")
        self.assertEqual(tests[1].testid, "test-002")
        self.assertEqual(tests[1].parent_category, nav_subcats[0])
        self.assertEqual(tests[1].required, True)
        self.assertEqual(tests[1].testsuite, ts)
        self.assertEqual(tests[1].description, "Tests whether required tests are supported.")
        self.assertEqual(tests[1].xhtml, 
            """<section xmlns="http://www.w3.org/1999/xhtml" id="test-002" class="ctest"><h4><span class="nature">[REQUIRED]</span><span class="test-id">test-002</span> EPUB Test 002</h4><p class="desc">Tests whether required tests are supported.</p></section>""")
        self.assertEqual(tests[1].flagged_as_new, False)
        self.assertEqual(tests[1].flagged_as_changed, False)
        self.assertEqual(tests[1].depth, 4) # category > epub > toc heading > toc heading 2 > test
        self.assertEqual(tests[1].source, 'epub')

        self.assertEqual(tests[2].name, "Test 003")
        self.assertEqual(tests[2].testid, "test-003")
        self.assertEqual(tests[2].parent_category, nav_subcats[0])
        self.assertEqual(tests[2].required, False)
        self.assertEqual(tests[2].testsuite, ts)
        self.assertEqual(tests[2].description, "Tests whether optional tests are supported.")
        self.assertEqual(tests[2].xhtml, 
            """<section xmlns="http://www.w3.org/1999/xhtml" id="test-003" class="otest"><h4><span class="nature">[OPTIONAL]</span><span class="test-id">test-003</span> EPUB Test 003</h4><p class="desc">Tests whether optional tests are supported.</p></section>""")
        self.assertEqual(tests[2].flagged_as_new, False)
        self.assertEqual(tests[2].flagged_as_changed, False)
        self.assertEqual(tests[2].depth, 4) # category > epub > toc heading > toc heading 2 > test
        self.assertEqual(tests[2].source, 'epub')

        

class AddUserAndRS(TestCase):
    def setUp(self):
        add_ts_v1()
        add_user()
        rs = add_rs()
        add_result_set(rs)
        
    def test_add_data(self):
        """Test that a user and rs were added """
        users = UserProfile.objects.all()
        self.assertEqual(users[0].username, "testuser")
        self.assertEqual(users[0].email, "test@example.com")
        self.assertEqual(users[0].first_name, "FirstName")
        self.assertEqual(users[0].last_name, "LastName")

        rses = ReadingSystem.objects.all()
        self.assertEqual(rses[0].name, "Reader")
        self.assertEqual(rses[0].locale, "US")
        self.assertEqual(rses[0].operating_system, "OSX")
        self.assertEqual(rses[0].notes, "NOTES")
        self.assertEqual(rses[0].version, "2.0")
        self.assertEqual(rses[0].user, users[0])

    def test_empty_evaluation(self):
        "Test the empty evaluation object and its scores"
        rses = ReadingSystem.objects.all()
        result_set = rses[0].get_default_result_set()
        self.assertNotEqual(result_set, None)
        self.assertEqual(result_set.percent_complete, 0.0)

        results = result_set.get_results()
        self.assertEqual(results.count(), 3)

        # each test should have a result
        tests = Test.objects.filter(testsuite = result_set.testsuite)
        for t in tests:
            self.assertIn(t, [x.test for x in results])

        top_level_cat = Category.objects.get(parent_category = None)
        epub_cat = Category.objects.get(parent_category = top_level_cat)
        nav_cats = Category.objects.filter(parent_category = epub_cat)
        nav_subcats = Category.objects.filter(parent_category = nav_cats[0])

        total_score = result_set.get_total_score()
        self.assertEqual(total_score.num_required_tests, 2)
        self.assertEqual(total_score.num_optional_tests, 1)
        self.assertEqual(total_score.num_required_passed, 0)
        self.assertEqual(total_score.num_optional_passed, 0)
        self.assertEqual(total_score.pct_required_passed, 0.0)
        self.assertEqual(total_score.pct_optional_passed, 0.0)
        self.assertEqual(total_score.pct_total_passed, 0.0)

        # basically the same as above
        top_level_cat_score = result_set.get_category_score(top_level_cat)
        self.assertEqual(top_level_cat_score.num_required_tests, 2)
        self.assertEqual(top_level_cat_score.num_optional_tests, 1)
        self.assertEqual(top_level_cat_score.num_required_passed, 0)
        self.assertEqual(top_level_cat_score.num_optional_passed, 0)
        self.assertEqual(top_level_cat_score.pct_required_passed, 0.0)
        self.assertEqual(top_level_cat_score.pct_optional_passed, 0.0)
        self.assertEqual(top_level_cat_score.pct_total_passed, 0.0)

        # so is this one
        epub_cat_score = result_set.get_category_score(epub_cat)
        self.assertEqual(epub_cat_score.num_required_tests, 2)
        self.assertEqual(epub_cat_score.num_optional_tests, 1)
        self.assertEqual(epub_cat_score.num_required_passed, 0)
        self.assertEqual(epub_cat_score.num_optional_passed, 0)
        self.assertEqual(epub_cat_score.pct_required_passed, 0.0)
        self.assertEqual(epub_cat_score.pct_optional_passed, 0.0)
        self.assertEqual(epub_cat_score.pct_total_passed, 0.0)        

        # and actually, so is this one
        nav_cat_score = result_set.get_category_score(nav_cats[0])
        self.assertEqual(nav_cat_score.num_required_tests, 2)
        self.assertEqual(nav_cat_score.num_optional_tests, 1)
        self.assertEqual(nav_cat_score.num_required_passed, 0)
        self.assertEqual(nav_cat_score.num_optional_passed, 0)
        self.assertEqual(nav_cat_score.pct_required_passed, 0.0)
        self.assertEqual(nav_cat_score.pct_optional_passed, 0.0)
        self.assertEqual(nav_cat_score.pct_total_passed, 0.0)        

        # but this one is slightly different (!)
        nav_subcat_score = result_set.get_category_score(nav_subcats[0])
        self.assertEqual(nav_subcat_score.num_required_tests, 1)
        self.assertEqual(nav_subcat_score.num_optional_tests, 1)
        self.assertEqual(nav_subcat_score.num_required_passed, 0)
        self.assertEqual(nav_subcat_score.num_optional_passed, 0)
        self.assertEqual(nav_subcat_score.pct_required_passed, 0.0)
        self.assertEqual(nav_subcat_score.pct_optional_passed, 0.0)
        self.assertEqual(nav_subcat_score.pct_total_passed, 0.0)        


class CompleteEvaluation(TestCase):

    def setUp(self):
        add_ts_v1()
        add_user()
        rs = add_rs()
        rset = add_result_set(rs)
        fill_out_evaluation(rset)

    def test_evaluation(self):
        """Test the migrated evaluation object and its scores"""
        rses = ReadingSystem.objects.all()
        result_set = rses[0].get_default_result_set()
        self.assertEqual(result_set.percent_complete, 100.0)

        top_level_cat = Category.objects.get(parent_category = None)
        epub_cat = Category.objects.get(parent_category = top_level_cat)
        nav_cats = Category.objects.filter(parent_category = epub_cat)
        nav_subcats = Category.objects.filter(parent_category = nav_cats[0])
        total_score = result_set.get_total_score()
        
        self.assertEqual(total_score.num_required_tests, 2)
        self.assertEqual(total_score.num_optional_tests, 1)
        self.assertEqual(total_score.num_required_passed, 1)
        self.assertEqual(total_score.num_optional_passed, 1)
        self.assertEqual(total_score.pct_required_passed, 50.0)
        self.assertEqual(total_score.pct_optional_passed, 100.0)
        # it's weird that this requires conversion; suspect that the other numbers are stored incidentally as ints because
        # there's no digit after the decimal point
        self.assertEqual(total_score.pct_total_passed, Decimal('66.7'))

        # basically the same as above
        top_level_cat_score = result_set.get_category_score(top_level_cat)
        self.assertEqual(top_level_cat_score.num_required_tests, 2)
        self.assertEqual(top_level_cat_score.num_optional_tests, 1)
        self.assertEqual(top_level_cat_score.num_required_passed, 1)
        self.assertEqual(top_level_cat_score.num_optional_passed, 1)
        self.assertEqual(top_level_cat_score.pct_required_passed, 50.0)
        self.assertEqual(top_level_cat_score.pct_optional_passed, 100.0)
        self.assertEqual(top_level_cat_score.pct_total_passed, Decimal('66.7'))

        # so is this one
        epub_cat_score = result_set.get_category_score(epub_cat)
        print epub_cat_score.pct_total_passed
        print epub_cat_score.pct_required_passed     
        self.assertEqual(epub_cat_score.num_required_tests, 2)
        self.assertEqual(epub_cat_score.num_optional_tests, 1)
        self.assertEqual(epub_cat_score.num_required_passed, 1)
        self.assertEqual(epub_cat_score.num_optional_passed, 1)
        self.assertEqual(epub_cat_score.pct_required_passed, 50.0)
        self.assertEqual(epub_cat_score.pct_optional_passed, 100.0)
        self.assertEqual(epub_cat_score.pct_total_passed, Decimal('66.7'))   
        

        # and actually, so is this one
        nav_cat_score = result_set.get_category_score(nav_cats[0])
        self.assertEqual(nav_cat_score.num_required_tests, 2)
        self.assertEqual(nav_cat_score.num_optional_tests, 1)
        self.assertEqual(nav_cat_score.num_required_passed, 1)
        self.assertEqual(nav_cat_score.num_optional_passed, 1)
        self.assertEqual(nav_cat_score.pct_required_passed, 50.0)
        self.assertEqual(nav_cat_score.pct_optional_passed, 100.0)
        self.assertEqual(nav_cat_score.pct_total_passed, Decimal('66.7'))        

        # but this one is slightly different (!)
        nav_subcat_score = result_set.get_category_score(nav_subcats[0])
        self.assertEqual(nav_subcat_score.num_required_tests, 1)
        self.assertEqual(nav_subcat_score.num_optional_tests, 1)
        self.assertEqual(nav_subcat_score.num_required_passed, 0)
        self.assertEqual(nav_subcat_score.num_optional_passed, 1)
        self.assertEqual(nav_subcat_score.pct_required_passed, 0.0)
        self.assertEqual(nav_subcat_score.pct_optional_passed, 100.0)
        self.assertEqual(nav_subcat_score.pct_total_passed, 50.0)  

    def test_metadata(self):
        rses = ReadingSystem.objects.all()
        result_set = rses[0].get_default_result_set()
        metadata = result_set.get_metadata()
        self.assertNotEqual(metadata, None)
        self.assertEqual(metadata.assistive_technology, "assistive_technology")
        self.assertEqual(metadata.input_type, common.INPUT_TYPE_KEYBOARD)
        self.assertEqual(metadata.supports_screenreader, False)
        self.assertEqual(metadata.supports_braille, False)

class UpgradeTestSuite(TestCase):
    def setUp(self):
        add_ts_v1()
        add_user()
        rs = add_rs()
        rset = add_result_set(rs)
        fill_out_evaluation(rset)
        add_ts_v2()

    def test_number_of_testsuites(self):
        "Test that there are two testsuites"
        self.assertEqual(TestSuite.objects.all().count(), 2)

    def test_testsuite_version(self):
        "Test that the testsuite version is correct"
        ts = TestSuite.objects.get_most_recent_testsuite()
        self.assertEqual(ts.version_date, datetime.today().date())
        self.assertEqual(ts.version_revision, 2)

    def test_number_of_objects(self):
        "Test that there are 3 tests and 4 categories"
        ts = TestSuite.objects.get_most_recent_testsuite()
        self.assertEqual(Test.objects.filter(testsuite = ts).count(), 3)
        self.assertEqual(Category.objects.filter(testsuite = ts).count(), 4)

        rses = ReadingSystem.objects.all()
        results = rses[0].get_default_result_set().get_results()
        self.assertEqual(results.count(), 3)


    def test_evaluation(self):
        """Test the migrated evaluation object and its scores"""
        rses = ReadingSystem.objects.all()
        result_set = rses[0].get_default_result_set()
        ts = result_set.testsuite
        results = result_set.get_results()

        #one test stayed the same, one changed, and one is new
        self.assertEqual(result_set.percent_complete, Decimal('33.33'))

        # test-001 did not change and should have a result
        r001 = result_set.get_result_for_test_by_id("test-001")
        self.assertEqual(r001.result, common.RESULT_SUPPORTED)
        self.assertEqual(r001.test.flagged_as_changed, False)
        self.assertEqual(r001.test.flagged_as_new, False)
        self.assertEqual(r001.notes, "Test note")

        # test-002 changed and has no result
        r002 = result_set.get_result_for_test_by_id("test-002")
        self.assertEqual(r002.result, None)
        self.assertEqual(r002.test.flagged_as_changed, True)
        self.assertEqual(r002.test.flagged_as_new, False)

        # test-002a is new and has no result
        r002a = result_set.get_result_for_test_by_id("test-002a")
        self.assertEqual(r002a.result, None)
        self.assertEqual(r002a.test.flagged_as_changed, False)
        self.assertEqual(r002a.test.flagged_as_new, True)

        # the result_set is flagged
        self.assertEqual(result_set.flagged_for_review, True)

        top_level_cat = Category.objects.get(parent_category = None, testsuite = ts)
        epub_cat = Category.objects.get(parent_category = top_level_cat)
        nav_cats = Category.objects.filter(parent_category = epub_cat)
        nav_subcats = Category.objects.filter(parent_category = nav_cats[0])
        total_score = result_set.get_total_score()
        
        self.assertEqual(total_score.num_required_tests, 3)
        self.assertEqual(total_score.num_optional_tests, 0)
        self.assertEqual(total_score.num_required_passed, 1)
        self.assertEqual(total_score.num_optional_passed, 0)
        self.assertEqual(total_score.pct_required_passed, Decimal('33.3'))
        self.assertEqual(total_score.pct_optional_passed, 0.0)
        self.assertEqual(total_score.pct_total_passed, Decimal('33.3'))

        # basically the same as above
        top_level_cat_score = result_set.get_category_score(top_level_cat)
        self.assertEqual(top_level_cat_score.num_required_tests, 3)
        self.assertEqual(top_level_cat_score.num_optional_tests, 0)
        self.assertEqual(top_level_cat_score.num_required_passed, 1)
        self.assertEqual(top_level_cat_score.num_optional_passed, 0)
        self.assertEqual(top_level_cat_score.pct_required_passed, Decimal('33.3'))
        self.assertEqual(top_level_cat_score.pct_optional_passed, 0.0)
        self.assertEqual(top_level_cat_score.pct_total_passed, Decimal('33.3'))

        # so is this one
        epub_cat_score = result_set.get_category_score(epub_cat)
        self.assertEqual(epub_cat_score.num_required_tests, 3)
        self.assertEqual(epub_cat_score.num_optional_tests, 0)
        self.assertEqual(epub_cat_score.num_required_passed, 1)
        self.assertEqual(epub_cat_score.num_optional_passed, 0)
        self.assertEqual(epub_cat_score.pct_required_passed, Decimal('33.3'))
        self.assertEqual(epub_cat_score.pct_optional_passed, 0.0)
        self.assertEqual(epub_cat_score.pct_total_passed, Decimal('33.3'))   
        

        # and actually, so is this one
        nav_cat_score = result_set.get_category_score(nav_cats[0])
        self.assertEqual(nav_cat_score.num_required_tests, 3)
        self.assertEqual(nav_cat_score.num_optional_tests, 0)
        self.assertEqual(nav_cat_score.num_required_passed, 1)
        self.assertEqual(nav_cat_score.num_optional_passed, 0)
        self.assertEqual(nav_cat_score.pct_required_passed, Decimal('33.3'))
        self.assertEqual(nav_cat_score.pct_optional_passed, 0.0)
        self.assertEqual(nav_cat_score.pct_total_passed, Decimal('33.3'))        

        # but this one is slightly different (!)
        nav_subcat_score = result_set.get_category_score(nav_subcats[0])
        self.assertEqual(nav_subcat_score.num_required_tests, 2)
        self.assertEqual(nav_subcat_score.num_optional_tests, 0)
        self.assertEqual(nav_subcat_score.num_required_passed, 0)
        self.assertEqual(nav_subcat_score.num_optional_passed, 0)
        self.assertEqual(nav_subcat_score.pct_required_passed, 0.0)
        self.assertEqual(nav_subcat_score.pct_optional_passed, 0.0)
        self.assertEqual(nav_subcat_score.pct_total_passed, 0.0)  

