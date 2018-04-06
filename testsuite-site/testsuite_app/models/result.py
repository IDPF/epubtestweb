from django.db import models
from . import common
from django.core.validators import MaxLengthValidator

class Result(models.Model):
    result = models.CharField(max_length = 1, choices = common.RESULT_TYPE, null = True, blank = True)
    #notes = models.TextField(null=True, blank=True, validators=[MaxLengthValidator(300)])
    notes = models.CharField(max_length = 300, null = True, blank = True)
    test = models.ForeignKey('Test')
    publish_notes = models.BooleanField(default=False)
    evaluation = models.ForeignKey('Evaluation')
    # the test for this result has changed so the result needs to be updated
    flagged = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        # if this result was flagged (meaning the test changed or is new), clear the flag
        # if there's an answer
        if self.flagged == True and self.result != common.RESULT_NOT_ANSWERED:
            self.flagged = False
        self.evaluation.update_category_and_feature_score(self)
        super(Result, self).save(*args, **kwargs)
