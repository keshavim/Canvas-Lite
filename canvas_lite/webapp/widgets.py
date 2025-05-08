from datetime import datetime

from django import forms
import json

from webapp.models.section import WEEKDAY_CHOICES, SEASON_CHOICES


class ScheduleWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        current_year = datetime.now().year
        widgets = [
            forms.CheckboxSelectMultiple(choices=WEEKDAY_CHOICES),
            forms.TimeInput(attrs={'placeholder': 'Start Time', 'type': 'time'}),
            forms.TimeInput(attrs={'placeholder': 'End Time', 'type': 'time'}),
            forms.Select(choices=SEASON_CHOICES, attrs={'placeholder': 'Semester'}),
            forms.NumberInput(attrs={'placeholder': 'Year', 'value':current_year}),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            try:
                data = json.loads(value)
                return [
                    data.get('days', []),
                    data.get('start_time'),
                    data.get('end_time'),
                    data.get('semester'),
                    data.get('year'),
                ]
            except Exception:
                pass
        return [[], None, None, None, None]

class ScheduleField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = [
            forms.MultipleChoiceField(choices=WEEKDAY_CHOICES, required=False),
            forms.TimeField(required=False),
            forms.TimeField(required=False),
            forms.ChoiceField(choices=SEASON_CHOICES, required=False),
            forms.IntegerField(required=False),
        ]
        super().__init__(fields, require_all_fields=False, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return json.dumps({
                'days': data_list[0],
                'start_time': data_list[1].strftime('%H:%M') if data_list[1] else None,
                'end_time': data_list[2].strftime('%H:%M') if data_list[2] else None,
                'semester': data_list[3],
                'year': data_list[4],
            })
        return None
