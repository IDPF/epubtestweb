from django import template

register = template.Library()

# for the reading system and evaluation form
@register.inclusion_tag('frag_category.html')
def category(category, evaluation, is_form, results_form):
	return {'category': category, "evaluation": evaluation, "is_form": is_form,
		"results_form": results_form}

# for the filter search
@register.inclusion_tag('frag_category_filter.html')
def category_filter(category):
	return {'category': category}

@register.inclusion_tag('frag_category_scores_as_dl_items.html')
def category_scores_as_dl_items(categories, evaluation):
	return {'evaluation': evaluation, 'categories': categories}

@register.inclusion_tag('frag_result.html')
def result(result, is_form, result_form):
    return {'result': result, "is_form": is_form, "result_form": result_form}

@register.inclusion_tag('frag_alerts.html')
def alerts(alerts):
    return {"alerts": alerts}

@register.inclusion_tag('frag_rs.html')
def reading_system(rs):
	return {"rs": rs}

@register.assignment_tag
def get_current_evaluation(rs):
    return rs.get_current_evaluation()

@register.assignment_tag
def get_result(test, evaluation):
	return evaluation.get_result_by_testid(test.testid)

@register.assignment_tag
def get_category_score(category, evaluation):
	return evaluation.get_category_score(category)

@register.assignment_tag
def get_current_evaluation(reading_system):
	return reading_system.get_current_evaluation()

@register.assignment_tag
def get_category_depth(category):
	return category.get_depth()

@register.assignment_tag
def get_form_for_result(result, result_forms):
	for f in result_forms.forms:
		if f.instance == result:
			return f
	return None

@register.assignment_tag
def has_public_evaluation(reading_system):
	evaluation = reading_system.get_current_evaluation()
	if evaluation.evaluation_type == "2": #public
		return True
	else:
		return False

@register.assignment_tag
def is_test_supported(reading_system, test):
	evaluation = reading_system.get_current_evaluation()
	result = evaluation.get_result(test)
	if result == None:
		return False
	if result.result == "1":
		return True
	else:
		return False

@register.filter
def get_status(rs):
	eval_type = ""
	evaluation = rs.get_current_evaluation()
	if evaluation.evaluation_type == "1":
		eval_type = "Internal"
	else:
		eval_type = "Public"

	return "{0}, {1}% complete.".format(eval_type, evaluation.percent_complete)

@register.filter
def get_parent_ids(item):
	"get a space-separated list of parent category IDs. item is a category or test."
	idarr = []
	parents = item.get_parents()
	for p in parents:
		idarr.append("id-{0}".format(str(p.id)))

	return " ".join(idarr)