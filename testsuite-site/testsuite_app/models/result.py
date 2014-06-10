from django.db import models
import common
from django.core.validators import MaxLengthValidator

class ATMetadata(models.Model):
    class Meta:
        db_table = 'testsuite_app_result_set_metadata'
        app_label = 'testsuite_app'

    result_set = models.ForeignKey('ResultSet')
    assistive_technology = models.CharField(max_length = common.LONG_STRING, null = True, blank = True)
    is_keyboard = models.BooleanField(default=False)
    is_mouse = models.BooleanField(default=False)
    is_touch = models.BooleanField(default=False)
    is_screenreader = models.BooleanField(default=False)
    is_braille = models.BooleanField(default=False)

class ResultSetManager(models.Manager):
    def create_result_set(self, testsuite, evaluation, user, assistive_technology = ''):
        result_set = ResultSet(user = user, testsuite=testsuite, evaluation = evaluation)
        result_set.save()   
        if testsuite.testsuite_type == common.TESTSUITE_TYPE_ACCESSIBILITY:
            metadata = ATMetadata(assistive_technology = assistive_technology)
            metadata.save()
            
        else:
            result_set = ResultSet(user = user, testsuite=testsuite, evaluation = evaluation)
            result_set.save()
        result_set.user = user
        return result_set

class ResultSet(models.Model, common.FloatToDecimalMixin):
    "A result set is pointed to by result objects and identifies them as belonging together"
    class Meta:
        db_table = 'testsuite_app_result_set'
        app_label= 'testsuite_app'

    objects = ResultSetManager()

    testsuite = models.ForeignKey('TestSuite')
    percent_complete = models.DecimalField(decimal_places = 2, max_digits = 5, default=0)
    user = models.ForeignKey('UserProfile', blank=True, null=True)
    last_updated = models.DateTimeField()
    reading_system = models.ForeignKey('ReadingSystem')
    flagged_for_review = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        self.update_percent_complete()
        super(ResultSet, self).save(*args, **kwargs)

    def save_scores(self):
        # update the score
        from score import Score
        from score import AccessibilityScore
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

        result_sets = self.get_accessibility_result_sets()
        for rset in result_sets:
            category_scores = AccessibilityScore.objects.filter(evaluation = self, result_set = rset)
            for score in category_scores:
                results = None
                if score.category != None:
                    print "UPDATING SCORE: {0}".format(score.category.name)
                    results = self.get_category_results(score.category, score.result_set)
                else:
                    print "UPDATING SCORE: {0}".format("ALL")
                    results = score.result_set.get_results_in_set()
                score.update(results)

    def delete_associated(self):
        from score import AccessibilityScore
        # delete results in the result set; delete metadata object
        results = self.get_results_in_set()
        for r in results:
            r.delete()
        scores = AccessibilityScore.objects.filter(result_set = self)
        for s in scores:
            s.delete()
        self.metadata.delete()

    def update_percent_complete(self):
        all_results = self.get_results_in_set()
        if all_results.count() != 0:
            completed_results = all_results.exclude(result = common.RESULT_NOT_ANSWERED)
            pct_complete = (completed_results.count() * 1.0) / (all_results.count() * 1.0) * 100.0
            self.percent_complete = self.float_to_decimal(pct_complete)
        else:
            self.percent_complete = 0.0

    def get_results_in_set(self):
        return Result.objects.filter(result_set = self)

    def get_accessibility_category_score(self, category):
        from score import AccessibilityScore
        try:
            score = AccessibilityScore.objects.get(result_set = self, category = category)
            return score
        except AccessibilityScore.DoesNotExist:
            return None

def validate_result(value):
    print "MODEL VALIDATION"
    return

class Result(models.Model):
    class Meta:
        db_table = 'testsuite_app_result'
        app_label= 'testsuite_app'

    evaluation = models.ForeignKey('Evaluation')
    result = models.CharField(max_length = 1, choices = common.RESULT_NA_TYPE, null = True, blank = True, validators=[validate_result])
    notes = models.TextField(null=True, blank=True, validators=[MaxLengthValidator(300)])
    test = models.ForeignKey('Test')
    publish_notes = models.BooleanField(default=False)
    result_set = models.ForeignKey('ResultSet', null = True, blank = True)
