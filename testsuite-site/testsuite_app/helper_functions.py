from models.category import Category
from models.score import Score
from models.result import Result
from models.reading_system import ReadingSystem
from models.test import Test

def get_public_scores(categories):
    "get the public evaluation scores for each reading system"
    retval = []
    reading_systems = ReadingSystem.objects.all()
    for rs in reading_systems:
        if rs.get_current_evaluation().evaluation_type == "1": #'internal'
            retval.append({"reading_system": rs, "scores": None})
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

def testsuite_to_dict(testsuite):
    "return a web template-friendly array of dicts describing categories and tests"
    top_level_categories = testsuite.get_top_level_categories()
    summary = []
    for c in top_level_categories:
        summary.append(category_to_dict(c))
    return summary

def category_to_dict(item):
    "return a nested structure of categories and tests."
    subcats = Category.objects.filter(parent_category = item)
    subcat_summaries = []
    for c in subcats:
        subcat_summaries.append(category_to_dict(c))
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


