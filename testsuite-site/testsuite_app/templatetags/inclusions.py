from django import template

register = template.Library()

@register.inclusion_tag('_alerts.html')
def alerts(alerts):
    return {"alerts": alerts}
