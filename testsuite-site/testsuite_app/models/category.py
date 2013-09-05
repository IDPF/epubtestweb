from django.db import models
from testsuite import *
from common import *
from test import *

class Category(models.Model, ItemMixin):
    class Meta:
        db_table = 'testsuite_app_category'
        app_label= 'testsuite_app'

    category_type = models.CharField(max_length = 1, choices = CATEGORY_TYPE)
    name = models.TextField()
    # Declare dependencies with string value instead of classname as workaround
    parent_category = models.ForeignKey('Category', null = True, blank = True)
    testsuite = models.ForeignKey(TestSuite)

    # get all the tests in the given category (drill down through subcategories too)
    def get_tests(self):
        tests = Test.objects.filter(parent_category = self)
        retval = []
        for t in tests:
            retval.append(t)
        subcats = self.objects.filter(parent_category = self)
        for cat in subcats:
            retval.extend(get_tests(cat))
        return retval
