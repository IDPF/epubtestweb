from django.db import models
import common

class TestManager(models.Manager):
    def already_exists(self, testid):
        from test import Test
        tests_with_same_id = Test.objects.filter(testid = testid)
        return tests_with_same_id.count() != 0

class Test(models.Model, common.ItemMixin):
    objects = TestManager()

    name = models.CharField(max_length = common.LONG_STRING)
    description = models.TextField()
    category = models.ForeignKey('Category')
    required = models.BooleanField()
    testid = models.CharField(max_length = common.SHORT_STRING)
    testsuite = models.ForeignKey('TestSuite')
    xhtml =  models.TextField()
    epub = models.ForeignKey('Epub')
    allow_na = models.BooleanField(default = False) # allow "Not applicable" as an answer to this test
    order_in_book = models.IntegerField()

    
    
class TestMetadata(models.Model):
    "Annotate test objects with accessibility metadata"
    test = models.ForeignKey('Test')
    is_advanced = models.BooleanField(default=False)
