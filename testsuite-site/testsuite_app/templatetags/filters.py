from django import template
from testsuite_app import permissions
from testsuite_app.models import common
from testsuite import settings
from testsuite_app.models.result_set import ResultSet
from testsuite_app.models.score import AccessibilityScore

register = template.Library()

@register.filter
def get_display_name(user):
    if (user.first_name != None and user.first_name != "") and \
        (user.last_name != None and user.last_name != ""):
        return "{0} {1}".format(user.first_name, user.last_name)
    else:
        return user.username

@register.filter
def get_visibility(rs):
    print rs.visibility
    vis = rs.visibility
    if vis == common.VISIBILITY_MEMBERS_ONLY:
		return "members-only"
    elif vis == common.VISIBILITY_PUBLIC:
		return "public"
    elif vis == common.VISIBILITY_OWNER_ONLY:
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
    if result == None:
        return "-"
    if result.result == common.RESULT_SUPPORTED:
        return "Supported"
    elif result.result == common.RESULT_NOT_SUPPORTED:
        return "Not Supported"
    elif result.result == common.RESULT_NOT_APPLICABLE:
        return "N/A"
    else:
        return "-"

@register.filter
def get_result_class(result, is_form):
    if result == None:
        return ""
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
def get_AT_metadata_description(result_set):
    meta = result_set.get_metadata()
    modalities = []
    if meta.input_type == common.INPUT_TYPE_KEYBOARD:
        modalities.append("Keyboard")
    if meta.input_type == common.INPUT_TYPE_MOUSE:
        modalities.append("Mouse")
    if meta.input_type == common.INPUT_TYPE_TOUCH:
        modalities.append("Touch/Gestures")
    if meta.supports_screenreader:
        modalities.append("Screenreader/Self-voicing")
    if meta.supports_braille:
        modalities.append("Braille")

    s = ", ".join(modalities)
    return s

@register.filter
def print_tested_not_tested(bool_value):
    if bool_value == True:
        return "Tested"
    else:
        return "Not tested"

@register.filter
def print_input_type(metadata):
    if metadata == None:
        return ""
    if metadata.input_type == common.INPUT_TYPE_TOUCH:
        return "Touch/Gestures"
    if metadata.input_type == common.INPUT_TYPE_KEYBOARD:
        return "Keyboard"
    if metadata.input_type == common.INPUT_TYPE_MOUSE:
        return "Mouse"


