from django.db import models
from common import *

class EvaluationManager(models.Manager):
    def create_evaluation(self, reading_system):
        "Create and return a new evaluation, along with an initialized set of result objects."
        from test import Test
        from score import Score
        from result import Result, ResultSet
        from category import Category
        from testsuite import TestSuite
        #from result_set import ResultSet

        default_testsuite = TestSuite.objects.get_most_recent_testsuite_of_type(TESTSUITE_TYPE_DEFAULT)
        accessible_testsuite = TestSuite.objects.get_most_recent_testsuite_of_type(TESTSUITE_TYPE_ACCESSIBILITY)
        print "Creating evaluation for testsuites {0} (default) and {1} (accessibility)"\
            .format(default_testsuite.version_date, accessible_testsuite.version_date)
        
        evaluation = self.create(
            testsuite = default_testsuite,
            accessibility_testsuite = accessible_testsuite,
            last_updated = generate_timestamp(),
            percent_complete = 0.00,
            reading_system = reading_system
        )
        evaluation.save()

        total_score = Score(category = None, evaluation = evaluation)
        total_score.save()

        # create default results for this evaluation
        default_tests = Test.objects.filter(testsuite = default_testsuite)
        
        default_result_set = ResultSet.objects.create_result_set(default_testsuite, evaluation)
        for t in default_tests:
            result = Result(test = t, evaluation = evaluation, result = RESULT_NOT_ANSWERED, result_set = default_result_set)
            result.save()

        # only do scoring for the default testsuite
        # update the score once results have been created
        total_score.update(evaluation.get_all_results(default_result_set))

        # create category score entries for this evaluation
        categories = Category.objects.filter(testsuite = default_testsuite)
        for cat in categories:
            score = Score(
                category = cat,
                evaluation = evaluation
            )
            score.update(evaluation.get_category_results(cat, default_result_set))
            score.save()

        # add an accessibility eval
        accessibility_result_set = ResultSet.objects.create_result_set(accessible_testsuite, evaluation, '')
        accessibility_tests = Test.objects.filter(testsuite = accessible_testsuite)
        for t in accessibility_tests:
            result = Result(test = t, evaluation = evaluation, result = RESULT_NOT_ANSWERED, result_set = accessibility_result_set)
            result.save()            

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
    
    # scheduled for deprecation
    percent_complete = models.DecimalField(decimal_places = 2, max_digits = 5, default=0)
    
    testsuite = models.ForeignKey('TestSuite', related_name='evaluation_testsuite')
    # new as of march 2014
    accessibility_testsuite = models.ForeignKey('TestSuite', related_name='evaluation_accessibility_testsuite', null=True, blank=True)
    last_updated = models.DateTimeField()
    reading_system = models.ForeignKey('ReadingSystem')
    flagged_for_review = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        "custom save routine"
        self.last_updated = generate_timestamp()
        self.save_scores()
        self.update_percent_complete()
        self.flagged_for_review = len(self.get_unanswered_flagged_items(self.get_default_result_set())) > 0
        # TODO add a check for the other result sets

        # call 'save' on the base class
        super(Evaluation, self).save(*args, **kwargs)
    
    # introduced for migration purposes
    def save_partial(self, *args, **kwargs):
        super(Evaluation, self).save(*args, **kwargs)
    
    # only categories from the default testsuite have associated score objects
    def save_scores(self):
        # update the score
        from score import Score
        from result import Result
        from category import Category
        category_scores = Score.objects.filter(evaluation = self)
        for score in category_scores:
            results = None
            if score.category != None:
                results = self.get_category_results(score.category, self.get_default_result_set())
            else:
                results = self.get_all_results(self.get_default_result_set())
            score.update(results)

    def update_percent_complete(self):
        from result import Result
        default_result_set = self.get_default_result_set()
        if default_result_set != None:
            default_result_set.update_percent_complete()
        accessibility_result_set = self.get_accessibility_result_set()
        if accessibility_result_set != None:
            accessibility_result_set.update_percent_complete()
            
    def get_reading_system(self):
        from reading_system import ReadingSystem
        try:
            rs = ReadingSystem.objects.get(evaluation = self)
        except ReadingSystem.DoesNotExist:
            return None
        return rs
    
    def get_default_result_set(self):
        # there should only be one
        #from result_set import ResultSet
        from result import ResultSet
        from common import *
        try:
            result_set = ResultSet.objects.get(evaluation = self, testsuite=self.testsuite)
        except ResultSet.DoesNotExist:
            return None
        return result_set

    # TEMPORARY! for while we are supporting a single accessibility evaluation per reading system
    def get_accessibility_result_set(self):
        from result import ResultSet
        from common import *
        result_sets = ResultSet.objects.filter(evaluation = self, testsuite=self.accessibility_testsuite)        
        if result_sets.count() > 0:
            result_set = result_sets[0]
            return result_set
        else:
            return None

    def get_category_results(self, category, result_set): 
        "get a queryset of all the results for the given category"
        tests = category.get_tests()
        return self.get_results(tests, result_set)

    def get_all_results(self, result_set):
        "get a queryset of all the results for the given testsuite"
        from result import Result
        return Result.objects.filter(result_set = result_set)

    def get_results(self, tests, result_set):
        "get a queryset of results for the given tests"
        from result import Result
        results = Result.objects.filter(test__in=tests, evaluation = self, result_set = result_set)
        return results

    def get_result(self, test, result_set):
        from result import Result
        try:
            result = Result.objects.get(test = test, evaluation = self, result_set = result_set)
            return result
        except Result.DoesNotExist:
            return None
    
    def get_result_by_testid(self, testid, result_set):
        "get the result for a test with the given ID"
        from result import Result
        try:
            result_obj = Result.objects.get(evaluation = self, test__testid = testid, result_set = result_set)
            return result_obj
        except Result.DoesNotExist:
            return None

    def get_tests(self, testsuite):
        "get a queryset of all tests"
        from test import Test
        tests = Test.objects.filter(testsuite = testsuite)
        return tests

    def get_top_level_category_scores(self, testsuite):
        "return a dict {category: score, category: score, ...}"
        from score import Score
        top_level_categories = testsuite.get_top_level_categories()
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

    def is_category_complete(self, category, result_set):
        results = self.get_category_results(category, result_set)
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

    def get_unanswered_flagged_items(self, result_set):
        results = self.get_all_results(result_set)
        retval = []
        for r in results:
            if (r.test.flagged_as_new or r.test.flagged_as_changed) and r.result == None:
                retval.append(r.test)
        return retval

def generate_timestamp():
    from datetime import datetime
    from django.utils.timezone import utc
    return datetime.utcnow().replace(tzinfo=utc)
