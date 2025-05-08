import json

from django import template
from django.forms import MultipleChoiceField

from webapp.models.section import WEEKDAY_CHOICES, SEASON_CHOICES

register = template.Library()

# Helper to map value to label
def get_label(value, choices):
    return dict(choices).get(value, value)

@register.filter
def format_schedule(schedule_json):
    if not schedule_json:
        return ""
    try:
        schedule = json.loads(schedule_json)
    except (TypeError, ValueError):
        return ""
    # Map days to their labels
    days = ', '.join(get_label(day, WEEKDAY_CHOICES) for day in schedule.get('days', []))
    start = schedule.get('start_time', 'N/A')
    end = schedule.get('end_time', 'N/A')
    # Map semester to its label
    semester = get_label(schedule.get('semester', ''), SEASON_CHOICES)
    year = schedule.get('year', '')
    return f"{days}, {start}-{end}, {semester} {year}"


@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter
def split(value, key):
    return value.split(key)

@register.filter
def is_multiplechoice(field):
    return isinstance(field.field, MultipleChoiceField)