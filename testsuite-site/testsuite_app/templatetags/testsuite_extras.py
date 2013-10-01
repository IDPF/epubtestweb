from django import template

register = template.Library()

@register.inclusion_tag('frag_category.html')
def category(category, is_form):
    return {'category': category, "is_form": is_form}

@register.inclusion_tag('frag_result.html')
def result(result, is_form):
    return {'result': result, "is_form": is_form}

@register.inclusion_tag('frag_alerts.html')
def alerts(alerts):
    return {"alerts": alerts}

@register.inclusion_tag('frag_rs.html')
def reading_system(rs):
	return {"rs": rs}

@register.assignment_tag
def current_evaluation(rs):
    return rs.get_current_evaluation()

@register.filter
def get_status(rs):
	eval_type = ""
	evaluation = rs.get_current_evaluation()
	if evaluation.evaluation_type == "1":
		eval_type = "Internal"
	else:
		eval_type = "Public"

	return "{0}, {1}% complete.".format(eval_type, evaluation.percent_complete)