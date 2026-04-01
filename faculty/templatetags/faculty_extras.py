from django import template

register = template.Library()

COLORS = [
    '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e',
    '#e74a3b', '#6f42c1', '#fd7e14', '#20c997',
]

@register.filter
def lookup(d, key):
    """Access dict by variable key: {{ mydict|lookup:variable }}"""
    try:
        return d[key]
    except (KeyError, TypeError):
        return []

@register.filter
def is_in(value, collection):
    """Check if value is in a set/list: {{ slot|is_in:day_occ }}"""
    try:
        return value in collection
    except TypeError:
        return False

@register.filter
def subject_color(pk):
    """Return a consistent hex color for a subject based on its pk."""
    try:
        return COLORS[int(pk) % len(COLORS)]
    except (TypeError, ValueError):
        return COLORS[0]
