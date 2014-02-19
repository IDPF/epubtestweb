from django.db import models
import common

class TestManager(models.Manager):
    def already_exists(self, testid):
        from test import Test
        tests_with_same_id = Test.objects.filter(testid = testid)
        return tests_with_same_id.count() != 0

class Test(models.Model, common.ItemMixin):
    class Meta:
        db_table = 'testsuite_app_test'
        app_label= 'testsuite_app'

    objects = TestManager()

    name = models.CharField(max_length = common.LONG_STRING)
    description = models.TextField()
    parent_category = models.ForeignKey('Category')
    required = models.BooleanField()
    testid = models.CharField(max_length = common.SHORT_STRING)
    testsuite = models.ForeignKey('TestSuite')
    xhtml =  models.TextField()
    flagged_as_new = models.BooleanField(default = False)
    flagged_as_changed = models.BooleanField(default = False)
    source = models.CharField(max_length = common.LONG_STRING, null=True, blank=True) # what epub the test or category came from
    depth = models.IntegerField(null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        "custom save routine"
        # call 'save' on the base class
        self.depth = self.calculate_depth()
        super(Test, self).save(*args, **kwargs)

    def get_epub_parent_category(self):
    	parents = self.get_parents()
    	for p in parents:
    		if p.category_type == common.CATEGORY_EPUB: 
    			return p
    	return None

    def get_top_level_parent_category(self):
        p = self.parent_category
        while p.parent_category != None:
            p = p.parent_category
        return p
    