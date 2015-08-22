from django.db import models
import common
from django.core.validators import MaxLengthValidator

class Result(models.Model):
    result = models.CharField(max_length = 1, choices = common.RESULT_NA_TYPE, null = True, blank = True)
    notes = models.TextField(null=True, blank=True, validators=[MaxLengthValidator(300)])
    test = models.ForeignKey('Test')
    publish_notes = models.BooleanField(default=False)
    evaluation = models.ForeignKey('Evaluation')
    flagged_as_new_or_changed = models.BooleanField(default = False)
    
