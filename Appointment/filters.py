from django_filters.rest_framework import FilterSet
from Appointment.models import Meet


class MeetFilter(FilterSet):
    class Meta:
        model = Meet
        fields = {
            'start_datetime': ['lt'],
            'end_datetime': ['gt'],
            'service': ['exact'],
            'rating': ['gt', 'lt']
        }
