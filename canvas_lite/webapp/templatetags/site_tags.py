from django import template

register = template.Library()

@register.filter
def format_schedule(schedule):
    return (
        f"{', '.join(schedule.get('days', []))}, "
        f"{schedule.get('start_time', 'N/A')}-{schedule.get('end_time', 'N/A')}, "
        f"{schedule.get('semester', '')} {schedule.get('year', '')}"
    )

@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()