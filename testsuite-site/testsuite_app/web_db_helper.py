# useful database functions

from models import *
from django.utils.timezone import utc
from datetime import datetime
from decimal import *

# get the most recent scores for each reading system
def get_scores(categories):
    retval = []
    reading_systems = ReadingSystem.objects.all()
    for rs in reading_systems:
        evaluation = get_most_recent_evaluation(rs)
        if evaluation is None:
            retval.append({"reading_system": rs, "scores": None})
        else:
            scores = get_category_scores(evaluation)
            # scores should have the same order as categories
            ordered_scores = []
            for cat in categories:
                ordered_scores.append(scores[cat])
            retval.append({"reading_system": rs, "scores": ordered_scores})
    return retval

# get the most recent public complete evaluation
def get_most_recent_evaluation(rs):
    evaluations = Evaluation.objects.filter(reading_system = rs, evaluation_type = "2").order_by("-timestamp")
    for e in evaluations:
        if is_evaluation_complete(e):
            return e
    return None

# an evaluation is complete if all the results have a value != None
def is_evaluation_complete(evaluation):
    incomplete_results = Result.objects.filter(evaluation = evaluation, result = None)
    return incomplete_results.count() == 0

def create_new_evaluation(testsuite, eval_type, reading_system, user):
    tests = Test.objects.filter(testsuite = testsuite)
    if len(tests) == 0:
        return None

    evaluation = Evaluation(
        evaluation_type = eval_type,
        reading_system = reading_system,
        user = user,
        testsuite = testsuite,
        timestamp = generate_timestamp(),
        percent_complete = 0
    )
    evaluation.save()

    # create results for this evaluation
    for t in tests:
        result = Result(test = t, evaluation = evaluation, result = None) # 4 = no value yet
        result.save()

    # create category score entries for this evaluation
    categories = Category.objects.filter(testsuite = evaluation.testsuite)
    for cat in categories:
        score = Score(
            category = cat,
            percent_passed = 0,
            evaluation = evaluation
        )
        score.save()
    return evaluation

# return a dict {category: score, category: score, ...}
def get_category_scores(evaluation):
    top_level_categories = Category.objects.filter(testsuite = evaluation.testsuite, parent_category = None)
    retval = {}
    for cat in top_level_categories:
        # use the database object if it's available
        score = Score.objects.get(evaluation = evaluation, category = cat)
        retval[cat] = score.percent_passed
    return retval

def get_category_score(evaluation, category):
    results = get_results(evaluation, category)
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

    category_score = calculate_score(required, optional)
    return category_score

# return a percentage
def calculate_score(required, optional):
    total_applicable = required['pass'] + required['fail'] + optional['pass'] + optional['fail']
    total_passed = required['pass'] + optional['pass']
    # the total score is based on the number of applicable tests that passed
    if total_applicable != 0:
        total_score = (total_passed * 1.0) / (total_applicable * 1.0) * 100
        total_score = round(total_score, 1)
        return total_score
    else:
        return 0

def get_depth(item):
    if item.parent_category == None:
        return 0
    else:
        return get_depth(item.parent_category) + 1

def get_top_level_parent_category(item):
    if item.parent_category == None:
        return item
    else:
        return get_top_level_parent_category(item.parent_category)

def get_reading_system_evaluation_as_nested_categories(evaluation):
    top_level_categories = get_top_level_categories(evaluation.testsuite)
    summary = []
    for c in top_level_categories:
        summary.append(summarize(c, evaluation))
    return summary

# create a tree-like structure of categories and tests
def summarize(item, evaluation):
    if type(item) == Category:
        # append a category score property
        #item.category_score = get_category_score(evaluation, item)
        score = Score.objects.get(evaluation = evaluation, category = item)
        item.category_score = score.percent_passed
        subcats = Category.objects.filter(parent_category = item)
        subcat_summaries = []
        for c in subcats:
            subcat_summaries.append(summarize(c, evaluation))
        results = Result.objects.filter(test__parent_category = item, evaluation = evaluation)
        return {"item": item, "depth": get_depth(item), "subcategories": subcat_summaries, "results": results}

# for debugging
def print_item_summary(summary):
    prefix = "\t" * get_depth(summary['item'])
    print "{0}{1}".format(prefix, summary['item'].name.encode('utf-8'))

    for s in summary['subcategories']:
        print_item_summary(s)

    for r in summary['result']:
        print "{0}TEST {1}".format(prefix+"\t", r.name.encode('utf-8'))

# get all the tests in the given category (drill down through subcategories too)
def get_tests(category):
    tests = Test.objects.filter(parent_category = category)
    retval = []
    for t in tests:
        retval.append(t)
    subcats = Category.objects.filter(parent_category = category)
    for cat in subcats:
        retval.extend(get_tests(cat))
    return retval

def get_results(evaluation, category):
    tests = get_tests(category)
    results = []
    for t in tests:
        result = Result.objects.filter(test = t, evaluation = evaluation)[0]
        results.append(result)
    return results

def get_most_recent_testsuite():
    return TestSuite.objects.order_by("-version_date").order_by("-version_revision")[0]

def get_top_level_categories(testsuite):
    return Category.objects.filter(testsuite = testsuite, parent_category = None)

# decorate result objects in summary_data with their form equivalent
def mash_summary_data_with_form_data(summary_data, form_data):
    for s in summary_data['subcategories']:
        mash_summary_data_with_form_data(s, form_data)

    for r in summary_data['results']:
        r.form = find_form_for_object(r, form_data)

def find_form_for_object(obj, formset):
    for f in formset.forms:
        if f.instance == obj:
            return f
    return None


def get_complete_evaluations(rs):
    evals = Evaluation.objects.filter(reading_system = rs).order_by("-timestamp")
    retval = []
    for e in evals:
        if is_evaluation_complete(e) == True:
            retval.append(e)
    return retval

def get_incomplete_evaluations(rs):
    evals = Evaluation.objects.filter(reading_system = rs).order_by("-timestamp")
    retval = []
    for e in evals:
        if is_evaluation_complete(e) == False:
            retval.append(e)
    return retval

def get_public_evaluations(rs):
    evals = Evaluation.objects.filter(reading_system = rs, evaluation_type = "2").order_by("-timestamp")
    retval = []
    for e in evals:
       retval.append(e)
    return retval

def get_internal_evaluations(rs):
    evals = Evaluation.objects.filter(reading_system = rs, evaluation_type = "1").order_by("-timestamp")
    retval = []
    for e in evals:
        retval.append(e)
    return retval

def get_pct_complete(evaluation):
    all_results = Result.objects.filter(evaluation = evaluation)
    complete_results = Result.objects.filter(evaluation = evaluation).exclude(result = None)
    #print "Calculating percentage for {0}".format(evaluation.timestamp)
    #print "{0}/{1}".format(complete_results.count(), all_results.count())
    pct_complete = (complete_results.count() * 1.0) / (all_results.count() * 1.0) * 100.0
    return pct_complete

def generate_timestamp():
    return datetime.utcnow().replace(tzinfo=utc)

def calculate_and_save_scores(evaluation):
    categories = Category.objects.filter(testsuite = evaluation.testsuite)
    for cat in categories:
        score = Score.objects.get(evaluation = evaluation, category = cat)
        score.percent_passed = float_to_decimal(get_category_score(evaluation, cat))
        score.save()

# this is the "right way"...
# http://docs.python.org/release/2.6.7/library/decimal.html#decimal-faq
def float_to_decimal1(f):
    "Convert a floating point number to a Decimal with no loss of information"
    n, d = f.as_integer_ratio()
    numerator, denominator = Decimal(n), Decimal(d)
    ctx = Context(prec=60)
    result = ctx.divide(numerator, denominator)
    while ctx.flags[Inexact]:
        ctx.flags[Inexact] = False
        ctx.prec *= 2
        result = ctx.divide(numerator, denominator)
    return result

# and this is the way that works in practice
# note that the problem solved by either function is permanently solved in python 2.7+
# also note we are just calculating an approximate percentage (e.g. percent of form completed),
# and can live with a rounding error past 2 decimal places
def float_to_decimal(f):
    s = str(f)
    return Decimal(s)

