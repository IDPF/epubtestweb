from django.db import models
from test import Test
import common

class Category(models.Model, common.ItemMixin):
    name = models.TextField()
    testsuite = models.ForeignKey('TestSuite')
    
    def get_tests(self):
        return Test.objects.filter(category = self)

    def get_features(self):
        return Feature.objects.filter(category = self)

