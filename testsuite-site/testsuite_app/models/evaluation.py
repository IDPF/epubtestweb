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
        from score import AccessibilityScore
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
        print "hi"
        evaluation.save()
        total_score = Score(category = None, evaluation = evaluation)
        total_score.save()


        # create default results for this evaluation
        default_tests = Test.objects.filter(testsuite = default_testsuite)
        
        print "Creating default result set"
        default_result_set = ResultSet.objects.create_result_set(default_testsuite, evaluation, evaluation.reading_system.user)
        for t in default_tests:
            result = Result(test = t, evaluation = evaluation, result = RESULT_NOT_ANSWERED, result_set = default_result_set)
            result.save()
        default_result_set.save()

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
    
    def save(self, *args, **kwargs):
        "custom save routine"
        print "SAVING EVAL"
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
    
            
    
    def get_result_set(self, result_set_id):
        from result import ResultSet
        from common import *
        try:
            rset = ResultSet.objects.get(id=result_set_id)
            return rset
        except ResultSet.DoesNotExist:
            return None

    def create_accessibility_result_set(self, user):
        # add an accessibility eval
        from result import ResultSet, Result
        from test import Test
        from category import Category
        from score import AccessibilityScore
        accessibility_result_set = ResultSet.objects.create_result_set(self.accessibility_testsuite, self, user, '')
        accessibility_tests = Test.objects.filter(testsuite = self.accessibility_testsuite)
        for t in accessibility_tests:
            result = Result(test = t, evaluation = self, result = RESULT_NOT_ANSWERED, result_set = accessibility_result_set)
            result.save()   
        accessibility_categories = Category.objects.filter(testsuite = self.accessibility_testsuite)
        for cat in accessibility_categories:
            score = AccessibilityScore(
                category = cat,
                evaluation = self,
                result_set = accessibility_result_set
            )
            score.update(self.get_category_results(cat, accessibility_result_set))
            score.save()  
        total_score = AccessibilityScore(evaluation = self, category = None, result_set = accessibility_result_set)
        total_score.save()
        accessibility_result_set.save() 
        return accessibility_result_set      

    def get_category_results(self, category, result_set): 
        "get a queryset of all the results for the given category"
        tests = category.get_tests()
        print "CATEGORY HAS  {0} TESTS".format(len(tests))
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
