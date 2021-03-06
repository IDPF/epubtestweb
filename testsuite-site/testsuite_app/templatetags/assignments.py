import os

from django import template

from testsuite_app import permissions
from testsuite import settings
from testsuite_app.models import *

register = template.Library()

@register.assignment_tag
def get_result(test, evaluation):
    if evaluation == None:
        return None
    return evaluation.get_result_for_test(test)

@register.assignment_tag
def get_metadata(evaluation):
    return evaluation.get_metadata()

@register.assignment_tag
def get_score(evaluation, category_or_feature):
    score = evaluation.get_score(category_or_feature)
    return score

@register.assignment_tag
def get_all_evaluations(reading_system, testsuite):
    # regardless of whether they are archived/published
    return reading_system.get_all_evaluations(testsuite)

@register.assignment_tag
def get_form_for_result(result, result_formset):
    for f in result_formset.forms:
        if f.instance == result:
            return f
    return None

@register.assignment_tag
def get_site_last_updated():
    most_recent_evaluation_date = Evaluation.objects.all().order_by("-last_updated").first().last_updated
    most_recent_testsuite_date = TestSuite.objects.all().order_by("-version_date").first().version_date

    if most_recent_evaluation_date > most_recent_testsuite_date:
        return most_recent_evaluation_date
    else:
        return most_recent_testsuite_date

@register.assignment_tag
def is_readonly():
    return settings.readonly

@register.assignment_tag
def has_supercategories(categories):
    for cat in categories:
        if cat.super_category != "":
            return True
    return False

@register.assignment_tag
def get_supercategories(categories):
    supercats = [] # using this because dictionaries aren't ordered
    for cat in categories:
        # is this already in our list? we want uniqueness, no duplicates. so if it's there already, just increment the 'value' field.
        if any(x['name'] == cat.super_category for x in supercats):
            supercat = next(sc for sc in supercats if sc['name'] == cat.super_category)
            supercat['value'] = supercat['value'] + 1
        else:
            supercats.append({'name': cat.super_category, 'value': 1})
    return supercats

#######################
# for analytics
@register.assignment_tag
def is_using_analytics():
    return settings.enable_analytics
