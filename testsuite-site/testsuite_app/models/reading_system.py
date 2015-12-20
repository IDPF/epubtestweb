from django.db import models
from . import common

class ReadingSystem(models.Model):
    name = models.CharField(max_length = common.LONG_STRING, blank = False, null = False)
    version = models.CharField(max_length = common.SHORT_STRING, blank = False, null = False)
    operating_system = models.CharField(max_length = common.SHORT_STRING, blank = False, null = False)
    operating_system_version = models.CharField(max_length = common.SHORT_STRING, blank = True, null = True)
    user = models.ForeignKey('UserProfile')
    notes = models.CharField(max_length = common.SHORT_STRING, null = True, blank = True)

    # by default, get only the current and public evaluations
    def get_evaluations(self, testsuite, is_archived = False, is_published = True):
        from .evaluation import Evaluation
        evaluations = Evaluation.objects.filter(
            reading_system = self, 
            testsuite = testsuite, 
            is_archived = is_archived,
            is_published = is_published)
        return evaluations

    # get all evaluations regardless of whether they are archived/published
    def get_all_evaluations(self, testsuite):
        from .evaluation import Evaluation
        evaluations = Evaluation.objects.filter(
            reading_system = self, 
            testsuite = testsuite)
        return evaluations

    def delete_associated(self):
        from .evaluation import Evaluation
        evaluations = Evaluation.objects.filter(reading_system = self)
        for evaluation in evaluations:
            evaluation.delete_associated()
            evaluation.delete()


