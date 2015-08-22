from django.db import models

class Feature (models.Model):
    featureid = models.TextField()
    name = models.TextField()
    category = models.ForeignKey('Category')