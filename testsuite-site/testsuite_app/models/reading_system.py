from django.db import models
from . import common

class ReadingSystem(models.Model):
    name = models.CharField(max_length = common.LONG_STRING, blank = False, null = False)
    operating_system = models.CharField(max_length = common.SHORT_STRING, blank = False, null = False)
    user = models.ForeignKey('UserProfile')

    def get_most_recent_version_with_evaluation(self, testsuite):
        # because we support many reading system versions and many testsuites, not all will have 
        # evaluations for every testsuite at each version revision
        reading_system_versions = ReadingSystemVersion.objects.filter(reading_system = self).order_by("-version_newness")
        # grab the first one that has an evaluation for the given testsuite
        for reading_system_version in reading_system_versions:
            if reading_system_version.get_evaluations(testsuite).count() > 0:
                return reading_system_version
        return None

    def get_all_versions(self):
        return ReadingSystemVersion.objects.filter(reading_system = self).order_by("-version_newness")

    def has_any_evaluations(self):
        from .testsuite import TestSuite
        reading_system_versions = ReadingSystemVersion.objects.filter(reading_system = self)
        testsuites = TestSuite.objects.get_most_recent_testsuites()
        for reading_system_version in reading_system_versions:
            for testsuite in testsuites:
                if reading_system_version.get_evaluations(testsuite).count() > 0:
                    return True
        return False

class ReadingSystemManager(models.Manager):
    def create_reading_system_version(self, version, notes, user, reading_system, is_most_recent_version = True):
        # if this is the most recent version in this family, then mark all the others as not the most recent version
        version_newness = 0
        if is_most_recent_version == True:
            reading_systems = ReadingSystemVersion.objects.filter(reading_system = reading_system).order_by("-version_newness")
            if reading_systems.count() > 0:
                version_newness = reading_systems[0].version_newness + 1
            
        reading_system = ReadingSystemVersion(
            version = version, 
            notes = notes, 
            user = user, 
            reading_system = reading_system,
            version_newness = version_newness)
        reading_system.save()
        return reading_system



class ReadingSystemVersion(models.Model):

    objects = ReadingSystemManager()
    
    version = models.CharField(max_length = common.SHORT_STRING, blank = False, null = False)
    notes = models.CharField(max_length = common.SHORT_STRING, null = True, blank = True)
    user = models.ForeignKey('UserProfile')
    status = models.CharField(max_length = 1, choices = common.READING_SYSTEM_STATUS_TYPE, default=common.READING_SYSTEM_STATUS_TYPE_CURRENT)
    reading_system = models.ForeignKey('ReadingSystem')
    # a greater number indicates a newer version
    version_newness = models.IntegerField(default = 0)

    def get_evaluations(self, testsuite):
        from .evaluation import Evaluation
        evaluations = Evaluation.objects.filter(reading_system_version = self, testsuite = testsuite)
        if testsuite.allow_many_evaluations == False and evaluations.count() > 1:
            print("WARNING TOO MANY EVALS")
        return evaluations

    def delete_associated(self):
        evaluations = Evaluation.objects.filter(reading_system = self)
        for evaluation in evaluations:
            evaluation.delete_associated()
            evaluation.delete()


