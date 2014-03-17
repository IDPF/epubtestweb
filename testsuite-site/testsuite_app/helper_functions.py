from models.category import Category
from models.score import Score
from models.result import Result
from models.reading_system import ReadingSystem
from models.test import Test, TestMetadata
from models.testsuite import TestSuite
import os
from testsuite import settings
from models import common

def get_public_scores(categories):
    "get the public evaluation scores for each reading system"
    retval = []
    reading_systems = ReadingSystem.objects.all()
    for rs in reading_systems:
        if rs.visibility == common.VISIBILITY_PUBLIC:
            evaluation = rs.get_current_evaluation()
            ts = TestSuite.objects.get_most_recent_testsuite_of_type(common.TESTSUITE_TYPE_DEFAULT)
            scores = evaluation.get_top_level_category_scores(ts)
            # make sure scores have the same order as the categories
            ordered_scores = []
            for cat in categories:
                ordered_scores.append(scores[cat])
            accessibility_score = calculate_accessibility_score(rs)
            accessibility_boolean = has_any_accessibility(accessibility_score)
            retval.append({"reading_system": rs, "total_score": evaluation.get_total_score(),
                "category_scores": ordered_scores, "accessibility_score": accessibility_score, "accessibility": accessibility_boolean})
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
    print "{0}{1}".format(prefix, summary['item'].name.encode('utf-8'))

    for s in summary['subcategories']:
        print_item_summary(s)

    for r in summary['tests']:
        print "{0}TEST {1}".format(prefix+"\t", r.test.name.encode('utf-8'))

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
	print "not found {0}".format(dirname)
	return None    


# TODO expand to support more than one accessibility evaluation
def calculate_accessibility_score(rs):
    result_set = rs.get_current_evaluation().get_accessibility_result_set()
    if result_set == None:
        return {"visual_adj": 0.0, "keyboard": 0.0, "mouse": 0.0, "touch": 0.0, "screenreader": 0.0}
    # use the most recent accessibility testsuite
    ts = TestSuite.objects.get_most_recent_testsuite_of_type(common.TESTSUITE_TYPE_ACCESSIBILITY)
    top_level_cats = ts.get_top_level_categories()

    visual_adj_tests = []
    # hackishly using this to indicate the visual_adjustments category
    visual_adj_cat = Category.objects.filter(testsuite = ts, temp_flag = True)[0]
    visual_adj_tests = visual_adj_cat.get_tests()
        
    keyboard_tests = []
    keyboard_test_meta = TestMetadata.objects.filter(access_type = common.ACCESS_TYPE_KEYBOARD)
    for m in keyboard_test_meta:
        keyboard_tests.append(m.test)

    mouse_tests = []
    mouse_test_meta = TestMetadata.objects.filter(access_type = common.ACCESS_TYPE_MOUSE)
    for m in mouse_test_meta:
        mouse_tests.append(m.test)

    touch_tests = []
    touch_test_meta = TestMetadata.objects.filter(access_type = common.ACCESS_TYPE_TOUCH)
    for m in touch_test_meta:
        touch_tests.append(m.test)

    screenreader_tests = []
    screenreader_test_meta = TestMetadata.objects.filter(access_type = common.ACCESS_TYPE_SCREENREADER)
    for m in screenreader_test_meta:
        screenreader_tests.append(m.test)
    
    score = {}
    score['visual_adj'] = calculate_score(visual_adj_tests, result_set)
    score['keyboard'] = calculate_score(keyboard_tests, result_set)
    score['mouse'] = calculate_score(mouse_tests, result_set)
    score['touch'] = calculate_score(touch_tests, result_set)
    score['screenreader'] = calculate_score(screenreader_tests, result_set)
    return score

# tests is an array
def calculate_score(tests, result_set):
    total = len(tests)
    passed = 0
    for t in tests:
        result = result_set.evaluation.get_result(t, result_set)
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




def has_any_accessibility(accessibility_score):
    # if a reader fails in all of screenreader, braille disp, & visual adj ==> inaccessible
    # if it passes in any of the above ==> accessible
    # TODO add braille once we have test(s) for it
    if accessibility_score['visual_adj'] > 0.0 or accessibility_score['screenreader'] > 0.0:
        return True
    else:
        return False 
