from django import template
from testsuite_app import permissions
from testsuite_app.models import common
from testsuite import settings
from testsuite_app.models.result_set import ResultSet
from testsuite_app.models.score import AccessibilityScore

register = template.Library()


@register.assignment_tag

@register.assignment_tag
def get_result(test, result_set):
    return result_set.get_result_for_test(test)

@register.assignment_tag
def get_category_score(category, result_set):
    return result_set.get_category_score(category)

@register.assignment_tag
def get_overall_score(result_set):
    return result_set.get_total_score()

@register.assignment_tag
def get_form_for_result(result, result_forms):
    for f in result_forms.forms:
        if f.instance == result:
            return f
    return None

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
def get_default_result_set(reading_system):
    return reading_system.get_default_result_set()

@register.assignment_tag
def get_category_heading(category):
    "get the heading tag to use with this category"
    if category.depth >= 0 and category.depth <=4:
        return "h{0}".format(category.depth + 1)
    else:
        return "h6"

@register.assignment_tag
def get_unanswered_flagged_items(result_set):
    "get unanswered flagged item ids"
    tests = result_set.get_unanswered_flagged_tests()
    retval = []
    for t in tests:
        retval.append({"id": t.testid, "parentid": t.get_top_level_parent_category().id})
    return retval

@register.assignment_tag
def get_users_reading_systems(reading_systems, user):
    rses = []
    for rs in reading_systems:
        if user == rs.user:
            rses.append(rs)
    return rses

@register.assignment_tag
def get_metadata(result_set):
    return result_set.get_metadata()

@register.assignment_tag
def is_test_supported(result):
    if result == None:
        return False
    if result.result == common.RESULT_SUPPORTED:
        return True
    else:
        return False

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