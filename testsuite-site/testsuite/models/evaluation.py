from django.db import models
import common

class EvaluationManager(models.Manager):
    def create_evaluation(self, reading_system, testsuite, user):
        from result import Result
        from score import Score, AccessibilityScore
        from testsuite import helper_functions
        last_updated = helper_functions.generate_timestamp()
        evaluation = Evaluation(reading_system = reading_system, testsuite=testsuite, last_updated = last_updated, user = user)
        evaluation.save()   
        print "Creating evaluation"
        # create empty results for each test
        tests = testsuite.get_tests()
        for test in tests:
            result = Result(evaluation = evaluation, test = test)
            result.save()

        # create empty scores for each category
        categories = testsuite.get_categories()
        for cat in categories:
            if testsuite.testsuite_type == common.TESTSUITE_TYPE_DEFAULT:
                score = Score(category = cat, evaluation = evaluation)
                score.save()
            else:
                score = AccessibilityScore(category = cat, evaluation = evaluation)
                score.save()

        if testsuite.testsuite_type == common.TESTSUITE_TYPE_DEFAULT:
            overall_score = Score(category = None, evaluation = evaluation)
            overall_score.save()
        else:
            overall_score = AccessibilityScore(category = None, evaluation = evaluation)
            overall_score.save()

        evaluation.visibility = reading_system.visibility

        return evaluation

    def get_evaluations_for_testsuite(self, reading_system, testsuite):
        try:
            return Evaluation.objects.filter(reading_system = reading_system, testsuite = testsuite)
        except Evaluation.DoesNotExist:
            return None

    def get_evaluation_by_id(self, evaluation_id):
        try:
            return Evaluation.objects.get(id = evaluation_id)
        except Evaluation.DoesNotExist:
            return None
    

class Evaluation(models.Model, common.FloatToDecimalMixin):
    "A result set is pointed to by result objects and identifies them as belonging together"
    objects = EvaluationManager()

    testsuite = models.ForeignKey('TestSuite')
    percent_complete = models.DecimalField(decimal_places = 2, max_digits = 5, default=0)
    last_updated = models.DateTimeField()
    reading_system = models.ForeignKey('ReadingSystem')
    flagged_for_review = models.BooleanField(default = False)
    visibility = models.CharField(max_length = 1, choices = common.VISIBILITY_TYPE, default=common.VISIBILITY_MEMBERS_ONLY)
    user = models.ForeignKey('UserProfile')
    

    def save(self, *args, **kwargs):
        self.update_percent_complete()
        self.update_scores()
        self.update_flagged_for_review()
        super(Evaluation, self).save(*args, **kwargs)

    def update_scores(self):
        from score import Score
        from score import AccessibilityScore
        from result import Result
        from category import Category

        # it would be nice to use a base class for the scores so we can just
        # call BaseScore.update
        # but purely abstract objects don't get put in the database... 

        if self.testsuite.testsuite_type == common.TESTSUITE_TYPE_DEFAULT:
            category_scores = Score.objects.filter(evaluation = self)
        else:
            category_scores = AccessibilityScore.objects.filter(evaluation = self)

        for score in category_scores:
            results = None
            if score.category != None:
                results = self.get_results_for_category(score.category)
            else:
                results = self.get_results()
            score.update(results)
    def update_flagged_for_review(self):
        results = self.get_results()
        for r in results:
            if (r.test.flagged_as_new or r.test.flagged_as_changed) and r.result == None:
                self.flagged_for_review = True
                return
        self.flagged_for_review = False

    def add_metadata(self, assistive_technology, input_type, supports_screenreader, supports_braille):
        m = ATMetadata(assistive_technology = assistive_technology,
            input_type = input_type,
            supports_screenreader = supports_screenreader,
            supports_braille = supports_braille,
            evaluation = self)

        m.save()
        print "((( {0}".format(m.assistive_technology)

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
        from score import AccessibilityScore, Score
        # delete results in the result set; delete metadata object
        results = self.get_results()
        for r in results:
            r.delete()

        scores = []
        if self.testsuite.testsuite_type == common.TESTSUITE_TYPE_DEFAULT:
            scores = Score.objects.filter(evaluation = self)
        else:
            scores = AccessibilityScore.objects.filter(evaluation = self)

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
            self.percent_complete = self.float_to_decimal(pct_complete)
        else:
            self.percent_complete = self.float_to_decimal(0.0)

    def get_results(self):
        "get a queryset of all the results for the given testsuite"
        from result import Result
        return Result.objects.filter(evaluation = self)

    def get_not_supported_results():
        from result import Result
        return Result.objects.filter(evaluation = self, result = common.RESULT_NOT_SUPPORTED)

    def get_results_for_category(self, category): 
        "get a queryset of all the results for the given category"
        tests = category.get_tests()
        return self.get_results_for_tests(tests)

    def get_results_for_tests(self, tests):
        "get a queryset of results for the given tests"
        from result import Result
        results = Result.objects.filter(test__in=tests, evaluation = self)
        return results
    
    def get_result_for_test(self, test):
        from result import Result
        try:
            result = Result.objects.get(test = test, evaluation = self)
            return result
        except Result.DoesNotExist:
            return None
    
    def get_result_for_test_by_id(self, testid):
        "get the result for a test with the given ID"
        from result import Result
        try:
            result_obj = Result.objects.get(test__testid = testid, evaluation = self)
            return result_obj
        except Result.DoesNotExist:
            return None

    def get_category_score(self, category):
        "return the score for a single category"
        from score import Score, AccessibilityScore
        if self.testsuite.testsuite_type == common.TESTSUITE_TYPE_DEFAULT:
            try:
                score = Score.objects.get(evaluation = self, category = category)
                return score
            except Score.DoesNotExist:
                return None
        else:
            try:
                score = AccessibilityScore.objects.get(evaluation = self, category = category)
                return score
            except AccessibilityScore.DoesNotExist:
                return None    

    def get_top_level_category_scores(self, testsuite):
        "return a dict {category: score, category: score, ...}"
        top_level_categories = testsuite.get_top_level_categories()
        retval = {}
        for cat in top_level_categories:
            score = self.get_category_score(cat)
            retval[cat] = score
        return retval

    def get_total_score(self):
        # total score is the score where category = None
        score = self.get_category_score(None)
        return score

    def is_category_complete(self, evaluation):
        results = self.get_results_for_category(category)
        for r in results:
            if r.result == None:
                return False
        return True

    def get_unanswered_flagged_tests(self):
        results = self.get_results()
        retval = []
        for r in results:
            if (r.test.flagged_as_new or r.test.flagged_as_changed) and r.result == None:
                retval.append(r.test)
        return retval

    def get_metadata(self):
        try:
            metadata = ATMetadata.objects.get(evaluation = self)
        except ATMetadata.DoesNotExist:
            return None
        return metadata



    
    




