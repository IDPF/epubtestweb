from django import template

register = template.Library()

# @register.inclusion_tag('_category.html')
# def category(category, result_set):
#     return {'category': category, "result_set": result_set}

# @register.inclusion_tag('_accessibility_category.html')
# def accessibility_category(category, result_set):
#     return {'category': category, "result_set": result_set}

# @register.inclusion_tag('_category_form.html')
# def category_form(category, result_set, results_form, flagged_items):
#     return {'category': category, "result_set": result_set, "results_form": results_form, 
#     "flagged_items": flagged_items}

# @register.inclusion_tag('_accessibility_category_form.html')
# def accessibility_category_form(category, result_set, results_form, flagged_items):
#     return {'category': category, "results_form": results_form, 
#     "flagged_items": flagged_items, 'result_set': result_set}


# # for the filter search
# @register.inclusion_tag('_category_compare_form.html')
# def category_compare_form(category):
#     return {'category': category}

# @register.inclusion_tag('_category_scores_list.html')
# def category_scores_list(categories, result_set):
#     return {'result_set': result_set, 'categories': categories}

# @register.inclusion_tag('_result.html')
# def result(result, show_required=True):
#     return {'result': result, 'show_required': show_required}

# @register.inclusion_tag('_result_form.html')
# def result_form(result, form, flagged_items, show_required = True):
#     return {'result': result, 'form': form, 'flagged_items': flagged_items, 'show_required': show_required}

@register.inclusion_tag('_alerts.html')
def alerts(alerts):
    return {"alerts": alerts}

# @register.inclusion_tag('_reading_system_details_list.html')
# def reading_system_details_list(rs, show_abridged = False):
#     return {"rs": rs, "show_abridged": show_abridged}

# @register.inclusion_tag('_manage_table.html')
# def manage_table(reading_systems, user):
#     return {"reading_systems": reading_systems, "user": user}
