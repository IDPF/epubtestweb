from django.db import models
from common import *
from evaluation import *


class ReadingSystem(models.Model):
    class Meta:
        db_table = 'testsuite_app_readingsystem'
        app_label= 'testsuite_app'


    locale = models.CharField(max_length = SHORT_STRING, null = True, blank = True)
    name = models.CharField(max_length = LONG_STRING, blank = False, null = False)
    operating_system = models.CharField(max_length = SHORT_STRING, null = True, blank = True)
    sdk_version = models.CharField(max_length = SHORT_STRING, null = True, blank = True)
    version = models.CharField(max_length = SHORT_STRING, blank = False, null = False)

    def create_new_evaluation(self, testsuite, evaluation_type, user):
        "Create and return a new evaluation, along with an initialized set of result objects."

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


    def get_most_recent_evaluation(self):
        "Get the most recent public complete evaluation"
        evaluations = Evaluation.objects.filter(reading_system = self, evaluation_type = "2").order_by("-timestamp")
        for e in evaluations:
            if e.is_evaluation_complete():
                return e
        return None

    def get_complete_evaluations(self):
        "Return all complete evaluations, most recent first."
        evals = Evaluation.objects.filter(reading_system = self).order_by("-timestamp")
        retval = []
        for e in evals:
            if e.is_evaluation_complete() == True:
                retval.append(e)
        return retval

    def get_incomplete_evaluations(self):
        "Return all incomplete evaluations for the given reading system, most recent first."
        evals = Evaluation.objects.filter(reading_system = self).order_by("-timestamp")
        retval = []
        for e in evals:
            if e.is_evaluation_complete() == False:
                retval.append(e)
        return retval

    def get_public_evaluations(self):
        "Return all public evaluations for the given reading system, most recent first."
        evals = Evaluation.objects.filter(reading_system = self, evaluation_type = "2").order_by("-timestamp")
        retval = []
        for e in evals:
           retval.append(e)
        return retval

    def get_internal_evaluations(self):
        "Return all internal evaluations for the given reading system, most recent first."
        evals = Evaluation.objects.filter(reading_system = self, evaluation_type = "1").order_by("-timestamp")
        retval = []
        for e in evals:
            retval.append(e)
        return retval




