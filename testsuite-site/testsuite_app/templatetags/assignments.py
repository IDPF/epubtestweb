from django import template
from testsuite_app import permissions
from testsuite_app.models import common
from testsuite import settings
from testsuite_app.models.evaluation import Evaluation
from testsuite_app.models.score import Score
from testsuite_app import helper_functions
import os

register = template.Library()


@register.assignment_tag

@register.assignment_tag
def get_result(test, evaluation):
    if evaluation == None:
        return None
    return evaluation.get_result_for_test(test)

@register.filter
def is_test_supported(result_set, test):
    result = result_set.get_result_for_test(test)
    if result == None:
        return False
    if result.result == common.RESULT_SUPPORTED:
        return True
    else:
        return False

@register.assignment_tag
def get_metadata(evaluation):
    return evaluation.get_metadata()

@register.assignment_tag
def is_test_supported(result):
    if result == None:
        return False
    if result.result == common.RESULT_SUPPORTED:
        return True
    else:
        return False

@register.assignment_tag
def is_reading_system_archived(reading_system):
    return reading_system.status == common.READING_SYSTEM_STATUS_TYPE_ARCHIVED

######################
# new stuff

@register.assignment_tag
def get_score(evaluation, category_or_feature):
    score = evaluation.get_score(category_or_feature) 
    print("score: {}".format(score.percent))
    return score

@register.assignment_tag
def get_composite_score(evaluations, category_or_feature):
    for evaluation in evaluations:
        score = evaluation.get_score(category_or_feature)
        if score.did_any_pass == True:
            return "See details"
    return "Not supported"


@register.assignment_tag
def get_evaluations(reading_system, testsuite):
    reading_system_version = reading_system.get_most_recent_version_with_evaluation(testsuite)
    return reading_system_version.get_evaluations(testsuite)

@register.assignment_tag
def get_evaluation(reading_system, testsuite):
    evaluations = get_evaluations(reading_system, testsuite)
    if evaluations.count() > 0:
        return evaluations[0]
    return None

####################
# permissions
@register.assignment_tag
def user_can_edit(user, reading_system):
    return permissions.user_can_edit_reading_system(user, reading_system)

@register.assignment_tag
def user_can_view(user, reading_system, context):
    return permissions.user_can_view_reading_system(user, reading_system, context)

@register.assignment_tag
def user_can_change_rs_visibility(user, rs, new_visibility):
    return permissions.user_can_change_reading_system_visibility(user, rs, new_visibility)

@register.assignment_tag
def user_can_change_result_set_visibility(user, result_set, new_visibility):
    return permissions.user_can_change_result_set_visibility(user, result_set, new_visibility)

@register.assignment_tag
def user_can_manage_accessibility(user, reading_system):
    return permissions.user_can_create_accessibility_result_set(user, reading_system)

@register.assignment_tag
def user_can_edit_accessibility_eval(user, result_set):
    return permissions.user_can_edit_accessibility_result_set(user, result_set)

#######################
# for analytics
@register.assignment_tag
def get_enable_analytics():
    return settings.enable_analytics