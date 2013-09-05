from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from evaluation import *
from common import *

# extend Django's built-in AbstractUser with a few properties
class UserProfile(AbstractUser):
    class Meta:
        db_table = 'testsuite_app_userprofile'
        app_label= 'testsuite_app'

    default_evaluation_type = models.CharField(max_length = 1, choices = EVALUATION_TYPE)
    organization = models.CharField(max_length = LONG_STRING)
    objects = UserManager()
