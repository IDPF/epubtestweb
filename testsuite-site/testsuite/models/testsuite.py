from django.db import models
import common

class TestSuiteManager(models.Manager):
    def get_most_recent_testsuite(self, testsuite_type):
        recent = TestSuite.objects.filter(testsuite_type = testsuite_type).order_by("-version_date", "-version_revision")
        if recent.count() == 0:
            return None
        return r[0]

class TestSuite(models.Model):
    objects = TestSuiteManager()

    # version is formatted as date-revision; e.g. 2013-01-01-5
    version_date = models.DateField(max_length = common.SHORT_STRING)
    version_revision = models.IntegerField()
    testsuite_type = models.CharField(max_length = 1, choices = common.TESTSUITE_TYPE, default=common.TESTSUITE_TYPE_DEFAULT)
    allow = models.CharField(max_length = 1, choices = common.TESTSUITE_ALLOW, default=common.TESTSUITE_ALLOW_ONE)
    name = models.CharField(max_length = common.SHORT_STRING)

    def get_categories(self):
        from category import Category
        return Category.objects.filter(testsuite = self)

    def get_features(self):
        from feature import Feature
        return Feature.objects.filter(testsuite = self)
    
    def get_tests(self):
        "get a queryset of all tests"
        from test import Test
        tests = Test.objects.filter(testsuite = self)
        return tests

    def get_test_by_id(self, testid):
        from test import Test
        try:
            return Test.objects.get(testid = testid, testsuite = self)
        except Test.DoesNotExist:
            return None

    def get_category_by_id(self, categoryid):
        from category import Category
        return Category.objects.get(testsuite = self, categoryid = categoryid)


