from django.db import models

class Feature (models.Model):
    feature_id = models.TextField()
    name = models.TextField()
    category = models.ForeignKey('Category')
    testsuite = models.ForeignKey('TestSuite')

    def get_tests(self):
        from .test import Test
        return Test.objects.filter(feature = self)
