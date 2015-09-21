from django.db import models

class Epub (models.Model):
    epubid = models.TextField()
    description = models.TextField()
    title = models.TextField()
    category = models.ForeignKey('Category')
    # TODO add source field