from django.db import models
import common
from django.core.validators import MaxLengthValidator

class ResultSetMetadata(models.Model):
    class Meta:
        db_table = 'testsuite_app_result_set_metadata'
        app_label = 'testsuite_app'

    assistive_technology = models.CharField(max_length = common.LONG_STRING, null = True, blank = True)
    is_keyboard = models.BooleanField(default=False)
    is_mouse = models.BooleanField(default=False)
    is_touch = models.BooleanField(default=False)
    is_screenreader = models.BooleanField(default=False)
    is_braille = models.BooleanField(default=False)

class ResultSetManager(models.Manager):
    def create_result_set(self, testsuite, evaluation, user, assistive_technology = ''):
        if testsuite.testsuite_type == common.TESTSUITE_TYPE_ACCESSIBILITY:
            metadata = ResultSetMetadata(assistive_technology = assistive_technology)
            metadata.save()
            result_set = ResultSet(user = user, metadata = metadata, testsuite=testsuite, evaluation = evaluation)
            result_set.save()   
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
    metadata = models.ForeignKey('ResultSetMetadata', blank=True, null=True)
    testsuite = models.ForeignKey('TestSuite')
    evaluation = models.ForeignKey('Evaluation')
    percent_complete = models.DecimalField(decimal_places = 2, max_digits = 5, default=0)
    user = models.ForeignKey('UserProfile', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.update_percent_complete()
        super(ResultSet, self).save(*args, **kwargs)


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
            print "PCT COMPLETE: {0}".format(self.percent_complete)
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
            print "NO SCORE"
            return None


class Result(models.Model):
    class Meta:
        db_table = 'testsuite_app_result'
        app_label= 'testsuite_app'

    evaluation = models.ForeignKey('Evaluation')
    result = models.CharField(max_length = 1, choices = common.RESULT_TYPE, null = True, blank = True)
    notes = models.TextField(null=True, blank=True, validators=[MaxLengthValidator(300)])
    test = models.ForeignKey('Test')
    publish_notes = models.BooleanField(default=False)
    result_set = models.ForeignKey('ResultSet', null = True, blank = True)
