from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser


SHORT_STRING = 50
LONG_STRING = 255

class ReadingSystem(models.Model):
    locale = models.CharField(max_length = SHORT_STRING, null = True, blank = True)
    name = models.CharField(max_length = LONG_STRING, blank = False, null = False)
    operating_system = models.CharField(max_length = SHORT_STRING, null = True, blank = True)
    sdk_version = models.CharField(max_length = SHORT_STRING, null = True, blank = True)
    version = models.CharField(max_length = SHORT_STRING, blank = False, null = False)

class TestSuite(models.Model):
    # version = version_date-version_revision (2013-01-01-5)
    version_date = models.DateField(max_length = SHORT_STRING)
    version_revision = models.IntegerField()

class Evaluation(models.Model):
    EVALUATION_TYPE = (
        ("1", "Internal"),
        ("2", "Public"),
        # consider a third type "Temporary"
    )
    evaluation_type = models.CharField(max_length = 1, choices = EVALUATION_TYPE)
    reading_system = models.ForeignKey(ReadingSystem)
    # User class has dependency on Evaluation class; order of declaration matters; use string value instead of classname as workaround
    user = models.ForeignKey('UserProfile')
    testsuite = models.ForeignKey(TestSuite)
    timestamp = models.DateTimeField()
    percent_complete = models.DecimalField(decimal_places = 2, max_digits = 5)

class Score(models.Model):
    percent_passed = models.DecimalField(decimal_places = 2, max_digits = 5)
    evaluation = models.ForeignKey(Evaluation)
    category = models.ForeignKey('Category')

# extend Django's built-in AbstractUser with a few properties
class UserProfile(AbstractUser):
    class Meta:
        app_label = 'testsuite_app'
    default_evaluation_type = models.CharField(max_length = 1, choices = Evaluation.EVALUATION_TYPE)
    organization = models.CharField(max_length = LONG_STRING)
    objects = UserManager()


class Category(models.Model):
    CATEGORY_TYPE = (
        ("1", "External"),
        ("2", "Epub"),
        ("3", "Internal"),
    )
    category_type = models.CharField(max_length = 1, choices = CATEGORY_TYPE)
    name = models.TextField()
    parent_category = models.ForeignKey('Category', null = True, blank = True)
    testsuite = models.ForeignKey(TestSuite)

class Test(models.Model):
    name = models.CharField(max_length = LONG_STRING)
    description = models.TextField()
    parent_category = models.ForeignKey(Category)
    required = models.BooleanField()
    testid = models.CharField(max_length = SHORT_STRING)
    testsuite = models.ForeignKey(TestSuite)
    xhtml =  models.TextField()


class Result(models.Model):
    RESULT_TYPE = (
        ("1", "Pass"),
        ("2", "Fail"),
        ("3", "NA")
    )
    evaluation = models.ForeignKey(Evaluation)
    result = models.CharField(max_length = 1, choices = RESULT_TYPE, null = True, blank = True)
    test = models.ForeignKey(Test)





