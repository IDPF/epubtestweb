from django.test import TestCase
from testsuite_app.models import Category, Evaluation, ReadingSystem, Result, Score, Test, TestSuite, UserProfile
from testsuite_app.models.evaluation import generate_timestamp
from import_testsuite_data import main
import os
from testsuite_app.models import common

def get_testsuite_v1_path():
    path = os.path.abspath(__file__)
    return os.path.join(path, "../../test_data/testsuite_v1")

def get_testsuite_v1_path():
    path = os.path.abspath(__file__)
    return os.path.join(path, "../../test_data/testsuite_v2")

def get_config_path():
    path = os.path.abspath(__file__)
    return os.path.join(path, "../../test_data/categories.yaml")


class ImportTestSuite(TestCase):
    def setUp(self):
        path = get_testsuite_v1_path()
        config_path = get_config_path()
        main.add_testsuite(path, config_path)

    def test_number_of_testsuites(self):
        "Test that there is one testsuite"
        self.assertEqual(TestSuite.objects.all().count(), 1)

    def test_correct_date(self):
        "Test that the testsuite date is correct"
        # the date is correct
        todays_date = datetime.today()
        version_date = "{0}-{1}-{2}".format(str(todays_date.year), str(todays_date.month).zfill(2), str(todays_date.day).zfill(2))
        self.assertEqual(TestSuite.objects.all()[0].version_date, version_date)

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
        self.assertEqual(epub_cat.source, get_testsuite_v1_path())

        # nav.xhtml categories
        nav_cats = Category.objects.filter(parent_category = epub_cat)
        self.assertEqual(nav_cats.count(), 2)
        self.assertEqual(nav_cats[0].parent_category, epub_cat)
        self.assertEqual(nav_cats[1].parent_category, nav_cats[0])
        self.assertEqual(nav_cats[0].name, "Test Category")
        self.assertEqual(nav_cats[0].category_type, common.CATEGORY_INTERNAL)
        self.assertEqual(nav_cats[0].testsuite, ts)
        self.assertEqual(nav_cats[0].source, get_testsuite_v1_path())
        self.assertEqual(nav_cats[1].name, "Test Sub-Category")
        self.assertEqual(nav_cats[1].category_type, common.CATEGORY_INTERNAL)
        self.assertEqual(nav_cats[1].testsuite, ts)
        self.assertEqual(nav_cats[1].source, get_testsuite_v1_path())
        

class AddSampleData(TestCase):
    def setUp(self):
        path = get_testsuite_v1_path()
        config_path = get_config_path()
        main.add_testsuite(path, config_path)
        main.add_user("testuser", "test@example.com", "password", "FirstName", "LastName")
        main.add_rs("Reader")


    def test_add_user(self):
        """Test that a user can be added """
        pass


    def test_add_reading_system(self):
        """Test that a reading system can be added """
        pass

    


class UpgradeTestSuite(TestCase):
    def setUp(self):
        pass

    def test_upgrade_evaluation(self):
        "Test that the evaluation was upgraded and flagged"
        pass

