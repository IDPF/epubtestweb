from models import *

def find_form_for_object(obj, formset):
    for f in formset.forms:
        if f.instance == obj:
            return f
    return None

# decorate result objects in summary_data with their form equivalent
def mash_summary_data_with_form_data(summary_data, form_data):
    for s in summary_data['subcategories']:
        mash_summary_data_with_form_data(s, form_data)

    for r in summary_data['results']:
        r.form = find_form_for_object(r, form_data)

# get the most recent scores for each reading system
def get_scores(categories):
    retval = []
    reading_systems = ReadingSystem.objects.all()
    for rs in reading_systems:
        evaluation = rs.get_most_recent_evaluation()
        if evaluation is None:
            retval.append({"reading_system": rs, "scores": None})
        else:
            scores = evaluation.get_top_level_category_scores()
            # scores should have the same order as categories
            ordered_scores = []
            for cat in categories:
                ordered_scores.append(scores[cat])
            retval.append({"reading_system": rs, "scores": ordered_scores})
    return retval

def get_most_recent_testsuite():
    return TestSuite.objects.order_by("-version_date").order_by("-version_revision")[0]

def generate_timestamp():
    return datetime.utcnow().replace(tzinfo=utc)




