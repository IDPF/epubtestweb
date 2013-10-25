from django.db import models
from common import RESULT_TYPE
from django.core.validators import MaxLengthValidator

class Result(models.Model):
    class Meta:
        db_table = 'testsuite_app_result'
        app_label= 'testsuite_app'

    evaluation = models.ForeignKey('Evaluation')
    result = models.CharField(max_length = 1, choices = RESULT_TYPE, null = True, blank = True)
    notes = models.TextField(null=True, blank=True, validators=[MaxLengthValidator(200)])
    #notes = models.CharField(max_length = 300, null=True, blank=True)
    test = models.ForeignKey('Test')

