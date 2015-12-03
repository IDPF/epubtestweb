from django.db import models
from . import common

class ReadingSystem(models.Model):
    name = models.CharField(max_length = common.LONG_STRING, blank = False, null = False)
    operating_system = models.CharField(max_length = common.SHORT_STRING, blank = False, null = False)
    user = models.ForeignKey('UserProfile')
    version = models.CharField(max_length = common.SHORT_STRING, blank = False, null = False)
    notes = models.CharField(max_length = common.SHORT_STRING, null = True, blank = True)

    # by default, get only the current and public evaluations
    def get_evaluations(self, testsuite, status=common.EVALUATION_STATUS_TYPE_CURRENT, visibility=common.VISIBILITY_PUBLIC):
        from .evaluation import Evaluation
        evaluations = Evaluation.objects.filter(
            reading_system = self, 
            testsuite = testsuite, 
            status = status, 
            visibility = visibility)
        if testsuite.allow_many_evaluations == False and evaluations.count() > 1:
            print("WARNING TOO MANY EVALS")
        return evaluations

    def delete_associated(self):
        evaluations = Evaluation.objects.filter(reading_system = self)
        for evaluation in evaluations:
            evaluation.delete_associated()
            evaluation.delete()


