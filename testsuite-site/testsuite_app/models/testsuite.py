from django.db import models
from common import *
from category import *

class TestSuite(models.Model):
    class Meta:
        db_table = 'testsuite_app_testsuite'
        app_label = 'testsuite_app'

    # version = version_date-version_revision (2013-01-01-5)
    version_date = models.DateField(max_length = SHORT_STRING)
    version_revision = models.IntegerField()

    def get_top_level_categories(self):
        return Category.objects.filter(testsuite = self, parent_category = None)

