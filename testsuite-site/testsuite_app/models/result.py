from django.db import models
from evaluation import *
from test import *
from common import *

class Result(models.Model):
    class Meta:
        db_table = 'testsuite_app_result'
        app_label= 'testsuite_app'

    evaluation = models.ForeignKey('Evaluation')
    result = models.CharField(max_length = 1, choices = RESULT_TYPE, null = True, blank = True)
    test = models.ForeignKey(Test)

