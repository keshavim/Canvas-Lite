from django.forms import TextInput, MultiWidget, TimeInput
import json

from django.forms.widgets import NumberInput, CheckboxSelectMultiple, Select, SelectMultiple

from webapp.models.section import SEASON_CHOICES, WEEKDAY_CHOICES


class SingleSelect(Select):
    def __init__(self, choices, attrs=None):
        super().__init__(attrs)
        self.choices = choices


class ScheduleWidget(MultiWidget):
    def __init__(self, attrs=None):
        widgets = [

            CheckboxSelectMultiple(choices=WEEKDAY_CHOICES),
            TimeInput(attrs={'placeholder': 'Start Time', 'format': '%H:%M'}),
            TimeInput(attrs={'placeholder': 'End Time', 'format': '%H:%M'}),
            SingleSelect(choices=SEASON_CHOICES, attrs={'placeholder': 'Semester'}),
            NumberInput(attrs={'placeholder': 'Year'}),
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
            except (json.JSONDecodeError, TypeError):
                pass
        return [[], None, None, None, None]

    def value_from_datadict(self, data, files, name):
        days = data.getlist(f'{name}_0', [])
        start_time = data.get(f'{name}_1')
        end_time = data.get(f'{name}_2')
        semester = data.get(f'{name}_3')
        year = data.get(f'{name}_4')

        return json.dumps({
            'days': days,
            'start_time': start_time,
            'end_time': end_time,
            'semester': semester,
            'year': year,
        }, indent=2)

