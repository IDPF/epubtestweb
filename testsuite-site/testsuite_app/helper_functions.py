from .models.category import Category
from .models.score import Score
from .models.result import Result
from .models.reading_system import ReadingSystemVersion
from .models.test import Test, TestMetadata
from .models.testsuite import TestSuite
import os
from testsuite import settings
from .models import common

def get_public_scores(categories, rs_status):
    "get the public scores for each reading system"
    "rs_status is an enum from common.py and indicates whether we want archived or current reading systems"
    retval = []

    reading_systems = ReadingSystemVersion.objects.filter(status = rs_status)
    for rs in reading_systems:
        if rs.visibility == common.VISIBILITY_PUBLIC:
            result_set = rs.get_default_result_set()
            ts = TestSuite.objects.get_most_recent_testsuite()
            ordered_scores = []
            if result_set != None:
                scores = result_set.get_top_level_category_scores(ts)
                # make sure scores have the same order as the categories
                
                for cat in categories:
                    ordered_scores.append(scores[cat])
            
            accessibility_score = has_any_accessibility(rs)
            total_score = 0.0
            if result_set != None:
                total_score = result_set.get_total_score()
            retval.append({"reading_system": rs, "total_score": total_score,
                "category_scores": ordered_scores, "accessibility": accessibility_score})
    return retval

def testsuite_to_dict(testsuite, test_filter_ids = []):
    "return a web template-friendly array of dicts describing categories and tests"
    top_level_categories = testsuite.get_top_level_categories()
    summary = []
    for c in top_level_categories:
        summary.append(category_to_dict(c))
    return summary

def category_to_dict(item, test_filter_ids = []):
    "return a nested structure of categories and tests."
    subcats = Category.objects.filter(parent_category = item)
    subcat_summaries = []
    for c in subcats:
        subcat_summaries.append(category_to_dict(c))
    tests = None
    # if we are filtering for specific test IDs, then just include those
    if len(test_filter_ids) != 0:
        tests = Test.objects.filter(parent_category = item, pk__in=test_filter_ids)
    else:
        tests = Test.objects.filter(parent_category = item)

    return {"item": item, "subcategories": subcat_summaries, "tests": tests}

def print_item_dict(summary):
    "Debug-print the summary data generated above."
    prefix = "\t" * summary['item'].depth
    print("{0}{1}".format(prefix, summary['item'].name.encode('utf-8')))

    for s in summary['subcategories']:
        print_item_summary(s)

    for r in summary['tests']:
        print("{0}TEST {1}".format(prefix+"\t", r.test.name.encode('utf-8')))

def calculate_source(dirname):
	# given the directory name of the source epub, get the filename in the build directory
	files = os.listdir(settings.EPUB_ROOT)

	for f in sorted(files):

		if f.find(dirname) != -1:
			filename = os.path.basename(f)
			# TODO duplicate code from views.py TestsuiteView
			link = "{0}{1}".format(settings.EPUB_URL, filename)
			doc_number = f[12:len(f)-14]
			dl = {"label": "Document {0}".format(doc_number), "link": link}
			return dl
	print("not found {0}".format(dirname))
	return None    


# tests is an array
def calculate_score(tests, result_set):
    total = len(tests)
    passed = 0
    for t in tests:
        result = result_set.get_result_for_test(t)
        if result.result == common.RESULT_SUPPORTED:
            passed += 1
    if total == 0: 
        return 0.0
    # not using percentages...but if we were:
    # pct = (passed * 1.0) / (total * 1.0) * 100.00
    # return "%.2f" % pct
    if total == 100:
        return "Pass"
    if total == 0:
        return "Fail"
    return "Partial support"

def has_any_accessibility(rs):
    # return values: 0 = fail; -1 = no accessible evals available, 1 = some accessibility support
    result_sets = rs.get_accessibility_result_sets()
    public_result_sets = []
    for rset in result_sets:
        if rset.visibility == common.VISIBILITY_PUBLIC:
            public_result_sets.append(rset)
    if len(public_result_sets) == 0:
        return -1    
    
    for result_set in public_result_sets:
        score = result_set.get_total_score()
        if score.pct_total_passed > 0:
                return 1
    return 0

def generate_timestamp():
    from datetime import datetime
    from django.utils.timezone import utc
    return datetime.utcnow().replace(tzinfo=utc)

def get_epubs_from_latest_testsuites():
    default_epubs = Category.objects.filter(category_type = common.CATEGORY_EPUB, testsuite = TestSuite.objects.get_most_recent_testsuite())
    accessibility_epubs = Category.objects.filter(category_type = common.CATEGORY_EPUB, testsuite = TestSuite.objects.get_most_recent_accessibility_testsuite())
    # merge two query sets with "|"
    return default_epubs | accessibility_epubs

def force_score_refresh():
    from testsuite_app.models.evaluation import Evaluation
    evaluations = Evaluation.objects.all()
    for evaluation in evaluations:
        evaluation.update_scores()


