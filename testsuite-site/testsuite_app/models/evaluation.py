from django.db import models
from common import *
from decimal import *

class Evaluation(models.Model):
    class Meta:
        db_table = 'testsuite_app_evaluation'
        app_label= 'testsuite_app'

    evaluation_type = models.CharField(max_length = 1, choices = EVALUATION_TYPE)
    user = models.ForeignKey('UserProfile') # workaround in quotes
    testsuite = models.ForeignKey('TestSuite')
    timestamp = models.DateTimeField()
    percent_complete = models.DecimalField(decimal_places = 2, max_digits = 5)


    def is_evaluation_complete(self):
        "Test if the evaluation is complete (all results must have a value != None)"
        from result import Result
        incomplete_results = Result.objects.filter(evaluation = self, result = None)
        return incomplete_results.count() == 0

    def get_evaluation_as_nested_categories(self):
        "Return a web template-friendly array of dicts describing an evaluation and its categories."
        top_level_categories = self.testsuite.get_top_level_categories()
        summary = []
        for c in top_level_categories:
            summary.append(self.summarize(c))
        return summary

    def summarize(self, item):
        "Return a nested structure of categories and tests. item is a category or test."
        from category import Category
        from score import Score
        from result import Result
        if type(item) == Category:
            score = Score.objects.get(evaluation = self, category = item)
            # append the score as a category property
            # TODO consider putting it in the dict
            item.category_score = score.percent_passed
            subcats = Category.objects.filter(parent_category = item)
            subcat_summaries = []
            for c in subcats:
                subcat_summaries.append(self.summarize(c))
            results = Result.objects.filter(test__parent_category = item, evaluation = self)
            return {"item": item, "depth": item.get_depth(), "subcategories": subcat_summaries, "results": results}

    def print_item_summary(self, summary):
        "Debug-print the summary data generated above."
        prefix = "\t" * summary['item'].get_depth()
        print "{0}{1}".format(prefix, summary['item'].name.encode('utf-8'))

        for s in summary['subcategories']:
            print_item_summary(s)

        for r in summary['result']:
            print "{0}TEST {1}".format(prefix+"\t", r.name.encode('utf-8'))

    def get_pct_complete(self):
        "Calculate the percent complete."
        from result import Result
        all_results = Result.objects.filter(evaluation = self)
        complete_results = Result.objects.filter(evaluation = self).exclude(result = None)
        pct_complete = (complete_results.count() * 1.0) / (all_results.count() * 1.0) * 100.0
        return self.float_to_decimal(pct_complete)

    def get_results(self, category):
        from result import Result
        tests = category.get_tests()
        results = []
        for t in tests:
            result = Result.objects.filter(test = t, evaluation = self)[0]
            results.append(result)
        return results

    # return a dict {category: score, category: score, ...}
    def get_top_level_category_scores(self):
        from category import Category
        top_level_categories = Category.objects.filter(testsuite = self.testsuite, parent_category = None)
        retval = {}
        for cat in top_level_categories:
            # use the database object if it's available
            score = Score.objects.get(evaluation = self, category = cat)
            retval[cat] = score.percent_passed
        return retval

    def get_category_score(self, category):
        results = self.get_results(category)
        # aside: can a test be both required and not applicable?
        required = {"pass": 0, "fail": 0, "na": 0}
        optional = {"pass": 0, "fail": 0, "na": 0}

        for r in results:
            # "1" = Pass, "2" = Fail, "3" = NA
            if r.test.required == True:
                if r.result == "1":
                    required['pass'] += 1
                elif r.result == "2":
                    required['fail'] += 1
                elif r.result == "3":
                    required['na'] += 1
            else:
                if r.result == "1":
                    optional['pass'] += 1
                elif r.result == "2":
                    optional['fail'] += 1
                elif r.result == "3":
                    optional['na'] += 1

        category_score = self.calculate_score(required, optional)
        return category_score

    # return a percentage
    def calculate_score(self, required, optional):
        total_applicable = required['pass'] + required['fail'] + optional['pass'] + optional['fail']
        total_passed = required['pass'] + optional['pass']
        # the total score is based on the number of applicable tests that passed
        if total_applicable != 0:
            total_score = (total_passed * 1.0) / (total_applicable * 1.0) * 100
            total_score = round(total_score, 1)
            return total_score
        else:
            return 0

    def calculate_and_save_scores(self):
        from category import Category
        from score import Score
        categories = Category.objects.filter(testsuite = self.testsuite)
        for cat in categories:
            score = Score.objects.get(evaluation = self, category = cat)
            score.percent_passed = self.float_to_decimal(self.get_category_score(cat))
            score.save()

    # this is the "right way"...
    # http://docs.python.org/release/2.6.7/library/decimal.html#decimal-faq
    # and this is the way that works in practice (in this case, we can live with rounding error past 2 decimal places)
    def float_to_decimal(self, f):
        s = str(f)
        return Decimal(s)
