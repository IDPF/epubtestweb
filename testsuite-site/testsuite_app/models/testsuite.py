from django.db import models
from . import common

class TestSuiteManager(models.Manager):
    def get_testsuite(self, testsuite_type):
        try:
            testsuite = TestSuite.objects.get(testsuite_type = testsuite_type)
        except TestSuite.DoesNotExist:
            return None
        return testsuite

    def get_testsuites(self):
        # returns all types
        testsuites = []
        for testsuite_type in common.TESTSUITE_TYPE:
            testsuite = self.get_testsuite(testsuite_type[0])
            if testsuite != None:
                testsuites.append(testsuite)
        return testsuites

class TestSuite(models.Model):
    objects = TestSuiteManager()

    version_date = models.DateTimeField(max_length = common.SHORT_STRING)
    testsuite_type = models.CharField(max_length = 1, choices = common.TESTSUITE_TYPE, default=common.TESTSUITE_TYPE_DEFAULT)
    allow_many_evaluations = models.BooleanField(default = False)
    name = models.CharField(max_length = common.SHORT_STRING)
    testsuite_id = models.CharField(max_length = common.SHORT_STRING)

    def get_categories(self):
        from .category import Category
        return Category.objects.filter(testsuite = self)

    def get_features(self):
        from .feature import Feature
        return Feature.objects.filter(testsuite = self)
    
    def get_tests(self):
        "get a queryset of all tests"
        from .test import Test
        tests = Test.objects.filter(testsuite = self)
        return tests

    def get_test_by_id(self, testid):
        from .test import Test
        try:
            return Test.objects.get(test_id = testid, testsuite = self)
        except Test.DoesNotExist:
            return None

    def get_category_by_id(self, categoryid):
        from .category import Category
        return Category.objects.get(testsuite = self, category_id = categoryid)

    def get_epubs(self):
        from .epub import Epub
        return Epub.objects.filter(testsuite = self)

    

    

