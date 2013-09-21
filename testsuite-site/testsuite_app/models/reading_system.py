from django.db import models
from common import *

# note: from evaluation import Evaluation was not working here

class ReadingSystem(models.Model):
    class Meta:
        db_table = 'testsuite_app_readingsystem'
        app_label= 'testsuite_app'


    locale = models.CharField(max_length = SHORT_STRING, null = True, blank = True)
    evaluation = models.OneToOneField('Evaluation')
    name = models.CharField(max_length = LONG_STRING, blank = False, null = False)
    operating_system = models.CharField(max_length = SHORT_STRING, null = True, blank = True)
    sdk_version = models.CharField(max_length = SHORT_STRING, null = True, blank = True)
    version = models.CharField(max_length = SHORT_STRING, blank = False, null = False)

    def create_new_evaluation(self, testsuite, evaluation_type, user):
        "Create and return a new evaluation, along with an initialized set of result objects."
        from evaluation import Evaluation
        from test import Test
        from score import Score
        from result import Result
        from testsuite_app.helper_functions import generate_timestamp
        from category import Category
        tests = Test.objects.filter(testsuite = testsuite)
        # is this check necessary?
        if len(tests) == 0:
            return None

        evaluation = Evaluation(
            evaluation_type = evaluation_type,
            reading_system = self,
            user = user,
            testsuite = testsuite,
            timestamp = generate_timestamp(),
            percent_complete = 0
        )
        evaluation.save()

        # create results for this evaluation
        for t in tests:
            result = Result(test = t, evaluation = evaluation, result = None) # 4 = no value yet
            result.save()

        # create category score entries for this evaluation
        categories = Category.objects.filter(testsuite = evaluation.testsuite)
        for cat in categories:
            score = Score(
                category = cat,
                percent_passed = 0,
                evaluation = evaluation
            )
            score.save()

        return evaluation



