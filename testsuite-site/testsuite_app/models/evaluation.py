from django.db import models
from common import *

class EvaluationManager(models.Manager):
    def create_evaluation(self, reading_system):
        "Create and return a new evaluation, along with an initialized set of result objects."
        from test import Test
        from score import Score
        from result import Result
        from category import Category
        from testsuite import TestSuite

        testsuite = TestSuite.objects.get_most_recent_testsuite()
        print "Creating evaluation for testsuite {0}".format(testsuite.version_date)
        tests = Test.objects.filter(testsuite = testsuite)

        evaluation = self.create(
            testsuite = testsuite,
            last_updated = generate_timestamp(),
            percent_complete = 0.00,
            reading_system = reading_system
        )
        evaluation.save()
        
        total_score = Score(category = None, evaluation = evaluation)
        total_score.save()

        # create results for this evaluation
        for t in tests:
            result = Result(test = t, evaluation = evaluation, result = RESULT_NOT_ANSWERED)
            result.save()

        # update the score once results have been created
        total_score.update(evaluation.get_all_results())

        # create category score entries for this evaluation
        categories = Category.objects.filter(testsuite = evaluation.testsuite)
        for cat in categories:
            score = Score(
                category = cat,
                evaluation = evaluation
            )
            score.update(evaluation.get_category_results(cat))
            score.save()

        return evaluation

    def delete_associated(self, reading_system):
        evaluations = Evaluation.objects.filter(reading_system = reading_system)
        for evaluation in evaluations:
            evaluation.delete()
    

class Evaluation(models.Model, FloatToDecimalMixin):
    class Meta:
        db_table = 'testsuite_app_evaluation'
        app_label= 'testsuite_app'

    objects = EvaluationManager()
    
    testsuite = models.ForeignKey('TestSuite')
    last_updated = models.DateTimeField()
    percent_complete = models.DecimalField(decimal_places = 2, max_digits = 5)
    reading_system = models.ForeignKey('ReadingSystem')
    flagged_for_review = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        "custom save routine"
        self.last_updated = generate_timestamp()
        self.save_scores()
        self.update_percent_complete()
        self.flagged_for_review = len(self.get_unanswered_flagged_items()) > 0
        # call 'save' on the base class
        super(Evaluation, self).save(*args, **kwargs)
        
    def save_scores(self):
        # update the score
        from score import Score
        from result import Result
        from category import Category
        category_scores = Score.objects.filter(evaluation = self)
        for score in category_scores:
            results = None
            if score.category != None:
                results = self.get_category_results(score.category)
            else:
                results = self.get_all_results()
            score.update(results)

    def update_percent_complete(self):
        from result import Result
        all_results = self.get_all_results()
        if all_results.count() != 0:
            completed_results = Result.objects.filter(evaluation = self).exclude(result = RESULT_NOT_ANSWERED)
            pct_complete = (completed_results.count() * 1.0) / (len(all_results) * 1.0) * 100.0
            self.percent_complete = self.float_to_decimal(pct_complete)
            #self.percent_complete = (completed_results.count() * 1.0) / (len(all_results) * 1.0) * 100.0
        else:
            self.percent_complete = 0

    def get_reading_system(self):
        from reading_system import ReadingSystem
        try:
            rs = ReadingSystem.objects.get(evaluation = self)
        except ReadingSystem.DoesNotExist:
            return None
        return rs

    def get_category_results(self, category): 
        "get a queryset of all the results for the given category"
        tests = category.get_tests()
        return self.get_results(tests)

    def get_all_results(self):
        "get a queryset of all the results for the current testsuite"
        tests = self.get_tests()
        return self.get_results(tests)

    def get_results(self, tests):
        "get a queryset of results for the given tests"
        from result import Result
        results = Result.objects.filter(test__in=tests, evaluation = self)
        return results

    def get_result(self, test):
        from result import Result
        try:
            result = Result.objects.get(test = test, evaluation = self)
            return result
        except Result.DoesNotExist:
            return None
    
    def get_result_by_testid(self, testid):
        "get the result for a test with the given ID"
        from result import Result
        try:
            result_obj = Result.objects.get(evaluation = self, test__testid = testid)
            return result_obj
        except Result.DoesNotExist:
            return None

    def get_tests(self):
        "get a queryset of all tests"
        from test import Test
        tests = Test.objects.filter(testsuite = self.testsuite)
        return tests

    def get_top_level_category_scores(self):
        "return a dict {category: score, category: score, ...}"
        from score import Score
        #top_level_categories = Category.objects.filter(testsuite = self.testsuite, parent_category = None)
        top_level_categories = self.testsuite.get_top_level_categories()
        retval = {}
        for cat in top_level_categories:
            try:
                score = Score.objects.get(evaluation = self, category = cat)
                retval[cat] = score
            except Score.DoesNotExist:
                retval[cat] = None
        return retval

    def get_total_score(self):
        from score import Score
        # total score is the score where category = None
        try:
            score = Score.objects.get(evaluation = self, category = None)
            return score
        except Score.DoesNotExist:
            return None

    def is_category_complete(self, category):
        results = self.get_category_results(category)
        for r in results:
            if r.result == None:
                return False
        return True

    def get_category_score(self, category):
        "return the score for a single category"
        from score import Score
        try:
            score = Score.objects.get(evaluation = self, category = category)
            return score
        except Score.DoesNotExist:
            return None

    def get_unanswered_flagged_items(self):
        results = self.get_all_results()
        retval = []
        for r in results:
            if (r.test.flagged_as_new or r.test.flagged_as_changed) and r.result == None:
                retval.append(r.test)
        return retval

def generate_timestamp():
    from datetime import datetime
    from django.utils.timezone import utc
    return datetime.utcnow().replace(tzinfo=utc)
