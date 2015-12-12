from django import template

from testsuite_app.models import *

register = template.Library()

@register.filter
def get_display_name(user):
    if (user.first_name != None and user.first_name != "") and \
        (user.last_name != None and user.last_name != ""):
        return "{0} {1}".format(user.first_name, user.last_name)
    else:
        return user.username


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
        return "Not Tested"

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
def get_AT_metadata_description(meta):
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
def get_AT_metadata_notes(evaluation):
    meta = evaluation.get_metadata()
    return meta.notes


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

@register.filter
def get_reading_system_display_name(reading_system):
    rsname = reading_system.name
    rsvers = reading_system.version
    osname = reading_system.operating_system
    osvers = reading_system.operating_system_version

    if rsname == None:
        rsname = ""
    if rsvers == None:
        rsvers = ""
    if osname == None:
        osname = ""
    if osvers == None:
        osvers = ""
    
    s = "{0} v {1} ({2} {3})".format(rsname, rsvers, osname, osvers)
    return s
