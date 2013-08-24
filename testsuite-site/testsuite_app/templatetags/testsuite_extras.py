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
