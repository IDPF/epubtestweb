from django.db import models
import common

class TestSuiteManager(models.Manager):
    def get_most_recent_testsuite(self):
        return self.get_most_recent_testsuite_of_type(common.TESTSUITE_TYPE_DEFAULT)

    def get_most_recent_accessibility_testsuite(self):
        return self.get_most_recent_testsuite_of_type(common.TESTSUITE_TYPE_ACCESSIBILITY)

    def get_most_recent_testsuite_of_type(self, testsuite_type):
        recent = TestSuite.objects.order_by("-version_date", "-version_revision")
        if recent.count() == 0:
            return None
        
        # return the first one that matches the testsuite_type
        for r in recent:
            if r.testsuite_type == testsuite_type:
                return r

        return None #this shouldn't happen

class TestSuite(models.Model):
    class Meta:
        db_table = 'testsuite_app_testsuite'
        app_label = 'testsuite_app'

    objects = TestSuiteManager()

    # version is formatted as date-revision; e.g. 2013-01-01-5
    version_date = models.DateField(max_length = common.SHORT_STRING)
    version_revision = models.IntegerField()
    testsuite_type = models.CharField(max_length = 1, choices = common.TESTSUITE_TYPE, default=common.TESTSUITE_TYPE_DEFAULT)

    def get_top_level_categories(self):
        from category import Category
        return Category.objects.filter(testsuite = self, parent_category = None)

    def get_categories(self):
        from category import Category
        return Category.objects.filter(testsuite = self)
    
    def get_tests(self):
        "get a queryset of all tests"
        from test import Test
        tests = Test.objects.filter(testsuite = self)
        return tests


