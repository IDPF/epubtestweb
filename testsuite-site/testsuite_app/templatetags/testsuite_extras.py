from django import template
from testsuite_app import permissions
from testsuite_app.models import common
from testsuite import settings

register = template.Library()

@register.inclusion_tag('_category.html')
def category(category, evaluation):
	return {'category': category, "evaluation": evaluation}

@register.inclusion_tag('_accessibility_category.html')
def accessibility_category(category, evaluation, result_set):
    return {'category': category, "evaluation": evaluation, "result_set": result_set}

@register.inclusion_tag('_category_form.html')
def category_form(category, evaluation, results_form, flagged_items):
    return {'category': category, "evaluation": evaluation, "results_form": results_form, 
    "flagged_items": flagged_items}

@register.inclusion_tag('_accessibility_category_form.html')
def accessibility_category_form(category, evaluation, results_form, flagged_items, result_set):
    return {'category': category, "evaluation": evaluation, "results_form": results_form, 
    "flagged_items": flagged_items, 'result_set': result_set}


# for the filter search
@register.inclusion_tag('_category_compare_form.html')
def category_compare_form(category):
	return {'category': category}

@register.inclusion_tag('_category_scores_list.html')
def category_scores_list(categories, evaluation):
	return {'evaluation': evaluation, 'categories': categories}

@register.inclusion_tag('_result.html')
def result(result, show_required=True):
    return {'result': result, 'show_required': show_required}

@register.inclusion_tag('_result_form.html')
def result_form(result, form, flagged_items, show_required = True):
    return {'result': result, 'form': form, 'flagged_items': flagged_items, 'show_required': show_required}

@register.inclusion_tag('_alerts.html')
def alerts(alerts):
    return {"alerts": alerts}

@register.inclusion_tag('_reading_system_details_list.html')
def reading_system_details_list(rs):
	return {"rs": rs}

@register.inclusion_tag('_manage_table.html')
def manage_table(reading_systems, user):
    return {"reading_systems": reading_systems, "user": user}

@register.assignment_tag
def get_current_evaluation(rs):
    return rs.get_current_evaluation()

@register.assignment_tag
def get_result_for_default_set(test, evaluation):
    result_set = evaluation.get_default_result_set()
    return evaluation.get_result_by_testid(test.testid, result_set)

@register.assignment_tag
def get_result_for_result_set(test, evaluation, result_set):
    result = evaluation.get_result_by_testid(test.testid, result_set)
    return result

@register.assignment_tag
def get_category_score(category, evaluation):
	return evaluation.get_category_score(category)

@register.assignment_tag
def get_current_evaluation(reading_system):
	return reading_system.get_current_evaluation()

@register.assignment_tag
def get_form_for_result(result, result_forms):
	for f in result_forms.forms:
		if f.instance == result:
			return f
	return None

@register.assignment_tag
def is_test_supported_for_default_set(reading_system, test):
	evaluation = reading_system.get_current_evaluation()
	result = evaluation.get_result(test, evaluation.get_default_result_set())
	if result == None:
		return False
	if result.result == common.RESULT_SUPPORTED:
		return True
	else:
		return False

@register.assignment_tag
def is_test_supported_for_result_set(reading_system, test, result_set):
    evaluation = reading_system.get_current_evaluation()
    result = evaluation.get_result(test, result_set)
    if result == None:
        return False
    if result.result == common.RESULT_SUPPORTED:
        return True
    else:
        return False


@register.assignment_tag
def user_can_edit(user, reading_system):
    return permissions.user_can_edit_reading_system(user, reading_system)

@register.assignment_tag
def user_can_view(user, reading_system, context):
	return permissions.user_can_view_reading_system(user, reading_system, context)

@register.assignment_tag
def user_can_change_visibility(user, reading_system, new_visibility):
	return permissions.user_can_change_visibility(user, reading_system, new_visibility)

@register.assignment_tag
def get_category_heading(category):
    "get the heading tag to use with this category"
    if category.depth >= 0 and category.depth <=4:
        return "h{0}".format(category.depth + 1)
    else:
        return "h6"

@register.assignment_tag
def get_unanswered_flagged_items_in_default_set(evaluation):
    "get unanswered flagged item ids"
    tests = evaluation.get_unanswered_flagged_items(evaluation.get_default_result_set())
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
def get_enable_analytics():
    return settings.enable_analytics

@register.filter
def get_display_name(user):
    if (user.first_name != None and user.first_name != "") or \
        (user.last_name != None and user.last_name != ""):
        return "{0} {1}".format(user.first_name, user.last_name)
    else:
        return user.username

@register.filter
def get_visibility(rs):
	if rs.visibility == common.VISIBILITY_MEMBERS_ONLY:
		return "members-only"
	elif rs.visibility == common.VISIBILITY_PUBLIC:
		return "public"
	elif rs.visibility == common.VISIBILITY_OWNER_ONLY:
		return "owner-only"
	else:
		return "not recognized"

@register.filter
def get_parent_ids(item):
	"get a space-separated list of parent category IDs. item is a category or test."
	idarr = []
	parents = item.get_parents()
	for p in parents:
		idarr.append("id-{0}".format(str(p.id)))

	return " ".join(idarr)

@register.filter
def get_result_description(result):
    if result.result == common.RESULT_SUPPORTED:
        return "Supported"
    elif result.result == common.RESULT_NOT_SUPPORTED:
        return "Not Supported"
    else:
        return "-"

@register.filter
def get_result_class(result, is_form):
    if is_form:
        if result.result == common.RESULT_NOT_ANSWERED:
            return "warning"
    else:
        if result.result == common.RESULT_SUPPORTED:
            return "success"
        elif result.result == common.RESULT_NOT_SUPPORTED:
            return "danger"
    return "" # default


@register.filter
def get_AT_metadata_description(evaluation):
    meta = evaluation.get_accessibility_result_set().metadata
    modalities = []
    if meta.is_keyboard:
        modalities.append("Keyboard")
    if meta.is_mouse:
        modalities.append("Mouse")
    if meta.is_touch:
        modalities.append("Touch/Gestures")
    if meta.is_screenreader:
        modalities.append("Screenreader/Self-voicing")
    if meta.is_braille:
        modalities.append("Braille")

    s = ", ".join(modalities)
    return s
