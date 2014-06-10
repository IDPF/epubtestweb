from django.db import models
import common

class ReadingSystem(models.Model):
    class Meta:
        db_table = 'testsuite_app_readingsystem'
        app_label= 'testsuite_app'

    locale = models.CharField(max_length = common.SHORT_STRING, null = True, blank = True)
    name = models.CharField(max_length = common.LONG_STRING, blank = False, null = False)
    operating_system = models.CharField(max_length = common.SHORT_STRING, blank = False, null = False)
    sdk_version = models.CharField(max_length = common.SHORT_STRING, null = True, blank = True)
    version = models.CharField(max_length = common.SHORT_STRING, blank = False, null = False)
    user = models.ForeignKey('UserProfile')
    visibility = models.CharField(max_length = 1, choices = common.VISIBILITY_TYPE, default=common.VISIBILITY_MEMBERS_ONLY)

    def save(self, *args, **kwargs):
        "custom save routine"
        from evaluation import Evaluation, EvaluationManager
        super(ReadingSystem, self).save(*args, **kwargs)
        # create an evaluation if there is none
        if self.get_current_evaluation() == None:
            print "CREATING EVAL"
            evaluation = Evaluation.objects.create_evaluation(self)
        

    def get_default_result_set(self):
        # there should only be one
        from result import ResultSet
        from common import *
        try:
            result_set = ResultSet.objects.get(evaluation = self, testsuite=self.testsuite)
        except ResultSet.DoesNotExist:
            return None
        return result_set

    def get_accessibility_result_sets(self):
        from result import ResultSet
        result_sets = ResultSet.objects.filter(evaluation = self, testsuite = self.accessibility_testsuite)
        return result_sets


    def get_evaluation_for_testsuite(self, testsuite):
        from testsuite import TestSuite
        from evaluation import Evaluation
        try:
            return Evaluation.objects.get(reading_system = self, testsuite = testsuite)
        except Evaluation.DoesNotExist:
            return None

