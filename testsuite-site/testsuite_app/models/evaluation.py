from django.db import models
from . import common

class EvaluationManager(models.Manager):
    def create_evaluation(self, reading_system_version, testsuite, user):
        from .result import Result
        from .score import Score
        from testsuite_app import helper_functions
        print("Creating evaluation")
        last_updated = helper_functions.generate_timestamp()
        evaluation = Evaluation(reading_system_version = reading_system_version, 
            testsuite=testsuite, last_updated = last_updated, user = user)
        evaluation.save()   
        # create empty scores for each category and each feature
        categories = testsuite.get_categories()
        for category in categories:
            category_score = Score(content_object = category, evaluation = evaluation)
            category_score.save()

            features = category.get_features()
            for feature in features:
                feature_score = Score(content_object = feature, evaluation = evaluation)
                feature_score.save()
        
        # create empty results for each test
        tests = testsuite.get_tests()
        for test in tests:
            result = Result(evaluation = evaluation, test = test)
            result.result = common.RESULT_NOT_ANSWERED
            result.save()
        
        return evaluation

    

class Evaluation(models.Model):
    "A result set is pointed to by result objects and identifies them as belonging together"
    objects = EvaluationManager()

    testsuite = models.ForeignKey('TestSuite')
    percent_complete = models.DecimalField(decimal_places = 2, max_digits = 5, default=0)
    last_updated = models.DateTimeField()
    reading_system_version = models.ForeignKey('ReadingSystemVersion')
    flagged_for_review = models.BooleanField(default = False)
    visibility = models.CharField(max_length = 1, choices = common.VISIBILITY_TYPE, default=common.VISIBILITY_MEMBERS_ONLY)
    user = models.ForeignKey('UserProfile')
    

    def save(self, *args, **kwargs):
        self.update_percent_complete()
        self.update_scores()
        self.update_flagged_for_review()
        super(Evaluation, self).save(*args, **kwargs)

    def update_scores(self):
        from .score import Score
        scores = Score.objects.filter(evaluation = self)
        for score in scores:
            score.update()

    def update_category_and_feature_score(self, result):
        # update the category that this test is in
        # it's much more efficient than updating all the scores in the whole evaluation
        from .score import Score
        from .category import Category
        category = result.test.category
        feature = result.test.feature
        score = self.get_score(category)
        score.update()
        score = self.get_score(feature)
        score.update()

    def update_flagged_for_review(self):
        results = self.get_results()
        for r in results:
            if (r.test.flagged_as_new or r.test.flagged_as_changed) and r.result == None:
                self.flagged_for_review = True
                return
        self.flagged_for_review = False

    def add_metadata(self, assistive_technology, input_type, supports_screenreader, supports_braille):
        from .atmetadata import ATMetadata
        m = ATMetadata(assistive_technology = assistive_technology,
            input_type = input_type,
            supports_screenreader = supports_screenreader,
            supports_braille = supports_braille,
            evaluation = self)

        m.save()
        print("((( {0}".format(m.assistive_technology))

    def copy_metadata(self, evaluation):
        # copy metadata from one result set to another
        metadata = evaluation.get_metadata()
        if metadata == None:
            return
        # make a new copy of the metadata
        # if somehow the originating evaluation gets deleted, our delete_associated would
        # dump its metadata too
        self.add_metadata(metadata.assistive_technology, 
            metadata.input_type,
            metadata.supports_screenreader, 
            metadata.supports_braille)

    def delete_associated(self):
        from .score import Score
        # delete results in the result set; delete metadata object
        results = self.get_results()
        for r in results:
            r.delete()

        scores = Score.objects.filter(evaluation = self)
        
        for s in scores:
            s.delete()

        metadata = self.get_metadata()
        if metadata != None:
            metadata.delete()

    def update_percent_complete(self):
        all_results = self.get_results()
        if all_results.count() != 0:
            completed_results = all_results.exclude(result = common.RESULT_NOT_ANSWERED)
            pct_complete = (completed_results.count() * 1.0) / (all_results.count() * 1.0) * 100.0
            self.percent_complete = pct_complete #self.float_to_decimal(pct_complete)
        else:
            self.percent_complete = 0.0 #self.float_to_decimal(0.0)

    def get_results(self):
        "get a queryset of all the results for the given testsuite"
        from .result import Result
        return Result.objects.filter(evaluation = self)

    def get_not_supported_results():
        from .result import Result
        return Result.objects.filter(evaluation = self, result = common.RESULT_NOT_SUPPORTED)

    def get_results_for_category(self, category): 
        "get a queryset of all the results for the given category"
        tests = category.get_tests()
        return self.get_results_for_tests(tests)

    def get_results_for_tests(self, tests):
        "get a queryset of results for the given tests"
        from .result import Result
        results = Result.objects.filter(test__in=tests, evaluation = self)
        return results
    
    def get_result_for_test(self, test):
        from .result import Result
        try:
            result = Result.objects.get(test = test, evaluation = self)
            return result
        except Result.DoesNotExist:
            return None
    
    def get_result_for_test_by_id(self, testid):
        "get the result for a test with the given ID"
        from .result import Result
        try:
            result_obj = Result.objects.get(test__test_id = testid, evaluation = self)
            return result_obj
        except Result.DoesNotExist:
            return None

    def get_score(self, category_or_feature):
        "return the score for a single category/feature"
        from .score import Score
        from django.contrib.contenttypes.models import ContentType

        try:
            score = Score.objects.get(
                evaluation = self, 
                content_type = ContentType.objects.get_for_model(category_or_feature),
                object_id = category_or_feature.id)
            return score
        except Score.DoesNotExist:
            print("WARNING: no score found for {}".format(category_or_feature))
            return None
        
    def is_category_complete(self, evaluation):
        results = self.get_results_for_category(category)
        for r in results:
            if r.result == None:
                return False
        return True

    def get_metadata(self):
        from .atmetadata import ATMetadata
        try:
            metadata = ATMetadata.objects.get(evaluation = self)
        except ATMetadata.DoesNotExist:
            return None
        return metadata



    
    




