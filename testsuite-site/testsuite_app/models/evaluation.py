# from django.db import models
# from common import *

# class EvaluationManager(models.Manager):
#     def create_evaluation(self, reading_system):
#         "Create and return a new evaluation, along with an initialized set of result objects."
#         from test import Test
#         from score import Score
#         from result import Result, ResultSet
#         from category import Category
#         from testsuite import TestSuite
#         from score import AccessibilityScore
#         #from result_set import ResultSet

#         default_testsuite = TestSuite.objects.get_most_recent_testsuite_of_type(TESTSUITE_TYPE_DEFAULT)
#         accessible_testsuite = TestSuite.objects.get_most_recent_testsuite_of_type(TESTSUITE_TYPE_ACCESSIBILITY)
#         print "Creating evaluation for testsuites {0} (default) and {1} (accessibility)"\
#             .format(default_testsuite.version_date, accessible_testsuite.version_date)
        
#         evaluation = self.create(
#             testsuite = default_testsuite,
#             accessibility_testsuite = accessible_testsuite,
#             last_updated = generate_timestamp(),
#             percent_complete = 0.00,
#             reading_system = reading_system
#         )
#         evaluation.save()
        
#     def delete_associated(self, reading_system):
#         evaluations = Evaluation.objects.filter(reading_system = reading_system)
#         for evaluation in evaluations:
#             evaluation.delete()
    

# class Evaluation(models.Model, FloatToDecimalMixin):
#     class Meta:
#         db_table = 'testsuite_app_evaluation'
#         app_label= 'testsuite_app'

#     objects = EvaluationManager()
    
#     def save(self, *args, **kwargs):
#         "custom save routine"
#         print "SAVING EVAL"
#         self.last_updated = generate_timestamp()
#         self.save_scores()
#         self.update_percent_complete()
#         self.flagged_for_review = len(self.get_unanswered_flagged_items(self.get_default_result_set())) > 0
#         # TODO add a check for the other result sets

#         # call 'save' on the base class
#         super(Evaluation, self).save(*args, **kwargs)
    
#     # introduced for migration purposes
#     def save_partial(self, *args, **kwargs):
#         super(Evaluation, self).save(*args, **kwargs)
    
            
    
#     def get_result_set(self, result_set_id):
#         from result import ResultSet
#         from common import *
#         try:
#             rset = ResultSet.objects.get(id=result_set_id)
#             return rset
#         except ResultSet.DoesNotExist:
#             return None

#     def create_accessibility_result_set(self, user):
#         # add an accessibility eval
#         from result import ResultSet, Result
#         from test import Test
#         from category import Category
#         from score import AccessibilityScore
#         accessibility_result_set = ResultSet.objects.create_result_set(self.accessibility_testsuite, self, user, '')
#         accessibility_tests = Test.objects.filter(testsuite = self.accessibility_testsuite)
#         for t in accessibility_tests:
#             result = Result(test = t, evaluation = self, result = RESULT_NOT_ANSWERED, result_set = accessibility_result_set)
#             result.save()   
#         accessibility_categories = Category.objects.filter(testsuite = self.accessibility_testsuite)
#         for cat in accessibility_categories:
#             score = AccessibilityScore(
#                 category = cat,
#                 evaluation = self,
#                 result_set = accessibility_result_set
#             )
#             score.update(self.get_category_results(cat, accessibility_result_set))
#             score.save()  
#         total_score = AccessibilityScore(evaluation = self, category = None, result_set = accessibility_result_set)
#         total_score.save()
#         accessibility_result_set.save() 
#         return accessibility_result_set      

#     