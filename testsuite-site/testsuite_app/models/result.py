from django.db import models
import common
from django.core.validators import MaxLengthValidator

class ResultSetMetadata(models.Model):
    class Meta:
        db_table = 'testsuite_app_result_set_metadata'
        app_label = 'testsuite_app'

    assistive_technology = models.CharField(max_length = common.LONG_STRING, null = True, blank = True)

class ResultSetManager(models.Manager):
    def create_result_set(self, testsuite, evaluation, assistive_technology = ''):
        if assistive_technology != '':
            metadata = ResultSetMetadata(assistive_technology = assistive_technology)
            metadata.save()
            result_set = ResultSet(metadata = metadata, testsuite=testsuite, evaluation = evaluation)
            result_set.save()   
        else:
            result_set = ResultSet(testsuite=testsuite, evaluation = evaluation)
            result_set.save()
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

    def update_percent_complete(self):
        all_results = Result.objects.filter(result_set = self)
        if all_results.count() != 0:
            completed_results = Result.objects.filter(result_set = self).exclude(result = common.RESULT_NOT_ANSWERED)
            pct_complete = (completed_results.count() * 1.0) / (len(all_results) * 1.0) * 100.0
            self.percent_complete = self.float_to_decimal(pct_complete)
        else:
            self.percent_complete = 0.0

    def get_results_in_set(self):
        return Results.objects.filter(result_set = self)

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
