from django.db import models
import common

class ReadingSystemFamily(models.Model):
    name = models.CharField(max_length = common.LONG_STRING, blank = False, null = False)

    

class ReadingSystem(models.Model):
    
    name = models.CharField(max_length = common.LONG_STRING, blank = False, null = False)
    operating_system = models.CharField(max_length = common.SHORT_STRING, blank = False, null = False)
    notes = models.CharField(max_length = common.SHORT_STRING, null = True, blank = True)
    version = models.CharField(max_length = common.SHORT_STRING, blank = False, null = False)
    visibility = models.CharField(max_length = 1, choices = common.VISIBILITY_TYPE, default=common.VISIBILITY_MEMBERS_ONLY)
    user = models.ForeignKey('UserProfile')
    status = models.CharField(max_length = 1, choices = common.READING_SYSTEM_STATUS_TYPE, default=common.READING_SYSTEM_STATUS_TYPE_CURRENT)

    def get_default_result_set(self):
        # there should only be one
        from testsuite import TestSuite
        testsuite = TestSuite.objects.get_most_recent_testsuite()
        result_sets = self.get_result_sets_for_testsuite(testsuite)
        if result_sets.count() > 0:
            return result_sets[0]
        else:
            return None

    def get_accessibility_result_sets(self):
        from evaluation import Evaluation
        from testsuite import TestSuite
        testsuite = TestSuite.objects.get_most_recent_accessibility_testsuite()
        result_sets = self.get_result_sets_for_testsuite(testsuite)
        return result_sets

    def get_result_sets_for_testsuite(self, testsuite):
        from evaluation import Evaluation
        result_sets = Evaluation.objects.get_result_sets_for_testsuite(self, testsuite)
        return result_sets        

    def get_result_set_by_id(self, rset_id):
        from evaluation import Evaluation
        return Evaluation.objects.get_result_set_by_id(rset_id)

    def delete_associated(self):
        result_set = self.get_default_result_set()
        if result_set != None:
            result_set.delete_associated()
            result_set.delete()
        accessibility_result_sets = self.get_accessibility_result_sets()
        for ars in accessibility_result_sets:
            if ars != None:
                ars.delete_associated()
                ars.delete()

    def set_visibility(self, visibility):
        self.visibility = visibility
        rset = self.get_default_result_set()
        if rset != None:
            rset.visibility = visibility
    

