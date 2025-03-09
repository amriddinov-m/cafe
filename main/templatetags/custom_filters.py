from django import template

register = template.Library()


@register.filter
def decimal_dot(value):
    """Преобразует десятичное число, заменяя запятую на точку."""
    try:
        return str(value).replace(',', '.')
    except (ValueError, TypeError):
        return 'Ошибка'


@register.filter
def item_update_quantity(value, _type):
    """Преобразует десятичное число, заменяя запятую на точку."""
    return value + 1 if _type == 'plus' else value - 1

