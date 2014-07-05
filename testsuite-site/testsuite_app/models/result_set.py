from django.db import models
import common

class ATMetadata(models.Model):
    class Meta:
        db_table = 'testsuite_app_atmetadata'
        app_label = 'testsuite_app'

    result_set = models.ForeignKey('ResultSet')
    assistive_technology = models.CharField(max_length = common.LONG_STRING, null = True, blank = True)
    # is_keyboard = models.BooleanField(default=False)
    # is_mouse = models.BooleanField(default=False)
    # is_touch = models.BooleanField(default=False)
    input_type = models.CharField(max_length = 1, choices = common.INPUT_TYPE, default=common.INPUT_TYPE_KEYBOARD) 
    supports_screenreader = models.BooleanField(default=False)
    supports_braille = models.BooleanField(default=False)


class ResultSetManager(models.Manager):
    def create_result_set(self, reading_system, testsuite, user):
        from result import Result
        from score import Score, AccessibilityScore
        from testsuite_app import helper_functions
        last_updated = helper_functions.generate_timestamp()
        result_set = ResultSet(reading_system = reading_system, testsuite=testsuite, last_updated = last_updated, user = user)
        result_set.save()   
        print "Creating result set"
        # create empty results for each test
        tests = testsuite.get_tests()
        for test in tests:
            result = Result(result_set = result_set, test = test)
            result.save()

        # create empty scores for each category
        categories = testsuite.get_categories()
        for cat in categories:
            if testsuite.testsuite_type == common.TESTSUITE_TYPE_DEFAULT:
                score = Score(category = cat, result_set = result_set)
                score.save()
            else:
                score = AccessibilityScore(category = cat, result_set = result_set)
                score.save()

        if testsuite.testsuite_type == common.TESTSUITE_TYPE_DEFAULT:
            overall_score = Score(category = None, result_set = result_set)
            overall_score.save()
        else:
            overall_score = AccessibilityScore(category = None, result_set = result_set)
            overall_score.save()

        return result_set

    def get_result_sets_for_testsuite(self, reading_system, testsuite):
        try:
            return ResultSet.objects.filter(reading_system = reading_system, testsuite = testsuite)
        except ResultSet.DoesNotExist:
            return None

    def get_result_set_by_id(self, rset_id):
        try:
            return ResultSet.objects.get(id = rset_id)
        except ResultSet.DoesNotExist:
            return None
    

class ResultSet(models.Model, common.FloatToDecimalMixin):
    "A result set is pointed to by result objects and identifies them as belonging together"
    class Meta:
        db_table = 'testsuite_app_result_set'
        app_label= 'testsuite_app'

    objects = ResultSetManager()

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
        super(ResultSet, self).save(*args, **kwargs)

    def update_scores(self):
        from score import Score
        from score import AccessibilityScore
        from result import Result
        from category import Category

        # it would be nice to use a base class for the scores so we can just
        # call BaseScore.update
        # but purely abstract objects don't get put in the database... 

        if self.testsuite.testsuite_type == common.TESTSUITE_TYPE_DEFAULT:
            category_scores = Score.objects.filter(result_set = self)
        else:
            category_scores = AccessibilityScore.objects.filter(result_set = self)

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
            result_set = self)

        m.save()
        print "((( {0}".format(m.assistive_technology)

    def copy_metadata(self, result_set):
        # copy metadata from one result set to another
        metadata = result_set.get_metadata()
        if metadata == None:
            return
        # make a new copy of the metadata
        # if somehow the originating result_set gets deleted, our delete_associated would
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
            scores = Score.objects.filter(result_set = self)
        else:
            scores = AccessibilityScore.objects.filter(result_set = self)

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
            self.percent_complete = 0.0

    def get_results(self):
        "get a queryset of all the results for the given testsuite"
        from result import Result
        return Result.objects.filter(result_set = self)

    def get_not_supported_results():
        from result import Result
        return Result.objects.filter(result_set = self, result = common.RESULT_NOT_SUPPORTED)

    def get_results_for_category(self, category): 
        "get a queryset of all the results for the given category"
        tests = category.get_tests()
        return self.get_results_for_tests(tests)

    def get_results_for_tests(self, tests):
        "get a queryset of results for the given tests"
        from result import Result
        results = Result.objects.filter(test__in=tests, result_set = self)
        return results
    
    def get_result_for_test(self, test):
        from result import Result
        try:
            result = Result.objects.get(test = test, result_set = self)
            return result
        except Result.DoesNotExist:
            return None
    
    def get_result_for_test_by_id(self, testid):
        "get the result for a test with the given ID"
        from result import Result
        try:
            result_obj = Result.objects.get(test__testid = testid, result_set = self)
            return result_obj
        except Result.DoesNotExist:
            return None

    def get_category_score(self, category):
        "return the score for a single category"
        from score import Score, AccessibilityScore
        if self.testsuite.testsuite_type == common.TESTSUITE_TYPE_DEFAULT:
            try:
                score = Score.objects.get(result_set = self, category = category)
                return score
            except Score.DoesNotExist:
                return None
        else:
            try:
                score = AccessibilityScore.objects.get(result_set = self, category = category)
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

    def is_category_complete(self, result_set):
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
            metadata = ATMetadata.objects.get(result_set = self)
        except ATMetadata.DoesNotExist:
            return None
        return metadata



    
    




