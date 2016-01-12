from django.db import models
from . import common

class Epub (models.Model):
    epubid = models.TextField()
    description = models.TextField()
    title = models.TextField()
    testsuite = models.ForeignKey('TestSuite')
    filename = models.CharField(max_length = common.LONG_STRING, blank = False, null = False)

