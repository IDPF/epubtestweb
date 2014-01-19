from django.db import models
from common import SHORT_STRING

class TestSuiteManager(models.Manager):
    def get_most_recent_testsuite(self):
        recent = TestSuite.objects.order_by("-version_date", "-version_revision")
        if recent.count() == 0:
            return None
        else:
            return recent[0]

class TestSuite(models.Model):
    class Meta:
        db_table = 'testsuite_app_testsuite'
        app_label = 'testsuite_app'

    objects = TestSuiteManager()

    # version is formatted as date-revision; e.g. 2013-01-01-5
    version_date = models.DateField(max_length = SHORT_STRING)
    version_revision = models.IntegerField()

    def get_top_level_categories(self):
        from category import Category
        return Category.objects.filter(testsuite = self, parent_category = None)

