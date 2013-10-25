from models.category import Category
from models.score import Score
from models.result import Result
from models.reading_system import ReadingSystem
from models.test import Test
import os
from testsuite import settings

def get_public_scores(categories):
    "get the public evaluation scores for each reading system"
    retval = []
    reading_systems = ReadingSystem.objects.all()
    for rs in reading_systems:
        if rs.get_current_evaluation().evaluation_type == "1": #'internal'
            retval.append({"reading_system": rs, "total_score": 0, "category_scores": None})
        else:
            evaluation = rs.get_current_evaluation()
            scores = evaluation.get_top_level_category_scores()
            # make sure scores have the same order as the categories
            ordered_scores = []
            for cat in categories:
                ordered_scores.append(scores[cat])
            retval.append({"reading_system": rs, "total_score": evaluation.get_total_score(),
                "category_scores": ordered_scores})
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

    return {"item": item, "depth": item.get_depth(), "subcategories": subcat_summaries,
        "tests": tests}

def print_item_dict(summary):
    "Debug-print the summary data generated above."
    prefix = "\t" * summary['item'].get_depth()
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

