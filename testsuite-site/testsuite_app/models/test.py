from django.db import models
from common import LONG_STRING, SHORT_STRING, ItemMixin

class TestManager(models.Manager):
    def already_exists(self, testid):
        from test import Test
        tests_with_same_id = Test.objects.filter(testid = testid)
        return tests_with_same_id.count() != 0

class Test(models.Model, ItemMixin):
    class Meta:
        db_table = 'testsuite_app_test'
        app_label= 'testsuite_app'

    objects = TestManager()

    name = models.CharField(max_length = LONG_STRING)
    description = models.TextField()
    parent_category = models.ForeignKey('Category')
    required = models.BooleanField()
    testid = models.CharField(max_length = SHORT_STRING)
    testsuite = models.ForeignKey('TestSuite')
    xhtml =  models.TextField()
    flagged_as_new = models.BooleanField(default = False)
    flagged_as_changed = models.BooleanField(default = False)
    source = models.CharField(max_length = LONG_STRING, null=True, blank=True) # what epub the test or category came from

    def save(self, *args, **kwargs):
        "custom save routine"
        if Test.objects.already_exists(self.testid) == True:
            print "WARNING! Test with ID {0} already exists. Cannot save.".format(self.testid)
        else:
            # call 'save' on the base class
            super(Test, self).save(*args, **kwargs)

    def get_epub_parent_category(self):
    	parents = self.get_parents()
    	for p in parents:
    		if p.category_type == "2": # 'epub'
    			return p
    	return None