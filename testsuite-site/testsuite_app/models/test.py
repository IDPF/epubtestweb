from django.db import models
from common import LONG_STRING, SHORT_STRING, ItemMixin

class Test(models.Model, ItemMixin):
    class Meta:
        db_table = 'testsuite_app_test'
        app_label= 'testsuite_app'

    name = models.CharField(max_length = LONG_STRING)
    description = models.TextField()
    parent_category = models.ForeignKey('Category')
    required = models.BooleanField()
    testid = models.CharField(max_length = SHORT_STRING)
    testsuite = models.ForeignKey('TestSuite')
    xhtml =  models.TextField()
