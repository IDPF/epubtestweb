from django.db import models
from common import SHORT_STRING, LONG_STRING

class ReadingSystem(models.Model):
    class Meta:
        db_table = 'testsuite_app_readingsystem'
        app_label= 'testsuite_app'

    locale = models.CharField(max_length = SHORT_STRING, null = True, blank = True)
    name = models.CharField(max_length = LONG_STRING, blank = False, null = False)
    operating_system = models.CharField(max_length = SHORT_STRING, blank = False, null = False)
    sdk_version = models.CharField(max_length = SHORT_STRING, null = True, blank = True)
    version = models.CharField(max_length = SHORT_STRING, blank = False, null = False)
    user = models.ForeignKey('UserProfile')

    def save(self, *args, **kwargs):
        "custom save routine"
        from evaluation import Evaluation
        super(ReadingSystem, self).save(*args, **kwargs)
        # create an evaluation if there is none
        if self.get_current_evaluation() == None:
            evaluation = Evaluation.objects.create_evaluation(self)
        

    def get_current_evaluation(self):
        "get the evaluation associated with the most recent testsuite"
        from testsuite import TestSuite
        from evaluation import Evaluation
        most_recent_testsuite = TestSuite.objects.get_most_recent_testsuite()
        try:
            return Evaluation.objects.get(reading_system = self, testsuite = most_recent_testsuite)
        except Evaluation.DoesNotExist:
            return None

    def get_evaluation_for_testsuite(self, testsuite):
        from testsuite import TestSuite
        from evaluation import Evaluation
        try:
            return Evaluation.objects.get(reading_system = self, testsuite = testsuite)
        except Evaluation.DoesNotExist:
            return None

    def get_all_evaluations(self):
        "get all evaluations"
        from evaluation import Evaluation
        return Evaluation.objects.filter(reading_system = self)
