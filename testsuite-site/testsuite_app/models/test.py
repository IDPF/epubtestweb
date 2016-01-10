from django.db import models
from . import common

class TestManager(models.Manager):
    def already_exists(self, testid):
        tests_with_same_id = Test.objects.filter(test_id = testid)
        return tests_with_same_id.count() != 0

class Test(models.Model):
    objects = TestManager()

    name = models.CharField(max_length = common.LONG_STRING)
    description = models.TextField()
    category = models.ForeignKey('Category', blank = True, null = True)
    required = models.BooleanField()
    test_id = models.CharField(max_length = common.SHORT_STRING)
    testsuite = models.ForeignKey('TestSuite')
    xhtml =  models.TextField()
    epub = models.ForeignKey('Epub')
    feature = models.ForeignKey('Feature', blank = True, null = True)
    order_in_book = models.IntegerField()
