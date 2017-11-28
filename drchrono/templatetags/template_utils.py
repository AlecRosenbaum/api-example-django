from django import template
register = template.Library()


@register.filter(name='addcss')
def addcss(field, css):
    if "class" in field.field.widget.attrs:
        return field.as_widget(attrs={"class": "{} {}".format(field.field.widget.attrs['class'], css)})
    else:
        return field.as_widget(attrs={"class": css})
