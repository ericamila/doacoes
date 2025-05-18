from django import template

register = template.Library()


@register.filter
def currency(value):
    try:
        value = float(value)
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "R$ 0,00"

# Filtros para adicionar atributos HTML aos campos de formulário
@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter
def add_no_required_class(field, css_class):
    return field.as_widget(attrs={"class": css_class, "required": False})

@register.filter
def add_disabled(field):
    return field.as_widget(attrs={"disabled": "disabled"})

@register.filter
def add_readonly(field):
    return field.as_widget(attrs={"readonly": "readonly"})

@register.filter
def add_focus(field):
    return field.as_widget(attrs={"autofocus": "autofocus"})

@register.filter
def add_style(field, style):
    return field.as_widget(attrs={"style": style})

# Filtros para remover atributos HTML dos campos de formulário
@register.filter
def remove_class(field, css_class):
    # Remove the specified class from the field's widget
    classes = field.field.widget.attrs.get("class", "").split()
    classes = [c for c in classes if c != css_class]
    return field.as_widget(attrs={"class": " ".join(classes)})

@register.filter
def remove_disabled(field):
    return field.as_widget(attrs={"disabled": False})

@register.filter
def remove_readonly(field):
    return field.as_widget(attrs={"readonly": False})

@register.filter
def remove_cursor_not_allowed(field):
    return field.as_widget(attrs={"style": "cursor: default; autofocus: true; caret-color: #3C3C3C;"})

@register.filter
def remove_style(field, style):
    # Remove the specified style from the field's widget
    styles = field.field.widget.attrs.get("style", "").split(";")
    styles = [s for s in styles if s.strip() != style.strip()]
    return field.as_widget(attrs={"style": "; ".join(styles)})

