from django.db import models
from . import common
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Score(models.Model):
    # Score can apply to any 'item' (Category or Feature in our case)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    evaluation = models.ForeignKey('Evaluation')
    percent = models.DecimalField(decimal_places = 2, max_digits = 5, default = 0)
    fraction = models.CharField(max_length = common.SHORT_STRING)
    did_any_pass = models.BooleanField(default = False)
    
    def update(self):
        results = self.evaluation.get_results_for_category(self.content_object)
        num_passed = 0
        total_applicable = 0
        for result in results:
            if result.result == common.RESULT_SUPPORTED:
                num_passed += 1
            if result.result != common.RESULT_NOT_APPLICABLE:
                total_applicable += 1

        if total_applicable > 0:
            self.percent = num_passed / total_applicable
        else:
            self.percent = 0

        self.percent = self.percent * 100
        
        self.did_any_pass = num_passed > 0

        self.fraction = "{}/{}".format(num_passed, total_applicable)

        self.save()

