from django.db import models
from . import common

class Category(models.Model):
    name = models.TextField()
    testsuite = models.ForeignKey('TestSuite')
    category_id = models.CharField(max_length = common.SHORT_STRING)
    def get_tests(self):
        from .test import Test
        return Test.objects.filter(category = self)

    def get_features(self):
        from .feature import Feature
        return Feature.objects.filter(category = self)

