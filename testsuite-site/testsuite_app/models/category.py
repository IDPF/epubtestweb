from django.db import models
from test import Test
import common

class Category(models.Model, common.ItemMixin):
    class Meta:
        db_table = 'testsuite_app_category'
        app_label= 'testsuite_app'

    category_type = models.CharField(max_length = 1, choices = common.CATEGORY_TYPE)
    name = models.TextField()
    parent_category = models.ForeignKey('Category', null = True, blank = True)
    testsuite = models.ForeignKey('TestSuite')
    source = models.CharField(max_length = common.LONG_STRING, null=True, blank=True) # what epub the test or category came from
    depth = models.IntegerField(null=True, blank=True, default=0)
    # desc is for an extended category description; e.g. an epub file will use name for the title and desc for the description
    desc = models.TextField(null = True, blank = True)    

    def save(self, *args, **kwargs):
        "custom save routine"
        # call 'save' on the base class
        self.depth = self.calculate_depth()
        super(Category, self).save(*args, **kwargs)

    def get_tests(self):
        # get all the tests in the given category (drill down through subcategories too)
        tests = Test.objects.filter(parent_category = self)
        retval = []
        for t in tests:
            retval.append(t)
        subcats = Category.objects.filter(parent_category = self)
        for cat in subcats:
            retval.extend(cat.get_tests())
        return retval

