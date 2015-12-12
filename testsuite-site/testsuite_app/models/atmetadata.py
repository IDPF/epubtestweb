from django.db import models
from . import common

class ATMetadata(models.Model):
    evaluation = models.ForeignKey('Evaluation')
    assistive_technology = models.CharField(max_length = common.LONG_STRING, null = True, blank = True)
    input_type = models.CharField(max_length = 1, choices = common.INPUT_TYPE, default=common.INPUT_TYPE_KEYBOARD) 
    supports_screenreader = models.BooleanField(default=False)
    supports_braille = models.BooleanField(default=False)
