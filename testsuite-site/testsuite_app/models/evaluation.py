from django.db import models
from common import EVALUATION_TYPE

class EvaluationManager(models.Manager):
    def create_evaluation(self, reading_system):
        "Create and return a new evaluation, along with an initialized set of result objects."
        from test import Test
        from score import Score
        from result import Result
        from category import Category
        from testsuite import TestSuite

        testsuite = TestSuite.objects.get_most_recent_testsuite()
        tests = Test.objects.filter(testsuite = testsuite)

        evaluation = self.create(
            evaluation_type = "1", # internal
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
            result = Result(test = t, evaluation = evaluation, result = None) # 4 = no value yet
            result.save()

        # create category score entries for this evaluation
        categories = Category.objects.filter(testsuite = evaluation.testsuite)
        for cat in categories:
            score = Score(
                category = cat,
                evaluation = evaluation
            )
            score.save()

        return evaluation

    def delete_associated(self, reading_system):
        evaluations = Evaluation.objects.filter(reading_system = reading_system)
        for evaluation in evaluations:
            evaluation.delete()
    

class Evaluation(models.Model):
    class Meta:
        db_table = 'testsuite_app_evaluation'
        app_label= 'testsuite_app'

    objects = EvaluationManager()

    evaluation_type = models.CharField(max_length = 1, choices = EVALUATION_TYPE)
    testsuite = models.ForeignKey('TestSuite')
    last_updated = models.DateTimeField()
    percent_complete = models.DecimalField(decimal_places = 2, max_digits = 5)
    reading_system = models.ForeignKey('ReadingSystem')
    flagged_for_review = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        "custom save routine"
        # clear the "please review" flag
        self.flagged_for_review = False
        self.last_updated = generate_timestamp()
        self.save_scores()
        self.update_percent_complete()
        # call 'save' on the base class
        super(Evaluation, self).save(*args, **kwargs)
        
    def save_scores(self):
        # update the score
        from score import Score
        from result import Result
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
        # note that we don't use all_results.count() because get_results() returns an array, not a queryset
        if len(all_results) != 0:
            completed_results = Result.objects.filter(evaluation = self).exclude(result = None)
            pct_complete = (completed_results.count() * 1.0) / (len(all_results) * 1.0) * 100.0
            self.percent_complete = float_to_decimal(pct_complete)
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
        "get an array of all the results for the given category"
        tests = category.get_tests()
        return self.get_results(tests)

    def get_all_results(self):
        "get an array of all the results for the current testsuite"
        tests = self.get_tests()
        return self.get_results(tests)

    def get_results(self, tests):
        "get an array of results for the given tests"
        from result import Result
        results = []
        for t in tests:
            try:
                result = Result.objects.get(test = t, evaluation = self)
            except Result.DoesNotExist:
                continue
            results.append(result)
        return results

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
            
# this is the "right way"...
# http://docs.python.org/release/2.6.7/library/decimal.html#decimal-faq
# and this is the way that works in practice (in this case, we can live with rounding error past 2 decimal places)
def float_to_decimal(f):
    from decimal import Decimal
    s = str(f)
    return Decimal(s)

def generate_timestamp():
    from datetime import datetime
    from django.utils.timezone import utc
    return datetime.utcnow().replace(tzinfo=utc)
