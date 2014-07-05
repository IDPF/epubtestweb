from django.db import models
import common
from django.core.validators import MaxLengthValidator

class Result(models.Model):
    class Meta:
        db_table = 'testsuite_app_result'
        app_label= 'testsuite_app'

    result = models.CharField(max_length = 1, choices = common.RESULT_NA_TYPE, null = True, blank = True)
    notes = models.TextField(null=True, blank=True, validators=[MaxLengthValidator(300)])
    test = models.ForeignKey('Test')
    publish_notes = models.BooleanField(default=False)
    result_set = models.ForeignKey('ResultSet')
