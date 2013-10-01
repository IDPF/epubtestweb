from models.category import Category
from models.score import Score
from models.result import Result
from models.reading_system import ReadingSystem

def find_form_for_object(obj, formset):
    "Given a set of forms, find the one for the given object"
    for f in formset.forms:
        if f.instance == obj:
            return f
    return None

def mash_summary_data_with_form_data(summary_data, form_data):
    "annotate result objects in summary_data with their form equivalent"
    for s in summary_data['subcategories']:
        mash_summary_data_with_form_data(s, form_data)

    for r in summary_data['results']:
        r.form = find_form_for_object(r, form_data)

def get_public_scores(categories):
    "get the public evaluation scores for each reading system"
    retval = []
    reading_systems = ReadingSystem.objects.all()
    for rs in reading_systems:
        if rs.get_current_evaluation().evaluation_type == "1": #'internal'
            retval.append({"reading_system": rs, "scores": None})
        else:
            scores = rs.get_current_evaluation().get_top_level_category_scores()
            # scores should have the same order as categories
            ordered_scores = []
            for cat in categories:
                ordered_scores.append(scores[cat])
            retval.append({"reading_system": rs, "scores": ordered_scores})
    return retval

def get_results_as_nested_categories(reading_system):
    "Return a web template-friendly array of dicts describing categorized reading system results."
    top_level_categories = reading_system.get_current_evaluation().testsuite.get_top_level_categories()
    summary = []
    for c in top_level_categories:
        summary.append(summarize(c, reading_system.get_current_evaluation()))
    return summary

def summarize(item, evaluation):
    "Return a nested structure of categories and tests. item is a category or test."
    if type(item) == Category:
        score = Score.objects.get(category = item, evaluation = evaluation)
        subcats = Category.objects.filter(parent_category = item)
        subcat_summaries = []
        for c in subcats:
            subcat_summaries.append(summarize(c, evaluation))
        results = Result.objects.filter(test__parent_category = item, evaluation = evaluation)
        return {"item": item, "depth": item.get_depth(), "subcategories": subcat_summaries,
            "results": results, "category_score": score.percent_passed}

def print_item_summary(summary):
    "Debug-print the summary data generated above."
    prefix = "\t" * summary['item'].get_depth()
    print "{0}{1}".format(prefix, summary['item'].name.encode('utf-8'))

    for s in summary['subcategories']:
        print_item_summary(s)

    for r in summary['results']:
        print "{0}TEST {1}".format(prefix+"\t", r.test.name.encode('utf-8'))


