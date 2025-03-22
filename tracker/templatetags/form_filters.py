from django import template

register = template.Library()

@register.filter
def addattr(field, attr):
    """Add an attribute to a form field"""
    try:
        attr_name, attr_value = attr.split(':')
        attrs = field.field.widget.attrs.copy()
        attrs[attr_name] = attr_value
        return field.as_widget(attrs=attrs)
    except ValueError:
        return field