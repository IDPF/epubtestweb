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

# @register.filter
# def is_test_supported(result_set, test):
#     result = result_set.get_result_for_test(test)
#     if result == None:
#         return False
#     if result.result == common.RESULT_SUPPORTED:
#         return True
#     else:
#         return False

@register.assignment_tag
def get_metadata(evaluation):
    return evaluation.get_metadata()

# @register.assignment_tag
# def is_test_supported(result):
#     if result == None:
#         return False
#     if result.result == common.RESULT_SUPPORTED:
#         return True
#     else:
#         return False


@register.assignment_tag
def get_score(evaluation, category_or_feature):
    score = evaluation.get_score(category_or_feature) 
    return score

# @register.assignment_tag
# def get_evaluations(reading_system, testsuite):
#     # gets only unarchived and published
#     return reading_system.get_evaluations(testsuite)

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


#######################
# for analytics
@register.assignment_tag
def get_enable_analytics():
    return settings.enable_analytics