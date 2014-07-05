from django.db import models
import common


class Score(models.Model, common.FloatToDecimalMixin):
    class Meta:
        db_table = 'testsuite_app_score'
        app_label= 'testsuite_app'

    num_required_tests = models.IntegerField(default = 0)
    num_optional_tests = models.IntegerField(default = 0)
    num_required_passed = models.IntegerField(default = 0)
    num_optional_passed = models.IntegerField(default = 0)

    pct_required_passed = models.DecimalField(decimal_places = 2, max_digits = 5, default = 0)
    pct_optional_passed = models.DecimalField(decimal_places = 2, max_digits = 5, default = 0)
    pct_total_passed = models.DecimalField(decimal_places = 2, max_digits = 5, default = 0)

    category = models.ForeignKey('Category', null=True, blank=True) # if category = None, this is the overall score
    result_set = models.ForeignKey('ResultSet')

    def update(self, results):
        "calculate a new score for the given results"
        self.num_required_tests = 0
        self.num_optional_tests = 0
        self.num_required_passed = 0
        self.num_optional_passed = 0
        self.pct_required_passed = 0
        self.pct_optional_passed = 0
        self.pct_total_passed = 0

        for r in results:
            if r.test.required == True:
                self.num_required_tests += 1
                if r.result == common.RESULT_SUPPORTED:
                    self.num_required_passed += 1
            elif r.test.required == False:
                self.num_optional_tests += 1
                if r.result == common.RESULT_SUPPORTED:
                    self.num_optional_passed += 1

        if self.num_required_tests > 0:
            self.pct_required_passed = (self.num_required_passed * 1.0) / (self.num_required_tests * 1.0) * 100
            self.pct_required_passed = round(self.pct_required_passed, 1)
            self.pct_required_passed = self.float_to_decimal(self.pct_required_passed)

        if self.num_optional_tests > 0:
            self.pct_optional_passed = (self.num_optional_passed * 1.0) / (self.num_optional_tests * 1.0) * 100
            self.pct_optional_passed = round(self.pct_optional_passed, 1)
            self.pct_optional_passed = self.float_to_decimal(self.pct_optional_passed)

        num_passed = self.num_required_passed + self.num_optional_passed
        num_total = self.num_required_tests + self.num_optional_tests
        if num_total > 0:
            self.pct_total_passed = (num_passed * 1.0) / (num_total * 1.0) * 100
            self.pct_total_passed = round(self.pct_total_passed, 1)
            self.pct_total_passed = self.float_to_decimal(self.pct_total_passed)
        else:
            print "Warning: no tests."
        
        self.save()

class AccessibilityScore(models.Model, common.FloatToDecimalMixin):
    class Meta:
        db_table = 'testsuite_app_accessibilityscore'
        app_label= 'testsuite_app'

    num_applicable_tests = models.IntegerField(default = 0)
    num_passed_tests = models.IntegerField(default = 0)
    
    pct_total_passed = models.DecimalField(decimal_places = 2, max_digits = 5, default = 0)

    category = models.ForeignKey('Category', null=True, blank=True) # if category = None, this is the overall score
    result_set = models.ForeignKey('ResultSet')

    def update(self, results):
        self.num_passed_tests = 0
        self.num_applicable_tests = 0
        for r in results:
            if r.result != common.RESULT_NOT_APPLICABLE:
                self.num_applicable_tests += 1
            if r.result == common.RESULT_SUPPORTED:
                self.num_passed_tests += 1
        if self.num_applicable_tests > 0:
            self.pct_total_passed = (self.num_passed_tests * 1.0) / (self.num_applicable_tests * 1.0) * 100
        self.save()

