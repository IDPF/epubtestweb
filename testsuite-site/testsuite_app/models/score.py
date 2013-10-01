from django.db import models

class Score(models.Model):
    class Meta:
        db_table = 'testsuite_app_score'
        app_label= 'testsuite_app'

    percent_passed = models.DecimalField(decimal_places = 2, max_digits = 5)
    evaluation = models.ForeignKey('Evaluation')
    category = models.ForeignKey('Category')
